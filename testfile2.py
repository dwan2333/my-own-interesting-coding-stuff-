print("Please enter the sentence that you want to translate:")
text = input(">").split()
import logging

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s', force = True)
for i in range(len(text)):
    logging.debug("word %s is being tested for isalpha", text[i])
    if not text[i].isalpha(): 
        logging.debug("word %s did not pass the test", text[i])
        left_stripped_character = ""
        for character in text[i]:
            logging.debug("character %s is being tested for isalpha", character)
            if not character.isalpha():
                left_stripped_character += text[i].lstrip(character)
                logging.debug("%s is being stripped out from the left side and added to the left striped characters",(character))

                
