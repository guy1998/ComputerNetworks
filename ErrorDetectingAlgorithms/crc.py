from env_simulator_methods import transmitter, generate_random_message
import pandas as pd
import random


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


def verify_crc(crc_code, generator):
    remainder = modulo_2_division(crc_code, generator)
    integer_remainder = int(remainder, 2)
    return not (integer_remainder == 0)


def channel_that_employs_crc(message, generator, error_rate):
    crc_code = calculate_crc(message, generator)
    arriving_code = transmitter(crc_code, error_rate)
    return verify_crc(arriving_code, generator)


def count_result(result_list):
    cnt = 0
    for item in result_list:
        if item:
            cnt += 1
    return cnt / len(result_list)


def generate_result_table(path, result_dict, polynomial):
    columns = ["0-5%", "6-10%", "11-15%", "16-20%", "21-25%", "26-30%",
               "31-35%", "36-40%", "41-45%", "46-50%", "51-55%", "56-60%", "61-65%", "66-70%"]
    table_dict = {}
    for key, column in zip(result_dict.keys(), columns):
        table_dict[column] = count_result(result_dict[key])
    df = pd.DataFrame(table_dict, index=[polynomial])
    df.to_csv(path)


def crc_experiment(generator, message_size, poly_string):
    rates = [(0, 5), (6, 10), (11, 15), (16, 20), (21, 25), (26, 30),
             (31, 35), (36, 40), (41, 45), (46, 50), (51, 55), (56, 60), (61, 65), (66, 70)]
    rate_cnt = 0
    result_tracker = {}
    for i in range(500):
        print("Iteration number: " + str(i+1))
        if rate_cnt == 14:
            rate_cnt = 0
        random_message = generate_random_message(message_size)
        result = channel_that_employs_crc(random_message, generator, random.randint(rates[rate_cnt][0], rates[rate_cnt][1]))
        if rates[rate_cnt] in result_tracker:
            result_tracker[rates[rate_cnt]].append(result)
        else:
            result_tracker[rates[rate_cnt]] = [result]
        rate_cnt += 1
    generate_result_table("crc_results/" + poly_string + "/"+str(message_size)+".csv", result_tracker, poly_string)
