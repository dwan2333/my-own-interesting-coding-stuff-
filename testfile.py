import random 

guess = int(input("Guess a number between 0 to 20: "))
x = random.randint(0,21)

while  x != guess:
    if guess < x:
        print("Your guess is smaller than the mysterious number")
    else:
        print("Your guess is larger than the mysterious number")
    guess = int(input("Guess a number between 0 to 20: "))

print("You guessed the right number")
    