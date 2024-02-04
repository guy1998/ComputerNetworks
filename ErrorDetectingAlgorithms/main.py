from crc import calculate_crc, generate_random_message, modulo_2_division, long_message_modulo_2_division

if __name__ == "__main__":
    message = generate_random_message(1024)
    print("Message: " + message)
    # print(calculate_crc(message, "1100"))
    print("Simple modulo 2: ")
    print(modulo_2_division(message, "1100"))
    # print("Complicated modulo 2: ")
    # print(long_message_modulo_2_division(message, "1100"))
