# Saleae Logic 2 NEC Protocol Decoder
This extension facilitates decoding NEC infrared (IR) codes using Saleae Logic 2. The extension currently can deocode and label standard IR transmissions assuming the address and command fields are both one byte long. It has not been tested against the extended NEC protcol.

Not all features of the NEC protocol are currently implemented; this was a test project used for pulling codes from an inexpensive RGB LED strip receiver. 

## Getting Started
To use this extension, you will need to install it to your Logic 2 instance. Once installed, capture an IR transmission or use one of the [sample captures](https://github.com/DSUmjham/saleae-nec-decoder/tree/main/captures) provided in this repository.

1. Configure your capture device to record **1 MS/s** on a digital channel. Higher sample rates may cause issues with frame processing.
2. With a capture open in Logic 2, add a **Simple Parallel Analyzer**
    * For **D0** choose the capture channel which has the IR stream
    * Set **Clock** to the same capture channel
    * **Clock State** generally will be **Falling Edge** or **Rising Edge** depending on the configuration of yoru receiver.
3. Add a second analyzer, **NEC Protocol Decoder**
    * Set the **Input Analyzer** to the **Simple Paralell** analyzer you added in the previous step.
    * Choose the data format address and code fields (decimal, hex, or binary).
4. You will see each frame labeled with either type (e.g., START_FRAME) or the values of the address/command in the datatype you specified.
5. The raw data of each frame is also printed to the Terminal inside of Logic 2. 

![Logic 2 screenshot of extension](https://github.com/DSUmjham/saleae-nec-decoder/blob/main/images/logic2-screenshot01.jpg?raw=true)