print("Please enter the sentence that you want to translate:")
text = str(input(">").split())
import logging

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s', force = True)
logging.debug('Test')
for word in range(len(text)):
    
    if not word.isalpha(): 
        for character in word:
            if not character.isaplpha():
                print()
