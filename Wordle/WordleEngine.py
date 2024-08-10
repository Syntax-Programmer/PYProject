from Dictionary import dictionary
from random import choice

def ValidityChecker(input_word:str)->bool:
    """Checks validity of a word."""
    if (
        len(input_word) != 5
        or not (input_word.isalpha())
        or input_word not in dictionary
    ):
        return True
def Logic(word_chosen: str, input_word: str) -> bool:
    """Main logic of the game."""
    word_chosen_array = list(word_chosen)
    if input_word == word_chosen:
        print("                                     You Got it!")
        return False
    for index, letter in enumerate(input_word):
        if word_chosen_array[index] == letter:
            print(
                f"                                        The letter {letter} belongs to the {index+1} st/nd/th place"
            )
            word_chosen_array.remove(letter)
            word_chosen_array.insert(index, "")
        elif letter in word_chosen_array:
            print(
                f"                                        The letter {letter} belongs in the word."
            )
            word_chosen_array.remove(letter)
            word_chosen_array.insert(index, "")
    return True


def Main() -> None:
    """Main game loop."""
    word_chosen = choice(dictionary)
    counter = 0
    while True: 
        input_word = input("Guess a word : ").strip().lower()
        if ValidityChecker(input_word=input_word):
            print("                                     Invalidity Detected")
            continue
        terminator = Logic(word_chosen=word_chosen, input_word=input_word)
        while terminator:
            input_word = input("Guess a word : ").strip().lower()
            if ValidityChecker(input_word=input_word):
                print("                                     Invalidity Detected")
                continue
            Logic(word_chosen=word_chosen, input_word=input_word)
            counter += 1
            if counter == 4:
                print("                                     Guesses are over, You Lost")
                print(f"                                        The word was : {word_chosen}")
                return
