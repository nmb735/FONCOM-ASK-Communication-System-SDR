import numpy as np
from gnuradio import gr

class MessageSink(gr.sync_block):
    """
    Custom GNU Radio block that takes a stream of floats as input and prints a string corresponding to the UTF-8 encoding of the bits.

    Attributes:
        bits (list): The message converted into a sequence of bits.
        chars (list): The characters of the current message.
        in_message (bool): A flag indicating whether we are currently within a message.
        delay (int): The delay in samples.
        last_message (str): The last printed message.

    Methods:
        float_to_bit(f): Converts a float into a bit using a threshold.
        bits_to_char(bits): Converts a sequence of bits into a character.
        work(input_items, output_items): The main function called by GNU Radio to process the data.
    """
    def __init__(self, delay=100):  # Default delay, just in case (can be changed later)
        gr.sync_block.__init__(self,
            name="Message Sink",
            in_sig=[np.float32],
            out_sig=None)
        self.bits = [] # List to store the bits
        self.chars = [] # List to store the characters
        self.in_message = False  # Flag to indicate if we are within a message
        self.delay = delay  # Delay in samples
        self.last_message = "" # Last printed message

    # Function to convert a float into a bit
    def float_to_bit(self, f):
        return 1 if f > 0.5 else 0 # Threshold to decide bit value (at 0.5)

    # Function to convert a sequence of bits into a character
    def bits_to_char(self, bits):
        return chr(int(''.join(map(str, bits)), 2))

    def work(self, input_items, output_items):
        ninput_items = len(input_items[0])
        
        # Convert floats to bits using the threshold
        self.bits.extend(self.float_to_bit(bit) for bit in input_items[0][:ninput_items])

        if len(self.bits) < self.delay:
            # Not enough bits to start processing, return
            return ninput_items

        # Apply delay
        self.bits = self.bits[self.delay:]

        # Main processing loop
        while len(self.bits) >= 8:
            byte = self.bits[:8] # Get the next byte
            self.bits = self.bits[8:]  # Remove processed bits

            # Check for synchronization sequence
            if byte == [1, 1, 1, 1, 1, 1, 1, 1]:
                if self.bits[:8] == [0, 0, 0, 0, 0, 0, 0, 0]:
                    self.bits = self.bits[8:]  # Remove the second part of the synchronization sequence
                    self.in_message = True  # Start processing
                continue

            # Process the message
            if self.in_message:
                try:
                    if byte == [1, 1, 1, 1, 1, 1, 1, 1]:
                        # Skip appending the start sequence to the message
                        continue
                    # Convert the byte to a character
                    char = self.bits_to_char(byte)
                    if char == '\0':
                        # End of message
                        message = ''.join(self.chars)
                        if message != self.last_message:  # Only print the message if it has changed
                            print(f"Received message: {message}")  # Print the message
                            self.last_message = message  # Update the last printed message
                        self.chars = []  # Clear the list of characters for the next message
                        self.in_message = False  # Reset the message flag
                    else:
                        self.chars.append(char)  # Add the character to the list of characters
                except ValueError:
                    # Invalid character, skip this byte
                    continue

        return ninput_items
