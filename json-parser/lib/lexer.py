from lib.types import JSONType


class Lexer:
    def lex_string(self, content: str, pos: int):
        text = ""
        is_escape = False
        while pos < len(content):
            char = content[pos]
            if not is_escape and char == '\\':
                is_escape = True
            elif is_escape:
                match char:
                    case c if c in ['b','f','n','r','t','"','\\']:
                        text += f'\\{char}'
                    case '/':
                        text += '/'
                    case 'u':
                        unicode_sequence = content[pos+1:pos+5]
                        try:
                            unicode_char = unicode_sequence.encode('utf-8').decode('unicode-escape')
                            text += unicode_char
                            pos += 4
                        except:
                            raise Exception(f"Invalid Unicode escape sequence: {unicode_sequence}")
                    case _:
                        raise Exception(f"Invalid escape sequence: \\{char}")

                is_escape = False
            elif char == '"':
                pos += 1
                break
            else:
                text += char

            pos+=1
        if pos == len(content) and content[pos - 1] != '"':
            raise Exception("Unterminated string")

        return text, pos



    def lex_number(self, content: str, pos: int):
        start = pos
        while content[pos] is not None and (content[pos].isdigit() or content[pos] in {'-', '.', 'e', 'E', '+'}):
            pos+=1

        num = content[start:pos]
        return num, pos

    def lex_boolean_null(self, content: str, pos:int):
        start = pos

        while content[pos] is not None and content[pos].isalpha():
            pos+=1

        word = content[start:pos]
        if word in ["true", "false", "null"]:
            return word, pos
        else:
            raise Exception(f"Unexpected token: {word}")


    def tokenize(self, content: str):
        tokens = []
        index = 0

        while index < len(content):
            char = content[index]

            if char.isspace():
                index += 1
                continue
            elif char == "{":
                tokens.append((char, JSONType.OPEN_BRACE))
            elif char == "}":
                tokens.append((char, JSONType.CLOSE_BRACE))
            elif char == "[":
                tokens.append((char, JSONType.OPEN_BRACKET))
            elif char == "]":
                tokens.append((char, JSONType.CLOSE_BRACKET))
            elif char == ",":
                tokens.append((char, JSONType.COMMA))
            elif char == ":":
                tokens.append((char, JSONType.COLON))
            elif char.isalpha():
                word, pos = self.lex_boolean_null(content, index)
                tokens.append((word, JSONType.BOOLEAN if word in ["true", "false"] else JSONType.NULL))
                index = pos
                continue
            elif char.isdigit() or char == "-":
                num, pos = self.lex_number(content, index)
                tokens.append((num, JSONType.NUMBER))
                index = pos
                continue
            elif char == '"':
                text, pos = self.lex_string(content, index + 1)
                tokens.append((text, JSONType.STRING))
                index = pos
                continue
            else:
                raise Exception(f"Unexpected token: {char}")

            index += 1

        return tokens
