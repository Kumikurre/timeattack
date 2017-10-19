import time
import numpy as np

correct = "aaaa"
incorrect = "xthisasdsadsaugabuga"

thestring = "aaaa"
corrects = []
falses = []

for x in range(10):
    start = time.perf_counter()
    if correct == thestring:
        pass
    end = time.perf_counter()
    print(end-start)
    corrects.append(end-start)

print("\n")

for y in range(10):
    start = time.perf_counter()
    if incorrect == thestring:
        pass
    end = time.perf_counter()
    print(end-start)
    falses.append(end-start)

print("\n")
print("\n")

print(np.mean(corrects))
print(np.mean(falses))
