import base64
import hashlib as dec


class EncodeString:
    def __init__(self, string):
        self.string = str(string)

    def switch(self, choice):
        default = "Invalid input"
        encryption_choice = {
            'base84': '1',
            'base64': '2',
            'base32': '3',
            'base16': '4',
            'SHA256': '5',
            'SHA384': '6',
            'SHA512': '7',
            'blake2b': '8',
            'md5': '9'
        }
        return getattr(self, 'encode_' + encryption_choice[choice], lambda: default)()

    def encode_1(self):
        return EncodeString(base64.b85encode(bytes(self.string, 'ascii')))

    def encode_2(self):
        return EncodeString(base64.b64encode(bytes(self.string, 'ascii')))

    def encode_3(self):
        return EncodeString(base64.b32encode(bytes(self.string, 'ascii')))

    def encode_4(self):
        return EncodeString(base64.b16encode(bytes(self.string, 'ascii')))

    def encode_5(self):
        m = dec.sha256()
        m.update(bytes(self.string, 'ascii'))
        return EncodeString(m.hexdigest())

    def encode_6(self):
        m = dec.sha384()
        m.update(bytes(self.string, 'ascii'))
        return EncodeString(m.hexdigest())

    def encode_7(self):
        m = dec.sha512()
        m.update(bytes(self.string, 'ascii'))
        return EncodeString(m.hexdigest())

    def encode_8(self):
        m = dec.blake2b()
        m.update(bytes(self.string, 'ascii'))
        return EncodeString(m.hexdigest())

    def encode_9(self):
        m = dec.md5()
        m.update(bytes(self.string, 'ascii'))
        return EncodeString(m.hexdigest())
