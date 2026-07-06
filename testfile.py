import random
from pathlib import Path

capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona':
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



quiz_folder = Path("D:/ Quiz folder")

# create a new directory named Quiz folder to store all the later quiz 
if quiz_folder.exists() != True:
    quiz_folder.mkdir()

# ask user how many quiz they want to print out 
while (number_of_quiz := int(input("Please select the number of quizes that you want to create: "))) < 0:
    print('Please select a positive integer')


for i in range(number_of_quiz):
    folder_path = quiz_folder / f'Quiz {i+1}'
    with folder_path.open('w', encoding = 'UTF-8') as quiz: 

        # writing the title of the quiz
        quiz.write('Name: \n\n')
        quiz.write('Date: \n\n')
        quiz.write('Period: \n\n')
        quiz.write(f'State Capital Quiz (Form{i+1})\n\n'.center(80))

        states = [states for states, capitals in capitals.items()]
        random.shuffle(states)
        print(states)

    








    
    