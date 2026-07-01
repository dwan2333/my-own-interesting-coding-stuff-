print("Please enter the sentence that you want to translate:")
text = input(">").split()
import logging

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s', force = True)
for i in range(len(text)):

    word =  text[i]
    logging.debug("word %s is being tested for isalpha", text[i])


    if not text[i].isalpha(): 
        logging.debug("word %s did not pass the test", text[i])
        left_stripped_character = ""
        right_stripped_character = ""
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
                right_stripped_chracter += character
                word = word.rstrip(character)
                logging.debug("%s is being stripped out from the left side and added to the left striped characters = %s" % (word,right_stripped_character))
            else:
                break

                
