from lib.types import JSONType


class Syntax:
    def __init__(self, tokens, index):
        self.tokens = tokens
        self.index = index

    def next_token(self):
        self.index += 1
        if self.index > len(self.tokens):
            raise IndexError("No more tokens")

    def parse_colon(self):
        if self.tokens[self.index][1] != JSONType.COLON:
            raise ValueError("Expected colon")
        self.next_token()

    def parse_comma(self):
        print("self.tokens[self.index][1]", self.tokens[self.index][1])
        if self.tokens[self.index][1] != JSONType.COMMA:
            raise ValueError("Expected comma")
        self.next_token()

    def parse_key(self):
        if self.tokens[self.index][1] != JSONType.STRING:
            raise ValueError("Expected string key")
        key = self.tokens[self.index][0]
        return key

    def parse_string(self):
        return self.tokens[self.index][0]

    def parse_number(self):
        return int(self.tokens[self.index][0])

    def parse_array(self):
        arr = []

        while self.tokens[self.index][1] != JSONType.CLOSE_BRACKET:
            arr.append(self.parse_value())
            self.parse_comma()

        self.next_token()
        return arr

    def parse_object(self):
        dict = {}
        self.next_token()

        while self.tokens[self.index][1] != JSONType.CLOSE_BRACE:
            key = self.parse_key()
            self.next_token()
            self.parse_colon()
            value = self.parse_value()

            dict[key] = value

            if self.tokens[self.index][1] == JSONType.CLOSE_BRACE:
                break
            self.parse_comma()

        self.next_token()
        return dict


    def parse_value(self):
        token = self.tokens[self.index][1]
        if token == JSONType.STRING:
            val =  self.parse_string()
            self.next_token()
            return val
        elif token == JSONType.NUMBER:
            val = self.parse_number()
            self.next_token()
            return val
        elif token == JSONType.OPEN_BRACKET:
            return self.parse_array()
        elif token == JSONType.OPEN_BRACE:
            return self.parse_object()
        elif token == JSONType.NULL:
            self.next_token()
            return None
        elif token == JSONType.BOOLEAN:
            val = self.tokens[self.index][0] == "true"
            self.next_token()
            return val

        else:
            raise ValueError(f"Unexpected token: {token}")

    def parse(self):
        if self.tokens[self.index][1] != JSONType.OPEN_BRACE:
            raise ValueError("Expected an object")
        else:
            result = self.parse_value()
            return result
