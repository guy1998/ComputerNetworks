import secrets
import random
# Here can be found the methods used to simulate a real transmission environment.
# The method generate_random_message simulates a messages sent by the sender
# The method transmitter simulates the unreliable data transfer channel
# And finally the method code_garbled simulates an error mask which changes certain amount of the message


# This method is used to generate random messages provided the size in bytes
# It does this by generating a random integer based on the number of bits needed
# Then this integer can be converted into a binary string representation
def generate_random_message(size_in_bytes):
    num_bits = size_in_bytes * 8
    binary_string = '0'
    while binary_string[0] != '1':  # makes sure that the message starts with a one
        # so all the bytes of the message are valid
        random_integer = secrets.randbits(num_bits)
        binary_string = bin(random_integer)[2:]
        binary_string = binary_string.zfill(num_bits)
    return binary_string


def code_garbled(message, mask_percentage):
    if not 0 <= mask_percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100")
    num_bits = len(message)
    num_bits_to_garble = int(mask_percentage / 100 * num_bits)
    garble_indices = random.sample(range(num_bits), num_bits_to_garble)
    binary_list = list(message)
    for index in garble_indices:
        binary_list[index] = '1' if binary_list[index] == '0' else '0'
    garbled_message = ''.join(binary_list)
    return garbled_message


def transmitter(message, error_rate):
    garbled_message = code_garbled(message, error_rate)
    return garbled_message
