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
numPeople = 100
yenko=1
def runTrial(growthRate,PanicFactor,maxWithdrawals,initialInvestment,verbose,rounds,graph):
	#rewards = [initialInvestment,initialInvestment*(1+growthRate),initialInvestment*((1+growthRate)**2)]
	if graph:
		plt.axhline(y=0.0, color='r')
	rewardParameter = growthRate

	#the uniform parameter added to everyone's
	numWithdrawals = 0
	withdrawParameter = 0
	BankPanic=0
	#risk parameter from people withdrawing
	#instantiate the people by using array format of [riskparam,withdraw,id,withdrawalAmt]
	peopleList = []
	BankMoney=[]
	BankCash=0
	theRisks=[]
	Conf=[]
	for i in range(0,numPeople):
		currentAccount=math.fabs(random.normalvariate(1000,200))
		BankCash=BankCash+currentAccount
		if yenko:
			peopleList.append([random.normalvariate(.5,.5/3),0,i,0,currentAccount])
		else:
			theRisk = random.normalvariate(1,.5/3)
			theRisks.append(theRisk)
			Confidence = random.normalvariate(0,.05)
			Conf.append(Confidence)
			peopleList.append([theRisk,0,i,0,currentAccount,Confidence])

	if graph:
		plt.plot(range(numPeople),Conf)
		plt.show()

	numWithdrawals = 0
	BankMoney.append(BankCash)
	for roundNum in range (0,rounds): #for 3 rounds
		if graph:
			plt.axvline(x=len(BankMoney), color='k')
		if roundNum>=1:
			BankCash=BankCash*((1+growthRate))
		if verbose:
			print "Bank starts round " + str(roundNum) + 'with $' + str(BankCash) 
		
		#reward=reward*(1+growthRate)
		if BankCash>0:
			if verbose:
				print "----ROUND " + str(roundNum) + "----"
			for person in peopleList:
				closed=0
				if BankCash > 0 :
					BankPanic=float(PanicFactor)*float(numWithdrawals)/numPeople
					#print "Bank Panic: " + str(BankPanic)
					BankMoney.append(BankCash)
					if not person[1] == 1: # Check if not withdrawn already
						person[4]=person[4]*(1+growthRate)
						num = random.random()-BankPanic
						currentRiskAversionParam = person[0]+withdrawParameter-rewardParameter
						#if verbose:
							#print "Risk parameter: " + str(currentRiskAversionParam) 
							#print " - Individual: " + str(person[0])
							#print " - WithdrawalParam: " + str(withdrawParameter)
							#print " - rewardParam(-): " + str(rewardParameter)
						if yenko:
							if num < currentRiskAversionParam: #then this person withdraws
								closed=0
								if BankCash < person[4]:
									if verbose:
										print "The bank is closed"
									closed=1
									break
								numWithdrawals = numWithdrawals + 1
								person[1]=1 #set flag to withdraw
								#withdrawParameter = numWithdrawals/100
								BankCash = BankCash-person[4]
								person[3] = person[4]
								if verbose:
									print "Person " + str(person[2]) + " withdrew " + str(person[3])
									# if numWithdrawals == maxWithdrawals:
									# 	print "THE BANK IS NOW CLOSED."
						else:
							UtilityNow = person[4]**(person[0])
							UtilityTomorrow = ((person[4]*(1+growthRate))**(person[0]))*(1-(BankPanic+person[5]))
							if verbose:
								print " \t \t RiskParam : " + str(person[0])
								print " \t \t Bank Confidence: " + str(person[5])
								print " \t \t Utility Now :" + str(UtilityNow)	
								print ' \t \t Utility Tomorrow: ' + str(UtilityTomorrow)
							if UtilityTomorrow < UtilityNow:
								numWithdrawals=numWithdrawals+1
								person[1]=1
								BankCash=BankCash-person[4]
								person[3]=person[4]
								if verbose:
									print "Person " + str(person[2]) + " withdrew " + str(person[3])

				else:
					closed=1
					break
					if verbose:
						print "THE BANK IS CLOSED"
			if verbose:
				print "In round " + str(roundNum) + ", " + str(numWithdrawals) + " withdrawals."
				print "---------------"
			

	if verbose:
		aggOutput = 0
		for person in peopleList:
			aggOutput = aggOutput + person[3]
		print "AGGREGATE OUTPUT: " +str(aggOutput)

	if graph==1:
		plt.plot(range(len(BankMoney)),BankMoney)

		plt.show()

	if closed==0:
		if verbose:
			print "The bank did not close."
		return 0
	else:
		if verbose:
			print "The bank did close."
		return 1

def Growth():
	x = []
	y = []
	PanicFactor=.9
	for inc in range(0,100,2):
		growthParam = float(inc)/100.00
		closeSum = 0
		maxWithdrawals=10000
		for i in range(0,numTrials):
			closeSum = closeSum + runTrial(growthParam,PanicFactor,maxWithdrawals,initialInvestment,0,3,0)
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

def Closure():
	#Vary the bank panic factor parameter
	x = []
	y = []
	growthParam=.4
	for inc in range(0,100,2):
		PanicFactor = float(inc)/100.00
		closeSum = 0
		maxWithdrawals=10000
		for i in range(0,numTrials):
			closeSum = closeSum + runTrial(growthParam,PanicFactor,maxWithdrawals,initialInvestment,0,3,0)
		fractionClose = float(closeSum)/numTrials
		print str(PanicFactor) + " : " + str(fractionClose)
		#Store results for graph
		x.append(PanicFactor)
		y.append(fractionClose)
	#plot the results
	plt.plot(x,y)
	plt.xlabel("Panic Factor ")
	plt.ylabel("Bank closure % (out of 100 trials)")
	plt.title("Reward Pameter vs. Bank Closure")
	plt.show()

def Trial3d():
	#Finally vary both parameters to form a 3d plot
	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')

	x = []
	y = []
	z = []
	Flags=0
	for inc in range(0,100,2): #vary maxWithdrawals
		print inc
		for inc2 in range(0,100,2): #vary growthParam
			growthParam = float(inc2)/100
			PanicFactor= float(inc)/100
			closeSum = 0
			for i in range(0,numTrials):
				flag=0
				added_trials = 0
				closeSum = closeSum + runTrial(growthParam,PanicFactor,maxWithdrawals,initialInvestment,0,3,0)
				added_trials = closeSum
				if i==20:
					if added_trials==0 or added_trials==20:
						flag=1
						fraction_close=float(added_trials)/20
						#print "Breaking "
						break
			if flag:
				fractionClose=fraction_close
				Flags+=1
			else:
				fractionClose = float(closeSum)/numTrials
			x.append(PanicFactor)
			y.append(growthParam)
			z.append(fractionClose)
		print "Flags: " + str(Flags)
	print Flags
	#trace1 = Scatter3d(x=x,y=y,z=z)
	#data = Data([trace1])
	#py.plot(data)

	ax.scatter(x,y,z,c='r',marker='o')
	ax.set_xlabel('Panic Factor')
	ax.set_ylabel('growth')
	ax.set_zlabel('Probability of closing')

	plt.show()

def main():

	if int(sys.argv[1])==1:
		Growth()
	elif int(sys.argv[1])==2:
		Closure()
	elif int(sys.argv[1])==3:
		Trial3d()
	elif int(sys.argv[1])==4:
		closing=0
		for i in range(1):
			closing += runTrial(float(sys.argv[2]),.3,10,10,1,3,1)

		print float(closing)/1

if __name__=="__main__":
	main()
