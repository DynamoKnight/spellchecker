'''
Nakul Kumar
Period 1
Spell Checker Project

Students must have a FAST implementation.
'''

import re
import string
from levenshtein import levenshtein_distance, lev_distance
from word_info import WordInfo
from itertools import product

class SpellChecker:
    '''
    The SpellChecker object parses through a text file to identify misspelled words
    It has several generators that are each a step in correcting a word
    It can suggest corrections by using the levenshtein distance
    '''

    def __init__(self, dictionary):
        # TODO: student will read and cache the words in the dictionary file
        with open(dictionary) as file:
            # A set is significantly faster when parsing
            self._dictionary = set(file.read().split())

    def spell_check(self, file_name, suggest = False):
        '''
        This will check the spelling of everyword in the file_name.
        It will return a list of WordInfo objects that describe the words misspelled.
        '''
        # The list of WordInfo objects
        misspelled_words = []
        with open(file_name) as file:
            lines = file.readlines()
            line_num = 0
            # enumerate returns a number for every iteration for the index
            for line_num, line in enumerate(lines, 1):
                # Splits the line by white space
                for word_num, word in enumerate(line.split(), 1):
                    if self.misspelled(word):
                        suggestions = None
                        if (suggest):
                            suggestions = self.suggest_corrections(normalize_token(word))
                        # Adds the WordInfo object into the list
                        word_info = WordInfo(normalize_token(word), line_num, word_num, suggestions)
                        misspelled_words.append(word_info)
                        # String representation will include line and word
                        print(word_info)
        # Prints the corrections in nice format
        if (suggest):
            print("\nSuggested Corrections:")
            for word_info in misspelled_words:
                print(word_info.get_word() + '\t\t--> ' + str(word_info.get_suggestions()))
        return misspelled_words

    def misspelled(self, word):
        '''
        This method MUST deal with hyphenated words.
        If any part of a hyphenated word is misspelled, then the whole word
        is misspelled.
        
        word   is not normalized and may or may not be hyphenated.
        return True if the word is misspelled, False if spelled correctly.
        '''
        # student must update to handle hyphens
        if '-' in word:
            # Recursion that looks at each word
            for split_word in word.split('-'):
                if self.misspelled(split_word):
                    return True
            # If it made it here, the the hypenated word is spelled correct
            return False
        # normalize the word
        word = normalize_token(word)
        # return True if misspelled
        return word not in self._dictionary

    def suggest_corrections(self, word):
        '''
        word : the misspelled word to find suggestions for
        
        Return a list of all the suggested words that share the same minimum
        distance from word using the levenshtein distance algorithm.
        '''
        corrections = []
        if ('-' in word):
            # A list of lists of the suggestions of each of the hypenated word
            hyphenated_suggestions = []
            for split_word in word.split('-'):
                split_suggestions = self.suggest_corrections(normalize_token(split_word))
                hyphenated_suggestions.append(split_suggestions)
            # itertools.product creates a list of tuples for every combination
            combinations = list(product(*hyphenated_suggestions))
            # Combines each tuple with a hyphen
            corrections = ['-'.join(combination) for combination in combinations]
        else:
            # Sets an intial variable that has to be from the set
            min = lev_distance(next(iter(self._dictionary)), word)
            for vocab in self._dictionary:
                # levenshtein_distance calculates the number of steps it takes to change a word
                lev = lev_distance(vocab, word)
                # Clears the list and stores closest values
                if lev < min:
                    min = lev
                    corrections = [vocab]
                # Adds only if the distance is the same
                elif lev == min:
                    corrections.append(vocab)
        return corrections
            
    def suggest_mismisspellings(self, word, max=6):
        '''
        word : the misspelled word to find suggestions for
        max : the max size of the list returned
        
        Return a list of all the suggested words by using the mis-misspelled
        approach. See instructions.
        '''
        word = normalize_token(word)
        corrections = set()
        # Checks every single combination to see if it is a word
        for i_word in self._insert_letters(word):
            for r_word in self._remove_letters(i_word):
                for s_word in self._swap_letters(r_word):
                    if s_word in self._dictionary:
                        corrections.add(s_word)
                        # Best to check only after a word is added
                        if len(corrections) >= max:
                            return list(corrections)
        return list(corrections)

    def _alphabets(self):
        '''
        Generates a letter from the alphabet
        '''
        # Unpacks string into list of characters
        letters = [*string.ascii_lowercase]
        for letter in letters:
            yield letter
                    
    def _insert_letters(self, word):
        '''
        This is a generator that will insert a-z at all location in the word
        '''
        yield word
        for i in range(0, len(word) + 1):
            for letter in self._alphabets():
                yield word[:i] + letter + word[i:]

    def _remove_letters(self, word):
        '''
        This is a generator that will remove each letter one at a time
        '''
        # student must implement this generator
        yield word
        for i in range(0, len(word)):
            yield word[:i] + word[i + 1:]

    # from 'ettiquitt' to 'etiquette' is: remove t, add e, swap i with e.
    def _swap_letters(self, word):
        '''
        This is a genertor that will replace each letter with a-z.
        This is sort of like a composition of insert & remove letters
        '''
        yield word
        for i in range(0, len(word)):
            for letter in self._alphabets():
                new_word = word[:i] + letter + word[i + 1:]
                # Wont yield the same word
                if new_word == word:
                    continue 
                yield new_word


def normalize_token(token):
    '''
    remove non-alphabetic characters using a regular expression
    don't forget to handle upper vs lowercase letters. Let's go lowercase.
    The hyphen is NOT removed. It remains.
    '''
    # student will NOT need to change
    return re.sub(r"[^A-Za-z\-]", "", token.lower())
