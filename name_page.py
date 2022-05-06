import qualities
import itertools
import math
from PyDictionary import PyDictionary
import json


dictionary = PyDictionary()  # instantiating dictionary module for present_in_dictionary fn
json_file = 'names_json.json'
user_input = input("Please enter your first name: ").lower()


def write_json(matter: dict):
    with open(json_file, 'w') as fwrite:
        json.dump(matter, fwrite)
    # print('Json file updated')


def read_json()->dict:
    with open(json_file, 'r') as fhand:
        json_data = json.load(fhand)
    return json_data


def get_permutations(name)->list:
    """Presents all unique combinations of the letters of a alphabetical string.
    Example: Ana, {'aa', 'na', 'an', 'ana', 'aan', 'naa'}"""
    if not name.isalpha():
        print('Please enter the name only in english letters!')
        return None
    all_permutations = []
    for length in range(3, len(name) + 1):
        formula = itertools.permutations(name, length)
        seq = [''.join(word) for word in formula]
        all_permutations += seq  # this will contain duplicates if the name has a given letter more than once
    all_unique_permutations = set(all_permutations)
    return list(all_unique_permutations)


def _word_list(file_name="words.txt")->list:
    """Presents an alphabetically ordered list of all scrabble words
    This resource features too many esoteric words which will be later weeded out"""
    all_words = []
    with open(file_name, 'r') as fhand:
        for word in fhand:
            word = word.rstrip()
            all_words += [word]
    return all_words


def _find_word(term: str, seq=_word_list())->bool:
    """This is a helper function for the _words_list fn
    which quickly confirms the presence of a word in a list of words, in this case the scrabble list"""
    if len(seq) < 2:
        if term == seq[0]:
            return True
        else:
            return False
    mid_way = math.ceil(len(seq)/2)
    mid_word = seq[mid_way]
    if term >= mid_word:
        seq = seq[mid_way:]
    else:
        seq = seq[: mid_way]
    return _find_word(term, seq)


def present_in_dictionary(terms: list):
    """Although it is slow (works online) it checks the presence of each word of the supplied list in the dictionary
    and removes rare, uncommon words"""
    for each in terms:
        if isinstance(dictionary.meaning(each, disable_errors=True), dict):
            yield each


def make_worthy_permutations():
    """This is a combining function for all sub-functions above"""
    name_permutations = get_permutations(user_input)
    scrabble_worthy = list(filter(_find_word, name_permutations))  # has several esoteric words
    # print("scrabble worthy", len(scrabble_worthy))
    dictionary_worthy_words = []
    print('The words made by recombining the letters of your name are: ')
    for ans in present_in_dictionary(scrabble_worthy):
        dictionary_worthy_words.append(ans)
        print(ans, end=' | ')
    print('\n')
    json_data = read_json()
    json_data.setdefault(user_input, dictionary_worthy_words)
    write_json(json_data)
    # print(dictionary_worthy_words)
    # print("dictionary worthy", len(dictionary_worthy_words))
    return dictionary_worthy_words


contents = read_json()
if user_input in contents.keys():
    final_list = contents.get(user_input)
    print('The words made by recombining the letters of your name are: \n')
    for parts in final_list:
        print(parts, end=' | ')
    print('\n')
else:
    final_list = make_worthy_permutations()


def read_number_file(number_file='number_name_mapping.json'):
    with open(number_file, 'r') as fhand:
        numbers_data = json.load(fhand)
    return numbers_data


data = read_number_file()  # this is a number-to-name mapping dictionary, where every key is a number but in string format

#==============================


def check_palindrome(seq: list)->list:
    palindromes = []
    for element in seq:
        if qualities.is_palindrome(element):
            palindromes.append(element)
    return palindromes


if check_palindrome(final_list):
    length = len(check_palindrome(final_list))
    print(f"Your name has {data.get(str(length))} palindrome words, (words that read the same backwards, eg.; noon): ", end=' ')
    for pali in check_palindrome(final_list):
        print(pali, end=', ')
    print('\n')


#==============================

def check_abecedarian(seq: list)->list:
    abecedarians = []
    for element in seq:
        if qualities.is_abecedarian(element):
            abecedarians.append(element)
    return abecedarians


if check_abecedarian(final_list):
    length = len(check_abecedarian(final_list))
    print(f"Your name also has {data.get(str(length))} abecedarian words, (words that conform to an alphabetical order, eg.; bell): ", end=' ')
    for abc in check_abecedarian(final_list):
        print(abc, end=', ')
    print('\n')


#==============================


def check_rev_pairs(seq: list)->list:
    reverse_pairs = []
    for each in range(len(seq)):
        for every in seq[each+1:]:
            if qualities.reverse_pair(seq[each], every):
                reverse_pairs.append((seq[each], every))
    return reverse_pairs


if check_rev_pairs(final_list):
    length = len(check_rev_pairs(final_list))
    print(f"This name even has {data.get(str(length))} reverse-pairs, (one word is the reverse of another): ", end=' ')
    for rev in check_rev_pairs(final_list):
        print(rev, end=', ')
    print('\n')


#==============================


def check_rotate_pairs(word_list: list)->list:
    """a program that reads a wordlist and finds all the rotate pairs."""
    rotate_pairs = []
    for word in word_list:
        for num in range(1, 26):
            twisted = qualities.word_rotator(word, num)
            if twisted in word_list:
                rotate_pairs.append((word, twisted, num))
    return rotate_pairs


if check_rotate_pairs(final_list):
    length = len(check_rotate_pairs(final_list))
    print(f'Even {data.get(str(length))} rotate pairs!')
    print("Two words are “rotate pairs” if you can rotate one of them and get the other")
    output = check_rotate_pairs(final_list)
    # sorted sorts the pars of words alphabetically, so the rotate-pair & its complementary rotate pair look similar
    # tuple prepares the sorted pair to be used as keys in rotate_pair_dict
    # setdefault ensures that a complement-tuple is not used as a key in the rotate_pair_dict
    rotate_pair_dict = {}
    for tup in output:
        rotate_pair_dict.setdefault(tuple(sorted(tup[:-1])), tup[-1])
    for k, v in rotate_pair_dict.items():
        print(f"'{k[0]}' rotated by {v} is '{k[1]}'")
    print('\n')


#==============================


def check_anagram_pairs(seq: list)->list:
    anagram_pairs = []
    for each in range(len(seq)):
        for every in seq[each+1:]:
            if qualities.is_anagram(seq[each], every):
                anagram_pairs.append((seq[each], every))
    return anagram_pairs


if check_anagram_pairs(final_list):
    length = len(check_anagram_pairs(final_list))
    print(f"The algorithm has even detected {data.get(str(length))} anagram-pairs in your name,\n(one word can be rearranged to spell the other, eg.; 'converse' & 'conserve'): ", end=' ')
    for ana in check_anagram_pairs(final_list):
        print(ana, end=', ')
    print('\n')


#==============================


def check_homophones(seq: list)->list:
    homophone_pairs = []
    for each in range(len(seq)):
        for every in seq[each+1:]:
            if qualities.are_homophones(seq[each], every):
                homophone_pairs.append((seq[each], every))
    return homophone_pairs


if check_homophones(final_list):
    length = len(check_homophones(final_list))
    print(f"And finally, we've found {data.get(str(length))} homophones,\n(i.e. two words that differ in spelling but not in their sounds, eg.; 'wrack' & 'rack'): ", end=' ')
    for hm in check_homophones(final_list):
        print(hm, end=', ')
    print('\n')


#============== E N D ================


