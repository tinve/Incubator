
# coding: utf-8

# In[34]:

from __future__ import division

import numpy as np
import random
import time

from math import factorial


# # Auxiliary functions

# In[35]:

def step_combinations((x, y), n):
    combinations = []
    for i in range(n + 1):
        j = i - x
        if j >= 0:
            for k in range(n + 1 - i - j):
                if k - (n - i - j - k) == y:
                    combinations.append((i, j, k, n - i - j - k))
    return combinations


# In[36]:

def combination_multiplicity((i, j, k, l)):
    return factorial(i + j + k + l) / (factorial(i) * factorial(j) * factorial(k) * factorial(l))


# In[37]:

def path_probability((x, y), n):
    # given the end point (x, y), returns probability of ending at that point in exactly n steps
    
    multiplicity = 0
    for combination in step_combinations((x, y), n):
        multiplicity = multiplicity + combination_multiplicity(combination)
    return multiplicity / 4**n


# In[38]:

def step((x, y), choice):
    if choice == 0:
        return (x + 1, y)
    elif choice == 1:
        return (x - 1, y)
    elif choice == 2:
        return (x, y + 1)
    else:
        return (x, y - 1)


# # Question 1

# In[39]:

r = 3
n = 10

# points that are _closer_ than r to the origin
points = []
for i in range(-r, r + 1):
    for j in range(-r, r + 1):
        if i**2 + j**2 < r**2:
            points.append((i,j))


# In[40]:

# probability of ending in one of these points
probability = 0
for point in points:
    probability = probability + path_probability(point, n)

# we need complementary probability
probability = 1 - probability
print probability


# In[41]:

# same with brute force
start_time = time.time()

outside = 0

for i in range(4**n):
    coord = (0, 0)
    directions = np.binary_repr(i, width = 2*n)
    for i in range(0, len(directions) - 1, 2):
        choice = int(directions[i : i + 2], 2)
        coord = step(coord, choice)
    if coord[0]**2 + coord[1]**2 >= r**2:
        outside = outside + 1
        
print("--- %s seconds ---" % (time.time() - start_time))

# round-up error from factorials in previous method?
outside / 4**n


# In[42]:

# same with simulation

n_walks = 10**6
outside = 0
random.seed(42)

start_time = time.time()

for w in range(n_walks):
    coord = (0, 0)
    for s in range(n):
        choice = random.randint(0, 3)
        coord = step(coord, choice)
    if coord[0]**2 + coord[1]**2 >= r**2:
        outside = outside + 1
        
print("--- %s seconds ---" % (time.time() - start_time))

# Only 2 digits are reliable
outside / n_walks


# # Question 2

# In[43]:

r = 10
n = 60

# points that are _closer than r to the origin
points = []
for i in range(-r, r + 1):
    for j in range(-r, r + 1):
        if i**2 + j**2 < r**2:
            points.append((i,j))


# In[44]:

# probability of ending in one of these points
probability = 0
for point in points:
    probability = probability + path_probability(point, n)

# we need complementary probability
probability = 1 - probability
print probability


# In[45]:

# brute force unfeasible at this n, so:
# same with simulation

n_walks = 10**6
outside = 0
random.seed(42)

start_time = time.time()

for w in range(n_walks):
    coord = (0, 0)
    for s in range(n):
        choice = random.randint(0, 3)
        coord = step(coord, choice)
    if coord[0]**2 + coord[1]**2 >= r**2:
        outside = outside + 1
        
print("--- %s seconds ---" % (time.time() - start_time))

# only three digits reliable
outside / n_walks


# # Question 3

# In[46]:

r = 3
n = 10

# brute force
start_time = time.time()

outside = 0

for i in range(4**n):
    coord = (0, 0)
    directions = np.binary_repr(i, width = 2*n)
    for i in range(0, len(directions) - 1, 2):
        choice = int(directions[i : i + 2], 2)
        coord = step(coord, choice)
        if coord[0]**2 + coord[1]**2 >= r**2:
            outside = outside + 1
            break
        
print("--- %s seconds ---" % (time.time() - start_time))

outside / 4**n


# In[47]:

# and simulation

n_walks = 10**6
outside = 0
random.seed(42)

start_time = time.time()

for w in range(n_walks):
    coord = (0, 0)
    for s in range(n):
        choice = random.randint(0, 3)
        coord = step(coord, choice)
        if coord[0]**2 + coord[1]**2 >= r**2:
            outside = outside + 1
            break
        
print("--- %s seconds ---" % (time.time() - start_time))

# Only 2 digits are reliable
outside / n_walks


# # Question 4

# In[49]:

# tried several approaches to solve analytically, didn't work out
# and brute force is unfeasible, 
# so here is simulation

r = 10
n = 60

n_walks = 10**6
outside = 0
random.seed(42)

start_time = time.time()

for w in range(n_walks):
    coord = (0, 0)
    for s in range(n):
        choice = random.randint(0, 3)
        coord = step(coord, choice)
        if coord[0]**2 + coord[1]**2 >= r**2:
            outside = outside + 1
            break

print("--- %s seconds ---" % (time.time() - start_time))

# bad approximation, but better than nothing
outside / n_walks


# # Question 5

# In[ ]:

def step(x, choice):
    if choice == 0:
        return x + 1
    elif choice == 1:
        return x - 1
    else:
        return x


# In[71]:

n = 10

# brute force
start_time = time.time()

match = 0

for i in range(4**n):
    west = 0
    east = 0
    coord = 0
    directions = np.binary_repr(i, width = 2*n)
    for i in range(0, len(directions) - 1, 2):
        choice = int(directions[i : i + 2], 2)
        coord = step_1d(coord, choice)
        if coord >= 2:
            east = 1
    if coord <= -2:
        west = 1
    match = match + east * west
        
print("--- %s seconds ---" % (time.time() - start_time))

match / 4**n


# # Question 6

# In[55]:

# simulation

n = 30

n_walks = 10**6
match = 0
random.seed(42)

start_time = time.time()

for w in range(n_walks):
    west = 0
    east = 0
    coord = 0
    for s in range(n):
        choice = random.randint(0, 3)
        coord = step_1d(coord, choice)
        if coord >= 2:
            east = 1
    if coord <= -2:
        west = 1
    match = match + east * west

print("--- %s seconds ---" % (time.time() - start_time))

# bad approximation, but better than nothing
match / n_walks


# # Question 7

# In[79]:

# simulation

r = 10

n_walks = 10**6
total_length = 0
random.seed(42)

start_time = time.time()

for w in range(n_walks):
    coord = (0, 0)
    while coord[0]**2 + coord[1]**2 < r**2:
        choice = random.randint(0, 3)
        coord = step(coord, choice)
        total_length = total_length + 1

print("--- %s seconds ---" % (time.time() - start_time))

# bad approximation, but better than nothing
total_length / n_walks


# # Question 8

# In[83]:

# simulation

r = 60

n_walks = 10**4
total_length = 0
random.seed(42)

start_time = time.time()

for w in range(n_walks):
    coord = (0, 0)
    while coord[0]**2 + coord[1]**2 < r**2:
        choice = random.randint(0, 3)
        coord = step(coord, choice)
        total_length = total_length + 1

print("--- %s seconds ---" % (time.time() - start_time))

# bad approximation, but better than nothing
total_length / n_walks


# In[ ]:



