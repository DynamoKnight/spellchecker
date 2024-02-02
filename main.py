'''
Nakul Kumar
Period 1
Spell Checker Project
'''
from spell_checker import SpellChecker
import os
import time

    
def main():
    # To time something, create a start time
    start = time.time()
    # do the work here.
    dictionary_path = input('Dictionary: ')
    if os.path.isfile(dictionary_path):
        sc = SpellChecker(dictionary_path)
        while True:
            file_path = input('Essay to check: ')
            if file_path == '':
                break
            if os.path.isfile(dictionary_path):
                sc.spell_check(file_path, True)
    # once complete, get the end time
    end = time.time()
    elapsed = end - start
    print(f'Time to spellcheck: {elapsed:.3f}')


if __name__ == '__main__':
    main()