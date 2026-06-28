import random 

guess = int(input("Guess a number between 0 to 20: "))

while (x := random.randint(0,21)) != guess:
    if guess < x:
        print("Your guess is smaller than the mysterious number")
    elif guess > x:
        print("Your guess is larger than the mysterious number")
    guess = int(input("Guess a number between 0 to 20: "))
    
print("You guessed the right number")
    