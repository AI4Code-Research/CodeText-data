import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Set, Optional

DOCSTRING_REGEX = re.compile(r"(['\"])\1\1(.*?)\1{3}", flags=re.DOTALL)
DOCSTRING_REGEX_TOKENIZER = re.compile(r"[^\s,'\"`.():\[\]=*;>{\}+-/\\]+|\\+|\.+|\(\)|{\}|\[\]|\(+|\)+|:+|\[+|\]+|{+|\}+|=+|\*+|;+|>+|\++|-+|/+")


def remove_words_in_string(words, string):
    new_string = string
    for word in words:
        new_string = str(new_string).replace(word, '')
    return new_string


def tokenize_docstring(docstring: str) -> List[str]:
    return [t for t in DOCSTRING_REGEX_TOKENIZER.findall(docstring) if t is not None and len(t) > 0]


def tokenize_code(node, blob: str, nodes_to_exclude: Optional[Set]=None) -> List:
    tokens = []
    traverse(node, tokens)
    # print(tokens)
    # for token in tokens:
    #     print(token.text)
    return [match_from_span(token, blob) for token in tokens if nodes_to_exclude is None or token not in nodes_to_exclude]


def traverse(node, results: List) -> None:
    if node.type == 'string':
        results.append(node)
        return
    for n in node.children:
        traverse(n, results)
    if not node.children:
        results.append(node)


def traverse_type(node, results, kind:List) -> None:
    if node.type in kind:
        results.append(node)
    if not node.children:
        return
    for n in node.children:
        traverse_type(n, results, kind)
        

def match_from_span(node, blob: str) -> str:
    lines = blob.split('\n')
    line_start = node.start_point[0]
    line_end = node.end_point[0]
    char_start = node.start_point[1]
    char_end = node.end_point[1]
    if line_start != line_end:
        return '\n'.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
    else:
        return lines[line_start][char_start:char_end]


class LanguageParser(ABC):
    # @staticmethod
    # @abstractmethod
    # def get_definition(tree, blob: str) -> List[Dict[str, Any]]:
        # pass

    @staticmethod
    @abstractmethod
    def get_class_metadata(class_node, blob):
        pass

    @staticmethod
    @abstractmethod
    def get_function_metadata(function_node, blob) -> Dict[str, str]:
        pass

    # @staticmethod
    # @abstractmethod
    # def get_context(tree, blob):
    #     raise NotImplementedError

    # @staticmethod
    # @abstractmethod
    # def get_calls(tree, blob):
    #     raise NotImplementedError