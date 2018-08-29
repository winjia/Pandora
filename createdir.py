import random

stringseed = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

class MakeDir():
    def __init__(self):
        pass

    def gen_url(self):
        string = ''.join(random.sample(stringseed, 32))
        return string

    def gen_extract_code(self):
        string = "abcdefghijklmnopqrstuvwxyz1234567890"
        string = ''.join(random.sample(stringseed, 4))
        return string

    def gen_dir(self):
        string = "abcdefghijklmnopqrstuvwxyz1234567890"
        string = ''.join(random.sample(stringseed, 8))
        return string
