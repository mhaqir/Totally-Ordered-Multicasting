

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--com',  help = "Directory of the command file")
parser.add_argument('-o', help = "Directory for outputs")
parser.add_argument('--id', help = "An id for client e.g. c1")
parser.add_argument('--nc', help = "Expected numebr of clients", type = int)

def get_config():
    config, unparsed = parser.parse_known_args()
    return config, unparsed
