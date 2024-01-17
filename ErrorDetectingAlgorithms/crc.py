import random
import secrets


ranges_of_error = [
                        [1, 5], [6, 10], [11, 15],
                       [16, 20], [21, 25], [26, 30],
                       [31, 35], [36, 40], [41, 45],
                       [46, 50], [51, 55], [56, 60],
                       [61, 65], [66, 70]
                    ]


def xor(first_number, second_number):
    result = []
    for i in range(1, len(second_number)):
        if first_number[i] == second_number[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)


def modulo2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0: pick]
    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)
    checkword = tmp
    return checkword


def range_to_percentage(error_range):
    return random.randint(error_range[0], error_range[1])


def random_message_generator(nr_of_bytes):
    random_bytes = secrets.token_bytes(nr_of_bytes)
    bits = ''.join(format(byte, '08b') for byte in random_bytes)
    return bits


def error_mask(message, percentage_of_error):
    num_bits_to_flip = int(len(message) * percentage_of_error / 100)
    indices_to_flip = random.sample(range(len(message)), num_bits_to_flip)
    message_list = list(message)
    for index in indices_to_flip:
        message_list[index] = '1' if message_list[index] == '0' else '0'
    error_masked_message = ''.join(message_list)
    return error_masked_message


def crc_coder(message, generator):
    nr_of_appended_zeros = len(generator)
    message_with_added_zeros = message + '0'*nr_of_appended_zeros
    remainder = modulo2div(message_with_added_zeros, generator)
    coded_message = message + remainder
    return coded_message


def error_detector(crc_message, generator):
    remainder = modulo2div(crc_message, generator)
    for i in range(len(remainder)):
        if remainder[i] == '1':
            return 0
    return 1


def polynomial_to_generator(polynomial):
    i = 0
    number = 0
    while i < len(polynomial):
        if polynomial[i] == '^':
            number += 2 ** int(polynomial[i+1])
        elif polynomial[i] == 1:
            number += 1
        elif polynomial[i] == 'x':
            if i == len(polynomial) - 1 or polynomial[i+1] != '^':
                number += 2
    return bin(number)[2:]


def transmission_simulation(message, error_range, generator):
    transmitted_message = crc_coder(message, generator)
    erroneous_message = error_mask(transmitted_message, range_to_percentage(error_range))
    return error_detector(erroneous_message, generator)


def write_to_file(file_path, index, line_dictionary):
    pass


def crc_study(length_of_message):
    with open('generators.txt', 'r') as file:
        # Iterate over each line in the file
        for line in file:
            bit_generator = polynomial_to_generator(line)
            outcomes = []
            result_tracker = {}
            for error_range in ranges_of_error:
                for i in range(500):
                    message = random_message_generator(length_of_message)
                    outcomes.append(transmission_simulation(message, error_range, bit_generator))
                result_tracker[str(error_range[0]) + "% - " + str(error_range[1]) + "%"] = sum(outcomes)/len(outcomes)
            # write_to_file("results_for_"+str(length_of_message)+"_bytes_messages.txt", bit_generator, result_tracker)
            print(result_tracker)
