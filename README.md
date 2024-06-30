# FONCOM-ASK-Communication-System-SDR

ASK Communication System implemented with SDR (Software Defined Radio) in GNU Radio. Part of the final project for FONCOM (*Fonaments de Comunicacions*) subject in UAB, part of the second course of the Electronic Engineering degree (BSc).

## 👨‍💻 Developers

- Adrià Arús - @Addruss
- Nedal Benelmekki - @nmb735

## 📜 Introduction

- We have implemented a digital transmitter and receiver. After analyzing the various modulation options studied, we chose ASK (Amplitude Shift Keying), specifically with OOK (On-Off Keying). This allowed us to expand the scope of the challenge, achieving encoded message transmission and decoded message reception. Each stage is explored in detail in the report.

## 📝 Message Encoding

- Initially, we used a `Vector Source` block to transmit and verify functionality. However, the goal was to transmit real messages. Various encoding strategies were considered, such as Morse Code (due to its similarity with OOK), ASCII, or UTF-8. Finally, we chose UTF-8.

- A custom Python block was created to achieve this (`Embedded Python Block`). Inspired by the source code of the `Vector Source` block (found and translated from `C++` to `Python`), an input parameter (`string`) and new functions were added. The created `Python block`, named `Message Bit Vector Source`, separates each character of the input `string` and encodes it in UTF-8. This generates a bit vector that is continuously transmitted. To identify each message, the message is framed. The start of the message is indicated by the sequence `1111 1111 0000 0000`, and the end by `0000 0000`. This helps synchronize transmitter and receiver.

- It is known and accepted due to the found limitations that using the sequence `1111 1111` means one possible character (`ÿ`) cannot be transmitted.

## 📡 Transmission

- Once the message is encoded in binary, a space is first introduced between the bits to avoid overlap between pulses with the `Interpolating FIR Filter` block.

- Next, Nyquist pulses are generated using the `Root Raised Cosine Filter` block. Finally, it is multiplied by a carrier frequency cosine and sent.

## 📶 Channel

- To simulate the channel, we used the ideal channel model ℎ𝑐 =𝛼 𝛿(𝑡−𝑡𝑑) where the `Delay` block allows adjusting the channel delay time 𝑡𝑑, the `Multiply Const` block adjusts the attenuation 𝛼, and white Gaussian noise is added with the `Noise Source` block.

## 📥 Reception

The reception consists of:

1. A Nyquist pulse filter with the `Root Raised Cosine Filter` block, which removes the cosine.

2. A decision maker that, based on a threshold called gamma, decides if it is a 1 or a 0 using the `Threshold` block.

Finally, samples are taken to obtain the original string.

## 🔄 Message Decoding

- The last step is to decode the message. Synchronization of the received signal and alignment of the bits for decoding is necessary. A custom Python block was created to achieve this (`Embedded Python Block`), named `Message Sink`.

- The start sequence described in `Message Encoding` is used to "wake up" the decoder. This is necessary because initially no signal is received, and the decoder interprets it as bytes of all zeros. Once "awake," it accumulates the bytes received from each frame and decodes each character of the message. This message is printed to the screen (it is printed each time it changes to avoid overflow). Printing each time it changes allows detecting errors and observing what is being received at each moment.

## 🔧 Example of Use

- Start by selecting the message in `Message Bit Vector Source`.

- Ensure that the transmitted message is correct (assuming "FONCOM" as the sent message):

  - `1111 1111 0000 0000`: Start sequence

  - `0100 0110`: F in UTF-8

  - `0100 1111`: O in UTF-8

  - `0100 1110`: N in UTF-8

  - `0100 0011`: C in UTF-8

  - `0100 0011`: O in UTF-8

  - `0100 1101`: M in UTF-8

  - `0000 0000`: End sequence

## 🧪 Testing and Quality Assurance

- Several tests were proposed to analyze the robustness of the implemented system. Below are the tests conducted.

### 📉 Robustness to Channel Noise Amplitude

- We wanted to check how the channel noise amplitude affects the system. A small system was implemented to subtract the sent message from the received message to see the differences.

- At a noise amplitude of 0.4, errors begin to appear. The message is decoded correctly, and it can be fixed by adjusting the gamma.

- At a noise amplitude of 0.6, errors occur that cannot be fixed by adjusting the gamma. The message decoding suffers because the synchronization sequence is modified. An estimated BER of 3% was observed.

- At maximum noise amplitude (2), there is a high error rate. Decoding is non-existent as the synchronization sequence is modified. An estimated BER of 50% was observed.

### 📉 Robustness to Channel Attenuation

- We wanted to check how channel attenuation affects the system. The same system used in the "Robustness to Channel Noise Amplitude" test was employed.

- At an attenuation 𝛼=0.1, if a gamma that discriminates at 200mV is used, the message is received and decoded correctly.

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for more details.

## ⚠️ Disclaimer

This code is provided for educational purposes only. The authors are not responsible for any use of this code in any form of academic dishonesty or plagiarism. Please adhere to your institution's academic integrity policies when using or referencing this code.
