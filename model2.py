import sys
import random
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np

def CreatePerson(t,d):

	risk = random.normalvariate(.6,(.2))
	while (risk<0):
		risk = random.normalvariate(.6,(.2))
	money = d
	ProbBankClosingToday = 0.5
	Withdrew = 0

	return [risk,money,ProbBankClosingToday,0]

def UpdatePeople(People,turn,CurrentWithdrawals,t,g):

	return People

def Decide (person,CurrentWithdrawals,t,g,turn,NumberOfPeople):

	ConfidenceOnBank = 0.2
	#print "\n \n Decision for person "+ str(turn)
	money=person[1]
	risk = person[0]
	#print risk
	UtilityNow = pow(money,risk)

	#print "UtilityNow: "+ str(UtilityNow)

	PeopleLeft = (NumberOfPeople-turn)
	#print PeopleLeft

	WithdrawalsLeft = (t - CurrentWithdrawals)
	#print WithdrawalsLeft

	ProbabilityBankClosingToday = float(WithdrawalsLeft)/PeopleLeft

	#print "ProbBankClosingToday: " + str(ProbabilityBankClosingToday)
	UtilityTomorrow = (1-0.5*ProbabilityBankClosingToday+ConfidenceOnBank)*pow(money*(1+g),risk)+(ProbabilityBankClosingToday)*0

	#print "UtilityTomorrow: " + str(UtilityTomorrow)

	if UtilityNow > UtilityTomorrow :
		return 1
	return 0

def runTrial(GrowthRate,ThresholdLimit,InitialDeposit,verbose):

	NumberOfPeople = 100

	CurrentWithdrawals = 0


	People = []
	#has multidimensional array
	#first row: risk factor, then 

	for i in range(NumberOfPeople):
		
		newPerson = CreatePerson(ThresholdLimit,InitialDeposit)
		People.append(newPerson)

	#print People

	for turn in range(NumberOfPeople):
		decision = Decide(People[turn],CurrentWithdrawals,ThresholdLimit,GrowthRate,turn,NumberOfPeople)
		if decision ==1 :
			CurrentWithdrawals +=1 
			#print "Person "+str(turn)+" withdrew money"
		#else:
			#print "Person "+str(turn)+" did NOT withdraw money"
		if CurrentWithdrawals>=ThresholdLimit:
			#print "------ Bank closed -----"
			return 1
		#People = UpdatePeople(People,turn,CurrentWithdrawals)
	return 0



def main2():
	x = []
	y = []
	numTrials=20
	initialInvestment=10
	verbose=0
	for inc in range(0,100,1):
		growthParam = float(inc)/100.00
		maxWithdrawals=40
		#growthParam = .2
		#maxWithdrawals = inc
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
	plt.xlabel("Withdrawals until closure")
	plt.ylabel("Bank closure % (out of 100 trials)")
	plt.title("Max Withdrawals vs. Bank Closure")
	plt.show()



def main():

	x = []
	y = []
	z = []
	fig = plt.figure()
	#ax = fig.add_subplot(111, projection='3d')

	# X=random.randrange(0,90,1)
	# Y=random.range(0,90,1)
	# Z=random.range(0,90,1)
	# for i in Z:
	# 	i=i/100.00


	for g in range(0,90,1):
		for inc in range(0,20,1):
			growthParam = float(g)/100.00
			maxWithdrawals = inc
			closeSum = 0
			initialInvestment=10
			verbose=0
			for i in range(0,40):
				closeSum = closeSum + runTrial(growthParam,maxWithdrawals,initialInvestment,verbose)
			fractionClose = float(closeSum)/40
			#Store results for graph
			x.append(growthParam)
			y.append(maxWithdrawals)
			z.append(fractionClose)
		print str(growthParam) + " : " + str(fractionClose)
	#	plot the results

	#ax.scatter(x,y,z, c='r', marker='o')
	plt.plot(x,z)
	plt.show()

	#ax.scatter(x,y,z,c=c,marker=m)
	#ax.plot_trisurf(x,y,z,cmap=cm.jet, linewidth=0.2)
	#plt.show()

if __name__=="__main__":
	main2()	