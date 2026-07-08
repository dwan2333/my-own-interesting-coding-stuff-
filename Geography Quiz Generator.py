import random
from pathlib import Path

States_and_Captials = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona':
'Phoenix', 'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado':
'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida':
'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise',
'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines',
'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge',
'Maine': 'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston',
'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson',
'Missouri': 'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln',
'Nevada': 'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton',
'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh',
'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence',
'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee':
'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont':
'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 
'West Virginia':'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

# list out only states so that it is much eazier to apply for loops
States = [keys for keys, values in States_and_Captials.items()]

# select a file path to put the folder in 
print("please type in your choice of the quiz folder path: ")
quiz_folder = Path(input(">>> "))

# create a new directory named Quiz folder to store all the later quiz 
if quiz_folder.exists() != True:
    quiz_folder.mkdir()

# letters of mutiple choices that is to be used later 
choice = ['A', 'B', 'C', 'D']

# ask user how many quiz they want to print out 
while True:
    try:
        number_of_quiz = int(input("Please select the number of quizes that you want to create: "))
        if number_of_quiz > 0:
            break
        print('Please select a positive integer')
    except ValueError:
        print('Invalid input. Please enter a valid number.')


for i in range(number_of_quiz):

    folder_path = quiz_folder / f'Quiz {i+1}'
    answer_path = quiz_folder / f'Quiz answer {i+1}'

    with folder_path.open('w', encoding = 'UTF-8') as quiz: 

        # writing the title of the quiz
        quiz.write('Name: \n\n')
        quiz.write('Date: \n\n')
        quiz.write('Period: \n\n')
        quiz.write(f'State Capital Quiz (Form{i+1})'.center(80)+ '\n\n')

        for s in range(len(States)):

            quiz.write(f'{s+1}. What is the capital of {States[s]} ? \n')

            # creating the mutiple choice
            correct_answer = States_and_Captials.get(States[s])
            Capitals = [values for keys, values in States_and_Captials.items() if values != correct_answer]
            multiple_choice = random.sample(Capitals, k = 3) + [correct_answer]
            random.shuffle(multiple_choice)

            for x in range(4):
                quiz.write(f'    {choice[x]}. {multiple_choice[x]}\n')
                if multiple_choice[x] == correct_answer:
                    if answer_path.exists() == False:
                        with answer_path.open('w', encoding = 'UTF-8') as quiz_answer:
                            quiz_answer.write(f'{s+1}, {choice[x]}---{correct_answer}\n')
                    else: 
                        with answer_path.open('a', encoding = 'UTF-8') as quiz_answer:
                            quiz_answer.write(f'{s+1}, {choice[x]}---{correct_answer}\n')
            quiz.write("\n")

    random.shuffle(States)

       
                

        
                

                 
        

    








    
    