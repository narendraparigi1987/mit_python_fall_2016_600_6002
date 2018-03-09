#-*- coding: utf-8 -*-
# test case 1
import random

#random.seed(0)

def rollDie():
    """returns a random int between 1 and 6"""
    return random.choice([1,2,3,4,5,6])

def testRoll(n):
    result = ''
    for i in range(n):
        result = result + str(rollDie())
    print (result)

#testRoll(6)

def runSim(goal, numtrails, txt):
    total = 0
    
    for i in range(numtrails):
        result = ''
        for j in range(len(goal)):
            result = result + str(rollDie())
        if result == goal:
            total+=1
    
    print ('Actual probability of', txt, '=',
          round(1/(6**len(goal)), 8))
    
    estProbability = round(total/numtrails,8)
    
    print ('Estimated probability of', txt, '=',
          round(estProbability, 8))

#runSim('11111', 1000000, '11111')

def sameDate(numPeople,numSame):
    possibleDates =  range(366)
    birthDays = [0] * 366
    for i in range(numPeople):
        birthDate = random.choice(possibleDates)
        birthDays[birthDate] += 1
    return max(birthDays) > numSame

def birthdayProb(numPeople, numSame, numTrials):
    numHits = 0
    for i in range(numTrials):
        if sameDate(numPeople,numSame):
            numHits+=1
    return numHits/numTrials

import math

for numPeople in [10,20,40,100]:
    print('For', numPeople,
          'est. prob. of a shared birthday is',
          birthdayProb(numPeople, 2, 10000))
    numerator = math.factorial(366)
    denom = (366**numPeople)*math.factorial(366-numPeople)
    print('Actual prob. for N = 100 =',
          1 - numerator/denom)
