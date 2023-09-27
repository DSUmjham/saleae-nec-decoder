# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from audioop import reverse
from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):

	# Settings:
	frame_label_format = ChoicesSetting(['Decimal', 'Hex', 'Binary'])

	# An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
	result_types = {
		'mytype': {
			'format': '{{data.result}}'
		}
	}

	def __init__(self):
		'''
		Initialize HLA.

		Settings can be accessed using the same name used above.
		'''
		self.byte_array = []
		self.byte_frame_start = None
		self.first_frame_start = None

	def decode(self, frame: AnalyzerFrame):
		'''
		Process a frame from the input analyzer, and optionally return a single `AnalyzerFrame` or a list of `AnalyzerFrame`s.

		The type and data values in `frame` will depend on the input analyzer.
		'''

		# mark the beginning of the frame and get the initial size
		if self.first_frame_start is None:
			self.first_frame_start = frame.start_time
		this_frame_size = int(float(frame.end_time - frame.start_time) * 100000)
		frame_label = ""

		# 9ms leading pulse burst + 4.5ms space for the beginning of the transmission
		if 1400 < this_frame_size < 1430:
			frame_label = "START FRAME"
		# repeats typically begin ~40ms after the end of the message
		elif 4000 < this_frame_size < 4100:
			frame_label = "REPEAT GAP"
		# repeats follow the gap with a 9ms burst, 2.25ms space, and a 562.5us pulse burst
		elif 1150 < this_frame_size < 1200:
			if self.byte_frame_start is None:
				self.byte_frame_start = frame.start_time
			return
		elif 40 < this_frame_size < 70:
			frame_label = "REPEAT"
			frame_start = self.byte_frame_start
			self.byte_frame_start = None
			return AnalyzerFrame('mytype', frame_start, frame.end_time, {
				'result': frame_label
			})
		# handle the address and command along with thier logical inverses
		else:
			# each frame in this section represents a bit, mark the start of the first 
			if self.byte_frame_start is None:
				self.byte_frame_start = frame.start_time

			# start building bytes
			bit = 0
			if 100 < this_frame_size < 130:		# transmit time 1.125ms
				bit = 0
			elif 210 < this_frame_size < 240:		# transmit time 2.25ms
				bit = 1
			self.byte_array.append(bit)
				
			# check for a full byte and reverse the order of the bits to correct endianness 
			if len(self.byte_array) == 8:
				reversed_byte = int(''.join(map(str, self.byte_array[::-1])), 2)
				# get the label in the correct format for the user-chosen option
				if self.frame_label_format == "Hex":
					reversed_byte = '0x{:02x}'.format(int(reversed_byte))
				elif self.frame_label_format == "Binary":
					reversed_byte = '0b{:08b}'.format(int(reversed_byte))
					
				# make the new frame, spans 1 byte of data
				frame_start = self.byte_frame_start
				
				# cleanup variables for reuse in the next byte
				self.byte_array = []
				self.byte_frame_start = None

				# print the contents of the frame to the Terminal
				print(reversed_byte)

				return AnalyzerFrame('mytype', frame_start, frame.end_time, {
					'result': str(reversed_byte)
				})
			else:
				return
			
		# Return the data frame itself
		return AnalyzerFrame('mytype', frame.start_time, frame.end_time, {
			'result': frame_label
		})