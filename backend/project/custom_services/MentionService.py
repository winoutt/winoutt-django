import re

def parse_keyword(text, parse_character):
    if not text:
        return []

    regex = '(' + parse_character + '\w+)'
    matches = re.findall(regex, text)
    if len(matches) <= 0:
        return []
    mentions = list(set(matches))
    mentions_without_parse_char = map(lambda x: x.replace(parse_character, ""), mentions) 
    return list(mentions_without_parse_char)
    