from crc import crc_experiment

if __name__ == "__main__":
    crc_experiment("1000000000000011", 65536, "x^15+x+1")
