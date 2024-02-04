

# Function to find the Checksum of Sent Message
def find_checksum(message, k):
    # Dividing sent message in packets of k bits where k will be 16 or 32
    integer_sum = 0
    i = 0
    while k <= len(message):
        integer_sum += int(message[i:k], 2)
        i = k
        k += k
    binary_sum = bin(integer_sum)[2:]
    if len(binary_sum) > k:
        x = len(binary_sum) - k
        binary_sum = bin(int(binary_sum[0:x], 2) + int(binary_sum[x:], 2))[2:]
    if len(binary_sum) < k:
        binary_sum = '0' * (k - len(binary_sum)) + binary_sum
    checksum = ''
    for i in binary_sum:
        if i == '1':
            checksum += '0'
        else:
            checksum += '1'
    return checksum


def generate_receiver_checksum(received_message, checksum, k):
    pass


def verify_checksum(sender_checksum, receiver_checksum):
    pass


