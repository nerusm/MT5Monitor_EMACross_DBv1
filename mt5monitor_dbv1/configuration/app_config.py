import yaml
import os

fname=str(os.getenv("fname"))
stream = open(fname, 'r')
print(stream.name)
config = yaml.load(stream=stream, Loader=yaml.FullLoader)
