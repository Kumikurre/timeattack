import time
import numpy as np

correct = "aaaa"
incorrect = "xthisasdsadsaugabuga"

thestring = "aaaa"
corrects = []
falses = []

for x in range(1000000):
    start = time.perf_counter()
    if correct == thestring:
        pass
    end = time.perf_counter()
    corrects.append(end-start)

for y in range(1000000):
    start = time.perf_counter()
    if incorrect == thestring:
        pass
    end = time.perf_counter()
    falses.append(end-start)

print("\n")
print('correct comparison:')
print(np.mean(corrects))
print(np.amin(corrects))
print('false comparison:')
print(np.mean(falses))
print(np.amax(falses))
