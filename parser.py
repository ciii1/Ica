from dataclasses import dataclass
from enum import Enum

class NodeType(Enum):
    KEYWORD = 1
    CONTENT = 2
    CONTENT_KEYWORD = 3

@dataclass
class Node:
    _type:NodeType
    text:str

class ParseError(Exception):
    def __init__(self, message, line_num, char_num):
        self.message = "An error encountered while parsing: " + message + f" at ({line_num},{char_num})"
        self.line_num = line_num
        self.char_num = char_num
        super().__init__(self.message)

def parse(text):
    output = []
    line_num = 1
    char_num = 0
    parts = text.split("\n===\n") 
    special_tokens_list = [
        ["{", "}", NodeType.CONTENT_KEYWORD], #[opening, closing, type]
        ["<", ">", NodeType.KEYWORD],
        ["[", "]", NodeType.CONTENT],
    ]
    for part in parts:
        local_output = []
        curr_str = ""
        last_char = ""
        opening = ""
        for char in part:
            if char == "\n":
                line_num += 1
                char_num = 0
            else:
                char_num += 1
            is_special_token = False
            for special_tokens in special_tokens_list:
                if char in special_tokens and last_char != "\\":
                    if special_tokens[0] == char: #if it's the opening
                        is_special_token = True
                        opening = char
                        curr_str = ""
                    elif special_tokens[1] == char: #if it's the closing
                        if opening == "":
                            raise ParseError(f"The closing '{char}' is not opened", line_num, char_num)
                        elif special_tokens[0] != opening:
                            raise ParseError(f"The closing '{char}' doesn't match the opening '{opening}'", line_num, char_num)
                        opening = ""
                        is_special_token = True
                        local_output.append(Node(special_tokens[2], curr_str))
                        curr_str = ""
            if not is_special_token:
                curr_str += char
            last_char = char
        if opening != "":
            raise ParseError(f"Unclosed '{opening}'", line_num, char_num)
        output.append(local_output)
        line_num += 2
        char_num = 0
    return output

