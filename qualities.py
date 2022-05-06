import pronunciation_dictionary


def is_palindrome(word: str)-> bool:
    """example: rotavator"""
    return word.lower() == word[::-1].lower()

# print(is_palindrome('rotavator'))


def is_abecedarian(word):
    """is_abecedarian returns True if the letters in a word appear in alphabetical order (double letters are okay)."""
    counter = 0
    while counter < len(word) - 1:
        if word[counter] > word[counter+1]:
            return False
        counter += 1
    else:
        return True


# print(is_abecedarian('bell'))


def reverse_pair(w1, w2):
    """takes two words returns True one is the reverse of other"""
    return w1[::-1] == w2

# print(reverse_pair('pool', 'loop'))


# for tip, tup in list_of_pairs:
#     if reverse_pair(tip, tup):
#         print(tip, tup)


def _letter_rotator(letter, n):
    if letter.isupper():
        start = ord('A')
    elif letter.islower():
        start = ord('a')
    else:
        return letter

    c = ord(letter) - start
    i = (c + n) % 26 + start
    return chr(i)


def word_rotator(word, rotate_by):
    """takes a word and a number and rotates the word by that number.
    Two words are “rotate pairs” if you can rotate one of them and get the other"""
    rotated_word = ''
    for letter in word:
        rotated_word += _letter_rotator(letter, rotate_by)
    return rotated_word


def is_anagram(word1, word2):
    """Two words are anagrams if you can rearrange the letters from one to spell the other."""
    return sorted(word1) == sorted(word2)

# print(is_anagram('loop', 'pool'))


def are_homophones(w1, w2):
    """Takes two words and check if they're the same in their pronunciation"""
    a = pronunciation_dictionary.d.get(w1)
    b = pronunciation_dictionary.d.get(w2)
    if all((a, b)):  # ensures that both have a value from the pronunciation-dictionary
        return a == b
    else:
        return False



# print(are_homophones('seen', 'scene'))
# print(are_homophones('moan', 'mourn'))
# print(are_homophones('any', 'ani'))
