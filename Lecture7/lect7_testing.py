import random
import matplotlib as pylab
import matplotlib.pyplot as pyplot
import numpy as np

#set line width
pylab.rcParams['lines.linewidth'] = 4
#set font size for titles 
pylab.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
#set size of markers, e.g., circles representing points
#set numpoints for legend
pylab.rcParams['legend.numpoints'] = 1

class FairRoulette(object):
    def __init__(self):
        self.pockets = []
        for i in range(1,37):
            self.pockets.append(i)
        self.ball = None
        self.pocketOdds = len(self.pockets)-1
    def spin(self):
        self.ball = random.choice(self.pockets)
    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt*self.pocketOdds
        else:
            return -amt
    def __str__(self):
        return 'Fair Roulette'

def playRoulette(game, numSpins, pocket, bet, toPrint):
    totPocket = 0
    for i in range(numSpins):
        game.spin()
        totPocket += game.betPocket(pocket,bet)
    if toPrint:
        print (numSpins, 'spins of ', game)
        print ('Expected return betting ', pocket, '=' , str(100*totPocket/numSpins) + '%\n')
    return (totPocket/numSpins)

def findPocketReturn(game, numTrails, trailSize, toPrint):
    pocketReturns = []
    for t in range(numTrails):
        trailVals = playRoulette(game, trailSize, 2, 1, toPrint)
        pocketReturns.append(trailVals)
    return pocketReturns

def getMeanAndStd(X):
    mean = sum(X) /float(len(X))
    tot = 0.0
    for x in X:
        tot+= (x-mean)**2
    std = (tot/len(X))**0.5
    return mean, std

random.seed(1)
dist, numSamples = [], 1000000
for i in range(numSamples):
    dist.append(random.gauss(0, 100))

weights = [1/numSamples]*len(dist)

v = pyplot.hist(dist, bins = 100, weights = [1/numSamples]*len(dist))

print('Fraction within ~200 of mean =', sum(v[0][30:70]))

def gaussian(x, mu, sigma):
    factor1 = (1.0/(sigma*((2*np.pi)**0.5)))
    factor2 = np.e**-(((x-mu)**2)/(2*sigma**2))
    return factor1*factor2

xVals, yVals = [], []
mu, sigma = 0, 1
x = -4
while x <= 4:
    xVals.append(x)
    yVals.append(gaussian(x, mu, sigma))
    x += 0.05

pyplot.plot(xVals, yVals)
pyplot.title('Normal Distribution, mu = ' + str(mu) + ', sigma = ' + str(sigma))
#pyplot.show()

import scipy.integrate

def checkEmpirical(numTrials):
    for t in range(numTrials):
        mu = random.randint(-10,10)
        sigma = random.randint(1,10)
        print('For mu =', mu, 'and sigma =', sigma)
        for numStd in (1, 1.96, 3):
            area = scipy.integrate.quad(gaussian,mu-numStd*sigma,mu+numStd*sigma,(mu, sigma))[0]
            print(' Fraction within', numStd,'std =', round(area, 4))

checkEmpirical(3)

def plotMeans(numDice, numRolls, numBins, legend, color, style):
    means = []
    for i in range(numRolls//numDice):
        vals = 0
        for j in range(numDice):
            vals += 5*random.random() 
        means.append(vals/float(numDice))
    pyplot.hist(means, numBins, color = color, label = legend,weights = [1/len(means)]*len(means),hatch = style)
    pyplot.show()
    return getMeanAndStd(means)

mean, std = plotMeans(1, 1000000, 19, '1 die', 'b', '*')
print('Mean of rolling 1 die =', str(mean) + ',', 'Std =', std)
mean, std = plotMeans(50, 1000000, 19, 'Mean of 50 dice', 'r', '//')
print('Mean of rolling 50 dice =', str(mean) + ',', 'Std =', std)
#pyplot.title('Rolling Continuous Dice')
#pyplot.xlabel('Value')
#pyplot.ylabel('Probability')
#pyplot.legend()

numTrials = 1000
numSpins = 200
game = FairRoulette()
means = []
for i in range(numTrials):
    means.append(findPocketReturn(game, 1, numSpins,False)[0])

pyplot.hist(means, bins = 19,  weights = [1/len(means)]*len(means))
pyplot.show()

def throwNeedles(numNeedles):
    inCircle = 0
    for Needles in range(1, numNeedles+1, 1):
        x = random.random()
        y = random.random()
        if (x*x + y*y)**0.5 <= 1.0:
            inCircle+=1
    return 4*(inCircle/float(numNeedles))

def getEst(numNeedles, numTrails):
    estimates = []
    for t in range(numTrials):
        piGuess = throwNeedles(numNeedles)
        estimates.append(piGuess)
    sDev = np.std(estimates)
    curEst = sum(estimates)/len(estimates)
    print('Est. = ' + str(curEst) +\
          ', Std. dev. = ' + str(round(sDev, 6))\
          + ', Needles = ' + str(numNeedles))
    return (curEst, sDev)

def estPi(precision, numTrials):
    numNeedles = 1000
    sDev = precision
    while sDev >= precision/2:
        curEst, sDev = getEst(numNeedles,numTrials)
        numNeedles *= 2
    return curEst

random.seed(0)
estPi(0.005, 6)