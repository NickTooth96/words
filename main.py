import re
import sys
import argparse

import parse as p
    

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--pattern', '-p', required=True, metavar='pattern', help='pattern')
parser.add_argument('--has', '-s', required=False, metavar='has', help='has letters')
parser.add_argument('--has-not', '-n', required=False, metavar='not', help='missing letters')
parser.add_argument('--non', '-z', required=False, metavar='non', help='non_pattern' )

argparse = parser.parse_args()



if len(argparse.pattern) != 5:
    print('Pattern must be 5 characters long')
    sys.exit(1)

dictionary = p.get_words()
five_letter_words = {k:v for k,v in dictionary.items() if len(k) == 5}

if not argparse.has and not argparse.has_not:
    options = {}
    for flw in five_letter_words:
        options[flw] = p.word_score(flw,p.appearance_of_letter(five_letter_words))
else: 

    if argparse.has:
        yellow_letters = [char for char in argparse.has]
    if argparse.has_not:
        has_not = [char for char in argparse.has_not]  


    options = {k:v for k,v in five_letter_words.items() if re.match(argparse.pattern, k)}

    if argparse.has_not:
        for char in has_not:
            options = {k:v for k,v in options.items() if char not in k}
            
    if argparse.has:
        for char in yellow_letters:
            options = {k:v for k,v in options.items() if char in k}
            
            
    for opt in options:
        options[opt] = p.word_score(opt, p.appearance_of_letter(options))
        
    if argparse.non:
        np_list = argparse.non.split(',')
        for np in np_list:
            options = {k:v for k,v in options.items() if not re.match(np, k)}
    

options = dict(sorted(options.items(), key=lambda x: x[1]))

for word in options:
    print(word, options[word])

print("Possible words found:",len(options))