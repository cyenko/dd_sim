import random
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *
from mpl_toolkits.mplot3d import Axes3D
import math
import sys
#Model settings
verbose = False
growthRate = .2 #reward parameters for waiting vs withdrawing early
initialInvestment = 10
maxWithdrawals = 70#the number of withdrawals until close
numTrials = 100
def runTrial(growthRate,maxWithdrawals,initialInvestment,verbose):
	rewards = [initialInvestment,initialInvestment*(1+growthRate),initialInvestment*(1+growthRate)*(1+growthRate)]
	rewardParameter = growthRate
	#the uniform parameter added to everyone's
	numWithdrawals = 0
	withdrawParameter = 0
	#risk parameter from people withdrawing
	#instantiate the people by using array format of [riskparam,withdraw,id,withdrawalAmt]
	peopleList = []
	for i in range(0,100):
		peopleList.append([random.normalvariate(.5,.5/3),0,i,0])
	numWithdrawals = 0
	for roundNum in range (0,3): #for 3 rounds
		if numWithdrawals < maxWithdrawals:
			if verbose:
				print "----ROUND " + str(roundNum) + "----"
			for person in peopleList:
				if numWithdrawals < maxWithdrawals:
					if not person[1] == 1: # Check if not withdrawn already
						num = random.random()
						currentRiskAversionParam = person[0]+withdrawParameter-rewardParameter
						if verbose:
							print "Risk parameter: " + str(currentRiskAversionParam) 
							print " - Individual: " + str(person[0])
							print " - WithdrawalParam: " + str(withdrawParameter)
							print " - rewardParam(-): " + str(rewardParameter)
						if num < currentRiskAversionParam: #then this person withdraws
							numWithdrawals = numWithdrawals + 1
							person[1]=1 #set flag to withdraw
							withdrawParameter = numWithdrawals/100
							person[3] = rewards[roundNum]
							if verbose:
								print "Person " + str(person[2]) + " withdrew " + str(person[3])
								if numWithdrawals == maxWithdrawals:
									print "THE BANK IS NOW CLOSED."
			if verbose:
				print "In round " + str(roundNum) + ", " + str(numWithdrawals) + " withdrawals."
				print "---------------"
	if verbose:
		aggOutput = 0
		for person in peopleList:
			aggOutput = aggOutput + person[3]
		print "AGGREGATE OUTPUT: " +str(aggOutput)

	if numWithdrawals < maxWithdrawals:
		if verbose:
			print "The bank did not close. Aggregate output:"
		return 0
	else:
		if verbose:
			print "The bank did close."
		return 1
#Vary the return parameter
x = []
y = []
for inc in range(0,100,1):
	growthParam = float(inc)/100
	closeSum = 0
	for i in range(0,numTrials):
		closeSum = closeSum + runTrial(growthParam,maxWithdrawals,initialInvestment,verbose)
	fractionClose = float(closeSum)/numTrials
	print str(growthParam) + " : " + str(fractionClose)
	#Store results for graph
	x.append(growthParam)
	y.append(fractionClose)
#plot the results
plt.plot(x,y)
plt.xlabel("Reward Parameter 'g'")
plt.ylabel("Bank closure % (out of 100 trials)")
plt.title("Reward Pameter vs. Bank Closure")
plt.show()
#Vary the bank closure parameter
x = []
y = []
for inc in range(0,100,1):
	growthParam = .1
	maxWithdrawals = inc
	closeSum = 0
	for i in range(0,numTrials):
		closeSum = closeSum + runTrial(growthParam,maxWithdrawals,initialInvestment,verbose)
	fractionClose = float(closeSum)/numTrials
	print str(growthParam) + " : " + str(fractionClose)
	#Store results for graph
	x.append(maxWithdrawals)
	y.append(fractionClose)
#plot the results
plt.plot(x,y)
plt.xlabel("Withdrawals until closure")
plt.ylabel("Bank closure % (out of 100 trials)")
plt.title("Max Withdrawals vs. Bank Closure")
plt.show()

#Finally vary both parameters to form a 3d plot
x = []
y = []
z = []
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

for inc in range(0,100,1): #vary maxWithdrawals
	print inc
	for inc2 in range(0,100,1): #vary growthParam
		growthParam = float(inc2)/100
		maxWithdrawals = inc
		closeSum = 0
		for i in range(0,numTrials):
			closeSum = closeSum + runTrial(growthParam,maxWithdrawals,initialInvestment,verbose)
		fractionClose = float(closeSum)/numTrials
		x.append(maxWithdrawals)
		y.append(growthParam)
		z.append(fractionClose)

ax.scatter(x,y,z,c='r',marker='o')
ax.set_xlabel('maxWithdrawals')
ax.set_ylabel('growthParam')
ax.set_zlabel('Probability of closing')
plt.show()

