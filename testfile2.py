import random
state = ['open', 'close', 'you']

new = random.sample(state, k = 2).append('F')


print(new)
