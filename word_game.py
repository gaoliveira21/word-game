# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Gabriel José de Oliveira

import math
import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    word_points = 0
    lower_word = word.lower()

    for letter in lower_word:
        letter_point = SCRABBLE_LETTER_VALUES.get(letter, 0)
        word_points += letter_point

    wordlen = len(word)
    points = 7 * wordlen - 3 * (n - wordlen)

    if points < 1:
        points = 1

    return word_points * points

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for _ in range(hand[letter]):
            print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand

def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    lower_word = word.lower()
    new_hand = hand.copy()

    for letter in lower_word:
        letter_frequency = new_hand.get(letter, None)

        if letter_frequency is not None and letter_frequency > 0:
            new_hand[letter] = letter_frequency - 1

    return new_hand

def match_with_wildcard(word, word_in_list):
    """
    Returns True if word match with word_in_list.

        * this function assumes that both word and word_in_list have the same lenght.

        * word might contain a "*" char, which will be ignored if its position is the same as a vowels in word_in_list.

    word: string
    word_ins_list: string
    returns: boolean
    """
    for index in range(len(word)):
        letter = word[index]

        if letter == '*' and word_in_list[index] not in VOWELS:
            return False

        if letter != '*' and letter is not word_in_list[index]:
            return False

    return True

def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word_lower = word.lower()
    has_match = False

    for word_in_list in word_list:
        if len(word_in_list) == len(word):
            if match_with_wildcard(word_lower, word_in_list):
                has_match = True
                break

    if has_match == False:
        return False

    word_dict = get_frequency_dict(word_lower)

    for letter in word_lower:
        if letter == '*':
            continue

        letter_frequency_in_hand = hand.get(letter, None)

        if letter_frequency_in_hand is None:
            return False

        letter_frequency_in_word = word_dict.get(letter)

        if letter_frequency_in_word > letter_frequency_in_hand:
            return False

    return True

def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    lenght = 0

    for key in hand.keys():
        letter_frequency = hand.get(key, 0)
        lenght += letter_frequency

    return lenght

def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
    """
    current_hand = hand.copy()
    total_hand_score = 0

    while True:
        print('Current hand:', end=" ")
        display_hand(current_hand)

        word = input('Enter word, or "!!" to indicate that you are finished: ')

        if word == '!!':
            break

        if is_valid_word(word, current_hand, word_list):
            points = get_word_score(word, calculate_handlen(current_hand))
            total_hand_score += points

            print(f'"{word}" earned {points} points. Total: {total_hand_score} points')
        else:
            print('That is not a valid word. Please choose another word.')

        current_hand = update_hand(current_hand, word)

        if calculate_handlen(current_hand) <= 0:
            print('Ran out of letters')
            break

    return total_hand_score

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()
    letters = hand.keys()
    letter_frequency = hand.get(letter, 0)

    while True:
        new_letter = random.choice(VOWELS + CONSONANTS)

        if(new_letter not in letters):
            del new_hand[letter]
            new_hand[new_letter] = letter_frequency
            break

    return new_hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    number_of_hands = int(input('Enter total number of hands: '))
    remaining_hands = number_of_hands
    total_score = 0
    should_replay_hand = False

    while remaining_hands > 0:
        if should_replay_hand == False:
            hand = deal_hand(HAND_SIZE)

        print("Current hand:", end=" ")
        display_hand(hand)

        if should_replay_hand == False:
            should_substitute = input('Would you like to substitute a letter? ')

            if should_substitute != "no":
                letter_to_replace = input('Which letter would you like to replace: ')
                hand = substitute_hand(hand, letter_to_replace)

        print()
        hand_score = play_hand(hand, word_list)
        total_score += hand_score
        remaining_hands -= 1

        print(f'Total score for this hand: {hand_score}')
        print('----------')

        if remaining_hands > 0:
            should_replay_hand = input('Would you like to replay the hand? ') == 'yes'

    print(f'Total score over all hands: {total_score}')



#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
