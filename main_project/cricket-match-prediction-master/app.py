from __future__ import division
import pandas as pd
import numpy as np
import glob

from collections import defaultdict
from sklearn import model_selection
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier, RandomForestRegressor, AdaBoostRegressor
from sklearn.model_selection import KFold

def HomeTeam(df1):
	d = defaultdict(list)
	country=''
	with open ('stadium/stadiums', 'r') as f:
	    lines = f.read().splitlines()
	    length=len(lines)
	    i=0
	    while i<length:
	        line = lines[i]
	    	if line == '$':
	    		country=lines[i+1]
	    		i+=1
	    	else:
	    		d[country].append(line)
	    	i+=1

	for index, row in df1.iterrows():
		if row['Venue'] in (d[row['TeamA']]):
			  df1.iloc[index, 6] = 1
		if row['Venue'] in (d[row['TeamB']]):
			df1.iloc[index, 6] = -1
		if row['Venue']not in(d[row['TeamB']]) and row['Venue']not in(d[row['TeamA']]):
			df1.iloc[index, 6] = 0
	return


def HTH(df):
	df.to_csv('beforeHTH.csv')
	for i in range(0, len(df)):
		teamA=df.loc[i, 'TeamA']
		teamB=df.loc[i, 'TeamB']
		date=df.loc[i, 'Date']
		
		playOffAandB=df[((df['TeamA']==teamA)&(df['TeamB']==teamB) | (df['TeamA']==teamB)&(df['TeamB']==teamA))&(df.Date<date)]
		playOffAandB = playOffAandB.sort_values(by = 'Date', ascending=[0])
		playOffAandB = playOffAandB.head(10)
		
		Awin=playOffAandB[(playOffAandB['Winner']==teamA)]
		a=len(Awin)
		p=len(playOffAandB)
		
		if p==0:
			df.iloc[i, 9] = 0.0
		else:	
			df.iloc[i, 9] = a/p
		
	df.to_csv("HTHOutput.csv")
	return


def WinningPerDes(df):
	for i in range(0, len(df)):
		date=df.iloc[i, 5]
		venue=df.iloc[i, 6]
		selection = df.iloc[i, 2]

		prevMatches = df[(df['Venue']==venue)&(df.Date<date)]
		prevMatches = prevMatches.sort_values(by = 'Date', ascending=[0])
		prevMatches = prevMatches.head(10)
		
		#print prevMatches

		if selection == 1:
			Awin = prevMatches[(prevMatches['Toss_Decision'] == prevMatches['Winner'])]
		else:
			Awin = prevMatches[(prevMatches['Toss_Decision'] != prevMatches['Winner'])]

		#print Awin
		a=len(Awin)
		p=len(prevMatches)
		
		if p==0:
			df.iloc[i, 10] = 0.0
		else:	
			df.iloc[i, 10] = a/p
		
	return

def Toss(df1):
	df1.loc[df1['Toss'] == df1['TeamA'], 'Toss'] = 1
	df1.loc[df1['Toss'] == df1['TeamB'], 'Toss'] = 0
	df1.loc[(df1['Toss_Decision'] == 'bat') & (df1['Toss'] == 1), 'Toss_Decision'] = 1
	df1.loc[(df1['Toss_Decision'] == 'bat') & (df1['Toss'] == 0), 'Toss_Decision'] = 0
	df1.loc[(df1['Toss_Decision'] == 'field') & (df1['Toss'] == 1), 'Toss_Decision'] = 0
	df1.loc[(df1['Toss_Decision'] == 'field') & (df1['Toss'] == 0), 'Toss_Decision'] = 1
	df1.loc[df1['Winner'] == df1['TeamA'], 'Winner'] = 1
	df1.loc[df1['Winner'] == df1['TeamB'], 'Winner'] = 0
	
			
def Classfier(df1):
	predictors = ['Toss', 'Toss_Decision', 'HTH', 'Venue', 'WinningPerDes','Strength','latest_form'] #, 'Toss_Decision', 'HTH', 'Venue', 'WinningPerDes' ... LogisticRegression(random_state=1)  ......AdaBoostRegressor(DecisionTreeRegressor(max_depth=10), n_estimators=500, random_state=1)
	alg = DecisionTreeRegressor(max_depth=10)#RandomForestRegressor(random_state = 0, n_estimators = 500)#ExtraTreesClassifier(random_state=1, n_estimators=500, min_samples_split=2, min_samples_leaf=1)##LogisticRegression(random_state=1)
	df = df1[['Toss', 'Toss_Decision', 'HTH', 'Venue', 'WinningPerDes', 'Strength','latest_form','Winner']]
	kf = KFold(df1.shape[0], random_state=1)
	predictions = []
	for train, test in kf.split(df):
		train_predictors = (df[predictors].iloc[train,:])
		train_target = df["Winner"].iloc[train]
		alg.fit(train_predictors, train_target)
		test_predictions = alg.predict(df[predictors].iloc[test,:])
		predictions.append(test_predictions)

	predictions = np.concatenate(predictions, axis=0)
	predictions = predictions.astype(int)
	cnt = 0
	for index, row in df.iterrows():
		if predictions[index] == row["Winner"]:
			cnt = cnt + 1

	accuracy = cnt/len(predictions)
	print accuracy

def bat_debut():
	path ="C:/Users/jatin singhal/Downloads/cricket-match-prediction-master/cricket-match-prediction-master/Dataset/PlayerInfo" # use your path
	allFiles = glob.glob(path + "/*.csv")
	frame = pd.DataFrame()
	list_ = []
	for file_ in allFiles:
	    df = pd.read_csv(file_,index_col=None, header=0)
	    # print df
	    list_.append(df)
	frame = pd.concat(list_)
	frame.to_csv('batDebutOutput.csv')

	# batsman
	debutant_bat=frame[((frame['Bat_Inngs']=='1') & (frame['Bowl_Inngs']=='-') &(frame['Matches_Played']==1))]
	sum1=0
	for index, row in debutant_bat.iterrows():
		sum1=sum1+int(row['Runs_Scored'])
	sum1=sum1*1.0	
	avg=sum1/len(debutant_bat)

	#bowler
	debutant_bowl=frame[((frame['Bowl_Inngs']=='1')&(frame['Matches_Played']==1))]
	wickts_taken=0.0
	runs_conceded=0.0

	for index, row in debutant_bowl.iterrows():
		runs_conceded=runs_conceded+int(row['Runs_Conceded'])
		wickts_taken=wickts_taken+int(row['Wkts_Taken'])
		#print row['Wkts_Taken'],row['Runs_Conceded']

	#print runs_conceded,wickts_taken
	bowl_avg=runs_conceded/wickts_taken

	return avg,bowl_avg

def Scoringfn(df1, bat_avg, bowl_avg):

	MAX = 100
	for i in range(0, len(df1)):
		#print "------------------------------------------------------------------"
		teamA=str(df1.loc[i, 'TeamA'])
		teamB=str(df1.loc[i, 'TeamB'])
			
		name = str(df1.loc[i, 'MatchID'])+'.csv'#"657643" #657645

		df=pd.read_csv("Dataset/PlayerInfo/"+name)

		df['Bowl_Inngs'] = df['Bowl_Inngs'].replace('-', 0)
		df['Matches_Played'] = df['Matches_Played'].replace('-', 0)
		df.loc[(df['Bowl_Inngs'] == 1) & (df['Matches_Played'] == 1), 'Bowl_Avg'] = bowl_avg


		#print df
		df['Bat_Avg'] = df['Bat_Avg'].replace('-', bat_avg)
		df['Bowl_Avg'] = df['Bowl_Avg'].replace('-', MAX)
		df['Wkts_Taken'] = df['Wkts_Taken'].replace('-', 0)

		teamA_list=df[(df.Country==teamA)]
		teamB_list=df[(df.Country==teamB)]

		total_A=0.0
		total_B=0.0

		#batting ab=vg considering 11 players

		for index, row in teamA_list.iterrows():
			total_A=total_A+float(row['Bat_Avg'])
		power_A=total_A/11

		for index, row in teamB_list.iterrows():
			total_B=total_B+float(row['Bat_Avg'])
		power_B=total_B/11
		#print power_A, power_B 


		#bowling avg of 6 bowlers

		teamA_list=teamA_list.sort_values(by = 'Wkts_Taken', ascending=0)
		top_bowl_A=teamA_list.head(6)
		
		# teamB_list[['Bowl_Avg']] = teamB_list[['Bowl_Avg']].astype(float)
		teamB_list=teamB_list.sort_values(by = 'Wkts_Taken', ascending=0)
		top_bowl_B=teamB_list.head(6)
		
		top_A=0.0   
		top_B=0.0
		for index, row in top_bowl_A.iterrows():
			top_A=top_A+float(row['Bowl_Avg'])
			#print row.Wkts_Taken, row.Bowl_Avg, row.Five_Wkts_Hawl
		top_A=top_A/6
		
		#print top_A

		for index, row in top_bowl_B.iterrows():
			top_B=top_B+float(row['Bowl_Avg'])
			#print row.Wkts_Taken, row.Bowl_Avg, row.Five_Wkts_Hawl
		top_B=top_B/6
		
		#print top_B
		

		#strngth=power_A-top_B + top_A-power_B
		strngth=(power_A-top_A) - (power_B-top_B)

		df1.iloc[i, 11]=strngth
	#print cnt/tot	
			
def latest_form(df1, bat_avg):
	for i in range(0, len(df1)):
		#print "------------------------------------------------------------------"
		teamA=str(df1.loc[i, 'TeamA'])
		teamB=str(df1.loc[i, 'TeamB'])
		date=df1.loc[i, 'Date']

		prevMatchesA = df1[((df1['TeamA']==teamA) | (df1['TeamB']==teamA)) & (df1.Date<date)]
		prevMatchesA = prevMatchesA.tail()
		
		form_A = 0
		cntA = 0
		for index, row in prevMatchesA.iterrows():
			name = str(row['MatchID'])+'.csv'#"657643" #657645
			df=pd.read_csv("Dataset/PlayerInfo/"+name)
			df['Bat_Avg'] = df['Bat_Avg'].replace('-', bat_avg)
			total_A = 0
			cntA = cntA + 1
			team_list=df[(df['Country']==teamA)]
			for index1, row1 in team_list.iterrows():
				total_A=total_A+float(row1['Bat_Avg'])
			form_A = form_A + total_A/11

		prevMatchesB = df1[((df1['TeamA']==teamB) | (df1['TeamB']==teamB)) & (df1.Date<date)]
		prevMatchesB = prevMatchesB.tail()
		
		form_B = 0
		cntB = 0
		for index, row in prevMatchesB.iterrows():
			name = str(row['MatchID'])+'.csv'#"657643" #657645
			df=pd.read_csv("Dataset/PlayerInfo/"+name)
			df['Bat_Avg'] = df['Bat_Avg'].replace('-', bat_avg)
			total_B = 0
			cntB = cntB + 1
			team_list=df[(df['Country']==teamB)]
			for index1, row1 in team_list.iterrows():
				total_B=total_B+float(row1['Bat_Avg'])
			form_B = form_B + total_B/11

		# print form_A, form_B, df1.loc[i, 'MatchID'] 
		if cntA == 0:
			cntA = 1
			formA = bat_avg
		if cntB == 0:
			cntB = 1
			formB = bat_avg
		
		df1.loc[i, 'latest_form']= form_A/cntA - form_B/cntB 



# def testPredicit(df1,testData):
# 	predictors = ['Toss', 'Toss_Decision','Venue', 'HTH', 'WinningPerDes','Strength']
# 	alg = LogisticRegression(random_state=1)
# 	df = df1[['Toss', 'Toss_Decision', 'Venue', 'HTH', 'WinningPerDes', 'Strength','Winner']]
# 	predictions = []
# 	train_predictors = (df[predictors])
# 	train_target = df["Winner"]
# 	alg.fit(train_predictors, train_target)
# 	test_predictions = alg.predict(testData)
# 	if test_predictions[0] == 1:
# 		print "Winner: india"
# 	else:
# 		print "Winner: Pakistan"
			



####Main

df1 = pd.read_csv('Dataset/CompleteMatchDetails.csv')

df1['Date'] = pd.to_datetime(df1.Date)

df1['HTH'] = 0
df1['WinningPerDes'] = 0
df1['Strength'] = 0
df1['latest_form']=0

print len(df1)
for index in range(len(df1)):
	if df1.loc[index,'TeamB'] < df1.loc[index,'TeamA']:
		df1.loc[index,['TeamA','TeamB']] = df1.loc[index,['TeamB','TeamA']].values

df1.to_csv("initialOutput.csv")

HTH(df1)
Toss(df1)
WinningPerDes(df1)
HomeTeam(df1)
bat_avg,bowl_avg=bat_debut()
print bat_avg
print bowl_avg

Scoringfn(df1, bat_avg, bowl_avg)
latest_form(df1, bat_avg)
df1.to_csv("OutputOfAllModified.csv")





