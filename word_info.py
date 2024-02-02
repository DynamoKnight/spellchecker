'''
Nakul Kumar
Period 1
Spell Checker Project
'''
class WordInfo:
    '''
    The WordInfo object represents a misspelled word and its location in a file
    '''

    def __init__(self, misspelled, line, word_number, suggestions=None):
        self._misspelled = misspelled
        self._line = line
        self._word_number = word_number
        self._suggestions = suggestions

    # This is a required getter for Unit Tests to run
    def get_word(self):
        return self._misspelled

    # TODO: Add more getters & setters as necessary
    def get_line(self):
        return self._line

    def get_word_number(self):
        return self._word_number

    def get_suggestions(self):
        return self._suggestions

    def __str__(self):
        # TODO: update to "print" the information nicely
        return self._misspelled + ":\tline:\t" + str(self._line) + "  word:\t" + str(self._word_number)