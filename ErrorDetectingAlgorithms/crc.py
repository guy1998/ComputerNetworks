import secrets


# This method is used to generate random messages provided the size in bytes
# It does this by generating a random integer based on the number of bits needed
# Then this integer can be converted into a binary string representation
def generate_random_message(size_in_bytes):
    num_bits = size_in_bytes * 8
    random_integer = secrets.randbits(num_bits)
    binary_string = bin(random_integer)[2:]
    binary_string = binary_string.zfill(num_bits)
    return binary_string


def long_message_modulo_2_division(dividend, divisor):
    current_string = dividend[:8]
    i = 8
    while True:
        int_dividend = int(current_string, 2)
        int_divisor = int(divisor, 2)
        result = bin(int_dividend % int_divisor)[2:]
        if i >= len(result):
            return result
        elif i+8-len(result) > len(dividend):
            current_string = result + dividend[i:len(dividend)]
            i = len(dividend)
        else:
            current_string = result + dividend[i: i+8-len(result)]
            i = i+8-len(result)


def modulo_2_division(dividend, divisor):
    int_dividend = int(dividend, 2)
    print(int_dividend)
    int_divisor = int(divisor, 2)
    result = int_dividend % int_divisor
    return bin(result)[2:]


def binary_addition(sequence_1, sequence_2):
    int_rep_seq_1 = int(sequence_1, 2)
    int_rep_seq_2 = int(sequence_2, 2)
    result = int_rep_seq_1 + int_rep_seq_2
    return bin(result)[2:]


def padding_with_zeros(message, nr_of_zeros):
    zeros = '0' * nr_of_zeros
    new_message = message + zeros
    return new_message


def calculate_crc(message, generator):
    message = padding_with_zeros(message, (len(generator)-1))
    remainder = modulo_2_division(message, generator)
    return binary_addition(message, remainder)
