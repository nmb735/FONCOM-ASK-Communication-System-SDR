import numpy as np
from gnuradio import gr

class MessageBitVectorSource(gr.sync_block):
    """
    Custom GNU Radio block for converting a message into a bit vector source.

    Attributes:
        bits (list): The message converted into a sequence of bits.
        index (int): The current position in the bit sequence.

    Methods:
        string_to_bits(s): Converts a string into a sequence of bits.
        char_to_bits(char): Converts a character into a sequence of bits.
        work(input_items, output_items): The main function called by GNU Radio to process the data.
    """
    def __init__(self, message="Hello"):  # Default message, just in case (can be changed later)
        gr.sync_block.__init__(self,
            name="Message Bit Vector Source",
            in_sig=None,
            out_sig=[np.byte])
        # Add the synchronization sequence, start sequence, and the frame to the message
        self.bits = [1]*8 + self.string_to_bits('\0' + message + '\0')
        self.index = 0  # Initialize the index to track current position in the bit sequence

    def string_to_bits(self, s):
        return [b for character in s for b in self.char_to_bits(character)]

    def char_to_bits(self, char):
        return [int(bit) for b in char.encode('utf-8') for bit in bin(b)[2:].zfill(8)]

    def work(self, input_items, output_items):
        noutput_items = len(output_items[0])
        for i in range(noutput_items):
            output_items[0][i] = self.bits[self.index]
            self.index = (self.index + 1) % len(self.bits)  # Loop back to the start if at the end
        return noutput_items
    

