import os
import sys
import random
from typing import List # For parameter type hints of Lists of strings.
from sty import fg, bg, ef, rs # For color coding.

OS_IS_WINDOWS = (sys.platform == "win32")

#Resets
CRESET = fg.rs # Style reset
SRESET = ef.rs # Color reset
RESET = CRESET + SRESET # Both resets at once
#Colors
RED = fg.red
BLUE = fg.blue
GREEN = fg.green
YELLOW = fg.yellow
MAGENTA = fg.magenta
CYAN = fg.cyan
# Styles
BOLD = ef.bold
ITALIC = ef.italic
UNDERL = ef.underl

def set_letters(letters_file: str, letter_list: List[str]):
    with open(letters_file, "r") as file:
        for line in file: # This assumes there aren't any extra empty lines in the file.
            letter = line.split()[0] # To ignore \n after each letter.
            letter = letter.lower()
            letter_list.append(letter) # This will directly modify the passed in letter_list (as in passing by reference).

def set_frames(frames_file: str, frame_exit: str, frame_list: List[str]):
    buffer = "" # We need a buffer since we are going to append multiple lines at once.
    with open(frames_file, "r") as file:
        for line in file:
            if line.strip() == frame_exit: # This assumes the frame end char is on its own line.
                buffer = buffer.removesuffix("\n") # Remove the \n from last line.
                frame_list.append(buffer) # This will directly modify the passed in frame_list.
                buffer = "" # Reset the buffer
            else:
                buffer += line

def get_rand_word(words_file: str) -> str:
    with open(words_file, "r") as file:
        words = file.readlines() # Read all the words into a list.
        word = random.choice(words).strip() # Pick a random word with the trailing \n removed.
        return word # The word at that random index of the word bank is returned to the caller.

def clear_screen():
    if OS_IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

def title(color: str = RESET, end: str = "\n"):
    print(color + "***************************")
    print(" H   A   N   G   M   A   N")
    print("***************************" + RESET, end = end) # If end parameter doesn't include \n, it will not \n.

def menu() -> bool:
    while (True):
        clear_screen()
        title(BLUE + BOLD)
        print(f"\n{BOLD}{MAGENTA}Welcome to hangman. You have two options:")
        print(f"\n1 - {SRESET}{YELLOW}Play")
        print(f"{BOLD}{MAGENTA}2 - {SRESET}{YELLOW}Quit")

        answer = input(f"\n{SRESET}{CYAN}Please choose an option. >>> {CRESET}")
        # Allow for both 1 & 2 as answers and any variation of "Play" & "Quit".
        if (answer != "1" and answer != "2" and answer.lower() != "play" and answer != "quit"): # Handle invalid inputs.
            print(f"\n{RED}Please input either 1 or 2, or type {BOLD}{CRESET}\"Play\"{SRESET}{RED} or {BOLD}{CRESET}\"Quit\"")
            input(f"{SRESET}{CYAN}Press any key to continue >>> {CRESET}")
            continue

        elif (answer == "1" or answer.lower() == "play"):
            return True
        
        elif (answer == "2" or answer.lower() == "quit"):
            print(f"{BOLD}{MAGENTA}\nGoodbye!{RESET}")
            return False

# This function checks if all the letters in an input string are in the allowed letter list.
def input_valid(input: str, allowed_chars: List[str]) -> bool:
    return all(char in allowed_chars for char in input) # Assume the for loop executes first.

# This function checks if a guessed letter is part of the word.
def validate_guess(guess: str, word: str) -> bool:
    for letter in word:
        if (guess.lower() == letter.lower()):
            return True        
    return False

# Display the frame at the specified index with the option to change the end parameter of print().
def show_frame(index: int, frame_list: List[str], color: str = RESET, end: str = "\n"):
    print(color + frame_list[index] + RESET, end = end) # If end parameter doesn't include \n, it will not \n.

# Return a string of the word with all letters hidden except those which have been correctly guessed.
def hidden_word(word: str, correct_guessed_letters: str, hidden_symbol: str = "_", letter_color: str = RESET) -> str:
    result = ""
    for letter in word:
        char_found = False
        for char in correct_guessed_letters:
            if (char == letter):
                char_found = True
                result += letter_color + char + " " + RESET
                break
        if (char_found != True):
            result += hidden_symbol + " " + RESET
    return result

def get_guessed_letters(guessed_letters: List[str], seperator: str = "|", letter_color: str = RESET) -> str:
    result = ""
    counter = 0
    for letter in guessed_letters:
        if (counter == len(guessed_letters) - 1): # The last letter should not have a seperator after it.
            result += letter_color + letter + RESET
        else:
            result += letter_color + letter + " " + RESET + seperator + " " + RESET
        counter += 1
    return result

# Return whether or not a letter has already been guessed.
def already_guessed(char: str, guessed_letters: List[str]) -> bool:
    for letter in guessed_letters:
        if (char == letter):
            return True
    return False

def play_game(words_file: str, allowed_letters: List[str], frame_list: List[str], allowed_guesses: int = 6):
    guess = ""
    guesses = 0
    guessed_letters = []
    correct_guessed_letters = []
    word = get_rand_word(words_file) # Set random word.

    while (guesses < allowed_guesses):
        incorrect_guesses = len(guessed_letters) - len(correct_guessed_letters)
        frame_index = incorrect_guesses

        clear_screen()
        title(BLUE + BOLD, end = "\n\n")
        show_frame(frame_index, frame_list, BOLD + GREEN) # Show the hangman graphic.
        print("\n" + hidden_word(word, correct_guessed_letters, BOLD + "_", GREEN + BOLD + ITALIC)) # Show the word with the missing letters.
        # Show the previously guessed letters if there are any.
        if (guesses > 0): print(f"\n{BOLD}{MAGENTA}Guessed Letters: {SRESET}" + get_guessed_letters(guessed_letters, BOLD + MAGENTA + "|", YELLOW + ITALIC))
        print(f"\n{BOLD}{MAGENTA}Guesses Left: {SRESET}{YELLOW}{ITALIC}{str(allowed_guesses - guesses)}{RESET}") # Show how many wrong guesses left.

        guess = input(f"{CYAN}\nWhat is your guess? >>> {CRESET}")

        # Check whether it is a valid new guess and is one letter.
        if ((input_valid(guess.lower(), allowed_letters) == True) and (len(guess) == 1) and (already_guessed(guess, guessed_letters) == False)):
            
            # The letter is found in the word.
            if (validate_guess(guess, word) == True):
                print(f"\n{GREEN}{BOLD}Congratulations! {SRESET}You guessed one of the letters.")
                guessed_letters.append(guess)
                correct_guessed_letters.append(guess)
                input(f"{CYAN}Press any key to continue. >>> {CRESET}")

                # There are no hidden symbols therefore the entire word matches. They won, and the game ends.
                if all(letter in correct_guessed_letters for letter in word): # Treat as if the for loop executes first. 
                    print(f"\n{GREEN}{BOLD}Congratulations! {SRESET}You successfully guessed the word.")
                    input(f"{CYAN}Press any key to continue. >>> {CRESET}")
                    return
            else: # The letter is not found in the word.
                print(f"{YELLOW}{BOLD}\n" + guess, f"{RED}was not part of the word.{SRESET}")
                input(f"{CYAN}Press any key to continue. >>> {CRESET}")
                guessed_letters.append(guess)
                guesses += 1

        # It's a valid input and is one letter, but they already guessed the letter (regardless of whether or not it was correct).
        elif((input_valid(guess.lower(), allowed_letters) == True) and (len(guess) == 1) and (already_guessed(guess, guessed_letters) == True)):
            print(f"\n{YELLOW}{BOLD}You already guessed that letter.{SRESET}")
            input(f"{CYAN}Press any key to continue. >>> {CRESET}")

        else: # It's not a valid input and/or it's longer than one letter.    
            print(f"\n{RED}{BOLD}Please input a valid letter.{SRESET}")
            input(f"{CYAN}Press any key to continue. >>> {CRESET}")

    # The while loop broke which means they used all their allowed_guesses and still didn't guess the word.
    frame_index = allowed_guesses # The last frame.

    clear_screen()
    title(BLUE + BOLD, end = "\n\n")
    show_frame(frame_index, frame_list, BOLD + RED)
    print("\n" + hidden_word(word, correct_guessed_letters, RED + BOLD + "_", GREEN + BOLD + ITALIC)) # Show the letters they did get right and in what positions.
    print(f"{BOLD}{MAGENTA}Guessed Letters: {SRESET}" + get_guessed_letters(guessed_letters, BOLD + MAGENTA + "|", YELLOW + ITALIC)) # Show all the letters they tried.
    print(f"\n{BOLD}{RED}You were hanged on account of terrible word guessing ability.")
    print(f"{MAGENTA}The word was: {YELLOW}{ITALIC}{UNDERL}{word}{RESET}") # Show them the word.
    print(f"{MAGENTA}Better luck next time?") # Tease.
    input(f"\n{CYAN}Press any key to continue. >>> {CRESET}")
    
def main():
    letters_file = "Hangman/letters.txt"
    letters = []
    set_letters(letters_file, letters)

    frames_file = "Hangman/frames.txt"
    frames = []
    set_frames(frames_file, "#", frames)

    words_file = "Hangman/words.txt"
    
    while (True): # The game will go on indefinitely until they choose to quit.
        if (menu() == False): # Menu returns False if they choose to quit. Otherwise the game starts.
            break
        play_game(words_file, letters, frames)

    sys.exit()

if __name__ == "__main__":
    main()
