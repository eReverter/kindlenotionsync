#!/usr/bin/env python3
'''
Auxiliary functions.
'''
import unicodedata

def format_text(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    formatted_text = ''
    for i, char in enumerate(text[:-1]):
        if char != ' ' or (char == ' ' and text[i + 1].isalnum()):
            formatted_text += char
    if text[-1] != ' ':
        formatted_text += text[-1]
    return formatted_text.replace(u' \xa0', '')