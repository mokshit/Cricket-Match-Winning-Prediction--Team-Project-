import csv
import pandas as pd
from math_plot import plot_graph_teamA,plot_graph_teamB,plot_graph_teamA_and_teamB
from datetime import datetime
#taking input from the user
'''
team1=input("enter team1")
team2=input("enter team2")
'''
teamA='India'
teamB='Pakistan'

df=pd.read_csv('OutputOfAll.csv')

df=df.loc[((df['TeamA']==teamA) & (df['TeamB']==teamB)) | ((df['TeamA']==teamB) & (df['TeamB']==teamA))]
df=df.sort_values(by='Date', ascending=[1])

matchID_list=df['MatchID'].tolist()
toss_decision_list=df['Toss_Decision'].tolist()
dates_list=df['Date'].tolist()

teamA_net_rates=[]
teamB_net_rates=[]

match_id_no=0

for matchId in matchID_list:
	

	overs_1=0
	runs_1=0

	try:
		with open("Dataset/Scorecard/"+str(matchId)+".csv",'r') as file:
			reader = csv.reader(file)
			for row in reader:
				if(row[1]=='nil'):
					break

				if(row[1]=='ScoreA'):
					continue

				overs_1=overs_1+1
				runs_1=int(row[1].partition("/")[0])
				
		
		net_run_rate_1=float(runs_1)/float(overs_1)

		overs_2=0
		runs_2=0

		with open("Dataset/Scorecard/"+str(matchId)+".csv",'r') as file:
			reader = csv.reader(file)
			for row in reader:

				if(row[2]=='nil'):
					break

				if(row[2]=='ScoreB'):
					continue

				overs_2=overs_2+1
				runs_2=int(row[2].partition("/")[0])

		net_run_rate_2=float(runs_2)/float(overs_2)

	except:
		net_run_rate_1=0
		net_run_rate_2=0

	if(toss_decision_list[match_id_no]==1):
		teamA_net_rates.append(net_run_rate_1)
		teamB_net_rates.append(net_run_rate_2)
	else:
		teamA_net_rates.append(net_run_rate_2)
		teamB_net_rates.append(net_run_rate_1)

	match_id_no=match_id_no+1

index=0

print "list of net run rates of teamA"
print teamA_net_rates

print "\nlist of net run rates of teamB"
print teamB_net_rates

print "\nlist of dates of matches played"
print dates_list

for date in dates_list:

	date=date[0:10]
	date=datetime.strptime(date,"%Y-%m-%d")
	dates_list[index]=date
	index=index+1

plot_graph_teamA(teamA,teamA_net_rates,dates_list)
plot_graph_teamB(teamB,teamB_net_rates,dates_list)
plot_graph_teamA_and_teamB(teamA,teamB,teamA_net_rates,teamB_net_rates,dates_list)