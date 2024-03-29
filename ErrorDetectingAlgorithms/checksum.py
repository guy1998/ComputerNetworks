from env_simulator_methods import generate_random_message, transmitter
import random
import pandas as pd


def calculating_complement(binary_string):
    complement = ''
    for i in binary_string:
        if i == '1':
            complement += '0'
        else:
            complement += '1'
    return complement


# Function to find the Checksum of Sent Message
def find_checksum(message, k):
    # Dividing sent message in packets of k bits where k will be 16 or 32
    integer_sum = 0
    i = k
    while i <= len(message):
        integer_sum += int(message[i-k:i], 2)
        if integer_sum > 65535:
            integer_sum = integer_sum - 65536 + 1
        i += k
    binary_sum = bin(integer_sum)[2:]
    if len(binary_sum) < k:
        binary_sum = '0' * (k - len(binary_sum)) + binary_sum  # zero padding in case number is smaller than k bits

    return calculating_complement(binary_sum)


def generate_receiver_checksum(received_message, checksum, k):
    integer_sum = 0
    i = k
    while i <= len(received_message):
        integer_sum += int(received_message[i-k:i], 2)
        if integer_sum > 65535:
            integer_sum = integer_sum - 65536 + 1
        i += k
    integer_sum = integer_sum + 2 * int(checksum, 2)  # Adding the received checksum
    if integer_sum > 65535:
        integer_sum = integer_sum - 65536 + 1
    binary_sum = bin(integer_sum)[2:]
    return calculating_complement(binary_sum)


def verify_checksum(sender_checksum, receiver_checksum):
    final_sum = bin(int(sender_checksum, 2) + int(receiver_checksum, 2))[2:]
    final_comp = calculating_complement(final_sum)
    return not (int(final_comp, 2) == 0)


def channel_that_employs_checksum(message, checksum_size, error_rate):
    checksum = find_checksum(message, checksum_size)
    transmitted_message = transmitter(message, error_rate)
    receiver_checksum = generate_receiver_checksum(transmitted_message, checksum, checksum_size)
    return verify_checksum(checksum, receiver_checksum)


def count_result(result_list):
    cnt = 0
    for item in result_list:
        if item:
            cnt += 1
    return cnt / len(result_list)


def generate_result_table(path, result_dict, check_sum_size):
    columns = ["0-5%", "6-10%", "11-15%", "16-20%", "21-25%", "26-30%",
               "31-35%", "36-40%", "41-45%", "46-50%", "51-55%", "56-60%", "61-65%", "66-70%"]
    table_dict = {}
    for key, column in zip(result_dict.keys(), columns):
        table_dict[column] = count_result(result_dict[key])
    df = pd.DataFrame(table_dict, index=[check_sum_size])
    df.to_csv(path)


def checksum_experiment(message_size, check_sum_size):
    rates = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 25), (26, 30),
             (31, 35), (36, 40), (41, 45), (46, 50), (51, 55), (56, 60), (61, 65), (66, 70)]
    rate_cnt = 0
    result_tracker = {}
    for i in range(500):
        print("Iteration number: " + str(i+1))
        if rate_cnt == 14:
            rate_cnt = 0
        random_message = generate_random_message(message_size)
        result = channel_that_employs_checksum(random_message,
                                               check_sum_size, random.randint(rates[rate_cnt][0], rates[rate_cnt][1]))
        if rates[rate_cnt] in result_tracker:
            result_tracker[rates[rate_cnt]].append(result)
        else:
            result_tracker[rates[rate_cnt]] = [result]
        rate_cnt += 1
    generate_result_table("checksum_results/" + str(check_sum_size) + "_bit_checksum/" + str(message_size) + ".csv",
                          result_tracker, str(check_sum_size) + "-bits")
