import string
import random

### DO NOT MODIFY THIS FUNCTION ###


def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

### DO NOT MODIFY THIS FUNCTION ###


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

### DO NOT MODIFY THIS FUNCTION ###


def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


WORDLIST_FILENAME = '/Users/dankreiger/Desktop/code/python_projekte/ps6/words.txt'


class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''

        # create empty dictionary
        shiftdict = {}

        # create list of tuples contains lowercase and matching uppercase alphabet letters i.e. [('a', 'A'), ('b', 'B')...]
        alphabet_list = list(
            zip(string.ascii_lowercase, string.ascii_uppercase))

        # creates a dictionary:
        # # keys: letters of alphabet (uppercase and lowercase) i.e. 'a', 'A', 'b', 'B'
        # # values encrypted letters of alphabet (shifted)
        for idx, letter in enumerate(alphabet_list):
            shiftIndex = idx + shift
            if(shiftIndex >= 26):
                shiftIndex = shiftIndex - 26
            shiftdict[letter[0]] = alphabet_list[shiftIndex][0]
            shiftdict[letter[1]] = alphabet_list[shiftIndex][1]

        return shiftdict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shiftdict = self.build_shift_dict(shift)
        new_message_text = ''

        for letter in self.message_text:
            if letter in shiftdict.keys():
                new_message_text += shiftdict[letter]
            else:
                new_message_text += letter

        return new_message_text


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less
        code is repeated
        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class

        Returns: a COPY of self.encrypting_dict
        '''
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift (ie. self.encrypting_dict and
        message_text_encrypted).

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        validTupleDecryptions = []
        for i in range(1, 27):
            words = []
            currentDecryption = self.apply_shift(26-i)
            for l in currentDecryption.split():
                if is_word(self.valid_words, l):
                    words.append(l)
            if(len(words) > 0):
                validTupleDecryptions.append(
                    tuple((len(words), 26-i, currentDecryption)))

        maxVal = 0
        chosenTuple = None
        if(len(validTupleDecryptions) > maxVal):
            for i in validTupleDecryptions:
                if(i[0] > maxVal):
                    maxVal = i[0]
                    chosenTuple = tuple((i[1], i[2]))

            return chosenTuple
        else:
            return 'No decryptions found'


# Example test case(PlaintextMessage)
testShift = 2

plaintext = PlaintextMessage('hello', testShift)
plaintext2 = PlaintextMessage('we are taking 6.00.1x', testShift)
print('')
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())
print('Expected Output: yg ctg vcmkpi 6.00.1z')
print('Actual Output: ', plaintext2.get_message_text_encrypted())


# Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq')
ciphertext = CiphertextMessage('yg ctg vcmkpi 6.00.1z')

print('')
print('Expected Output:', (26 - testShift, 'hello'))
print('Actual Output:', ciphertext.decrypt_message())


print('')
print('Expected Output:', (26 - testShift, 'we are taking 6.00.1x'))
print('Actual Output:', ciphertext.decrypt_message())


def decrypt_story():
    ctx = CiphertextMessage(get_story_string())
    return ctx.decrypt_message()


print(decrypt_story())
