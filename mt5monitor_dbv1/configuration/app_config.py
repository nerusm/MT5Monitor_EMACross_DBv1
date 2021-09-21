import os
import yaml

fname=str(os.getenv("fname"))
stream = open(fname, 'r')
print(stream.name)
config = yaml.load(stream=stream, Loader=yaml.FullLoader)


def get_round_decimal(symbol):
    if symbol.__contains__('JPY'):
        return 5
    else:
        return config['decimals']

