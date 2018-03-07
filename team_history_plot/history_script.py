import csv
import pandas as pd

#taking input from the user
'''
team1=input("enter team1")
team2=input("enter team2")
'''
teamA='Sri Lanka'
teamB='South Africa'

df=pd.read_csv('OutputOfAll.csv')

df=df.loc[(df['TeamA']==teamA & df['TeamB']==teamB) | (df['TeamA']==teamB & df['TeamB']==teamA)]
df=df.sort_values(by='Date', ascending=[1])

matchID_list=df.['MatchID'].tolist()
toss_decision_list=df['Toss_Decision'].tolist()
teamA_net_rates=[]
teamB_net_rates=[]

match_id_no=0

for matchId in matchID_list:

	overs_1=-1
	runs_1=0

	with open("Dataset/Scorecard/"str(file_name[0])+".csv",'r') as file:
		for row in file:

			if(row[1]=='nil'):
				break

			overs_1++
			runs_1=row[1].partition("/")[0]

	net_run_rate_1=runs_1/overs_1

	overs_2=-1
	runs_2=0

	with open("Dataset/Scorecard/"str(file_name[0])+".csv",'r') as file:
		for row in file:

			if(row[2]=='nil'):
				break

			overs_2++
			runs_2=row[2].partition("/")[0]

	net_run_rate_2=runs_2/overs_2

	if(toss_decision_list[match_id_no]==1):
		teamA_net_rates.append(net_run_rate_1)
		teamB_net_rates.append(net_run_rate_2)
	else
		teamA_net_rates.append(net_run_rate_2)
		teamB_net_rates.append(net_run_rate_1)

	match_id_no++
	