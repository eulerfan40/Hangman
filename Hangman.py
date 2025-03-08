import os
import sys
import random

os_is_windows = (sys.platform == 'win32')

words_file = "Hangman/words.txt"
word = ""
allowed_guesses = 5
guesses = 0
guessed_letters = []
correct_guessed_letters = []
letters = ["a", "b", "c", "d", "e", "f", "g",
           "h", "i", "j", "k", "l", "m", "n", "o", "p",
           "q", "r", "s", "t", "u", "v", 
           "w", "x", "y", "z"]

def horizontal_line() -> str:
    result = "***************************"
    return result

def title():
    print(horizontal_line())
    print(" H   A   N   G   M   A   N")
    print(horizontal_line())

def clear_screen():
    if os_is_windows:
        os.system("cls")
    else:
        os.system("clear")

def play_option() -> bool:
    while (True):
        clear_screen()
        title()
        print("\nWelcome to hangman. You have two options:")
        print("1 - Play")
        print("2 - Quit")
        answer = str(input("Please choose an option. >>> "))
        if ((answer != "1") and (answer != "2")):
            print("\nPlease input an integer value: Either 1 or 2.")
            input("Press any key to continue >>> ")
        elif (answer == "1"):
            return True
        elif (answer == "2"):
            return False

def check_input(input: str) -> bool:
    for letter in input:
        letter_found = False
        for char in letters:
            if ((not letter_found) and (letter == char.lower())):
                letter_found = True
                break
        if (not letter_found):
            return False
    return True

def set_word():
    global words_file
    global word    

    with open(words_file, "r") as file:
        words = file.readlines()
        random_word_index = random.randrange(0, len(words) - 1)
        word = words[random_word_index]

def validate_guess(char: str) -> bool:

    for letter in word:
        if (char.lower() == letter.lower()):
            return True
        
    return False

def word_missing_chars() -> str:
    result = ""

    for letter in word:
        char_found = False
        for char in correct_guessed_letters:
            if (char == letter):
                char_found = True
                result += char + " "
                break
        if (char_found != True):
            result += "_ "

    return result

def get_guessed_letters() -> str:
    result = ""
    counter = 0
    for letter in guessed_letters:
        if (counter == len(guessed_letters) - 1):
            result += letter
        else:
            result += letter + " | "
        counter += 1
    return result

def already_guessed(char: str) -> bool:
    for letter in guessed_letters:
        if (char == letter):
            return True
    return False

def game_loop():
    guess = ""
    global guesses

    while (guesses < allowed_guesses):
        clear_screen()
        title()
        print("\n" + word_missing_chars())
        print("Guessed Letters: " + get_guessed_letters())
        print("Guesses Left: " + str(allowed_guesses - guesses))

        guess = str(input("\nWhat is your guess? >>> "))

        if ((check_input(guess) == True) and (len(guess) == 1) and (already_guessed(guess) == False)):

            if (validate_guess(guess) == True):
                print("\nCongratulations! You guessed one of the letters.")
                guessed_letters.append(guess)
                correct_guessed_letters.append(guess)
                input("Press any key to continue. >>> ")
                if(word_missing_chars().replace(" ", "") == word):
                    print("\nCongratulations! You have successfully guessed the word.")
                    input("Press any key to continue. >>> ")
                    return
            else:
                print("\n" + guess, "was not part of the word.")
                input("Press any key to continue. >>> ")
                guessed_letters.append(guess)
                guesses += 1

        elif((check_input(guess) == True) and (len(guess) == 1) and (already_guessed(guess) == True)):
            print("\nYou already guessed that letter.")
            input("Press any key to continue. >>> ")

        else:            
            print("\nPlease input a valid letter.")
            input("Press any key to continue. >>> ")
    
    print("\nYou were unable to guess the word.")
    print("The word was: " + word)
    print("Better luck next time!")
    input("\nPress any key to continue. >>> ")
    
def main():
    while (True):
        if (play_option() == False):
            sys.exit()
        set_word()
        game_loop()

if __name__ == "__main__":
    main()
