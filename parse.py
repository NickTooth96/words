import json


def spoof_regex(pattern):
    pat_list = pattern.split('.')
    regex_key = '^'
    
    # ^\w{2}a\w{2}$
    
    unknown = 0
    for l in pat_list:
        print(l,len(l))
        if len(l) == 0:
            regex_key += '\w{1}'  
        else:
            regex_key += l

    print(regex_key)
    return regex_key
            
def get_words():
    with open('words_dictionary.json', 'r') as f:
        dictionary = json.loads(f.read())
    return dictionary

def appearance_of_letter(words):
    frequency = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        frequency[letter] = 0
    for word in words:
        for letter in word:
            frequency[letter] += 1
    return frequency

def word_score(word, letter_frequency):
    score = 0
    temp = word

    for letter in set(word):
        score += letter_frequency[letter]
    return score


def order_by_score(words, letter_frequency):
    return sorted(words, key=lambda x: word_score(x, letter_frequency), reverse=True)

def has_double_letter(word):
    for i in range(len(word)-1):
        if word[i] == word[i+1]:
            return True
    return False

def has_repeated_letters(word):
    
    for i in range(len(word)-1):
        key = word[i]
        buffer = word
        buffer.replace(key,'')
        for j in range(len(buffer)):
            if buffer[j] == key:
                return True  
    return False  
         
