import json
import re

'''
From StackOverflow:
Author: Chr1s
URL: https://stackoverflow.com/questions/65910282/jsondecodeerror-invalid-escape-when-parsing-from-python
'''

class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)