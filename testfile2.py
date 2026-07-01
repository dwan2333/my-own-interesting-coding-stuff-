print("Please enter the sentence that you want to translate:")
text = input(">").split()
vowels= ['a', 'e', 'i', 'o','u']
import logging

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s', force = True)
for i in range(len(text)):

    word =  text[i]
    logging.debug("word %s is being tested for isalpha", text[i])

    left_stripped_character = ""
    right_stripped_character = ""
    if not text[i].isalpha(): 
        logging.debug("word %s did not pass the test", text[i])
        for character in word:
            logging.debug("character %s is being tested for isalpha for left side", character)
            if not character.isalpha():
                left_stripped_character += character
                word = word.lstrip(character)
                logging.debug("%s is being stripped out from the left side and added to the left striped characters = %s" % (word,left_stripped_character))
            else:
                break
        
        logging.debug("%s is being test if it is all non alpha", word)
        if len(word) == 0:
            logging.debug("%s is is all non alpha", word)
            continue


        for character in word[::-1]:
            logging.debug("character %s is being tested for isalpha for right side", character)
            if not character.isalpha():
                right_stripped_character += character
                word = word.rstrip(character)
                logging.debug("%s is being stripped out from the left side and added to the left striped characters = %s" % (word,right_stripped_character))
            else:
                break

    title = word.istitle()
    logging.debug("%s is being check if it is titled %s" % (word, title))
    upper = word.isupper()
    logging.debug("%s is being check if it is titled %s" % (word, upper))

    word = word.lower()

    prefix_consonants = ""
    while len(word) > 0 and not word[0]in vowels:
        prefix_consonants += word[0]
        word = word[1:]
    logging.debug(f'{prefix_consonants} is being stripped out of {word}')

    if prefix_consonants != "": 
        word += prefix_consonants + 'ay'
    else:
        word += "yay"

    if title:
        word = word.title()
    elif upper:
        word = word.upper()

    text[i] = left_stripped_character + word + right_stripped_character

print(" ".join(text))




                
