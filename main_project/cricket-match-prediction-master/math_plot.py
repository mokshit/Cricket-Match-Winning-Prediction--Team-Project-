# importing the required module
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates

import matplotlib.pyplot as plt
import matplotlib.dates as dte




def plot_graph_teamA(teamA,teamA_net_rates,dates_list):
	#PLOTTING THE GRAPH OF TEAM 1
	x=dates_list
	y1=teamA_net_rates

	#plt.plot(x,y1)
	dates = dte.date2num(x)


	#plotting for teamA
	plt.plot_date(dates, y1)

	plt.xlabel("dates")
	plt.ylabel("peformance (net run rate)")
	plt.title(teamA)

	plt.gcf().autofmt_xdate()
	plt.legend([teamA], loc='upper left')
	plt.savefig(teamA+'.png')




def plot_graph_teamB(teamB,teamB_net_rates,dates_list):
	#PLOTTING THE GRAPH OF TEAM 1
	x=dates_list
	y2=teamB_net_rates

	#plt.plot(x,y1)
	dates = dte.date2num(x)

	plt.clf()

	#plotting for teamB
	plt.plot_date(dates, y2)

	plt.xlabel("dates")
	plt.ylabel("peformance (net run rate)")
	plt.title(teamB)

	plt.gcf().autofmt_xdate()
	plt.legend([teamB], loc='upper left')
	plt.savefig(teamB+'.png')

	


def plot_graph_teamA_and_teamB(teamA,teamB,teamA_net_rates,teamB_net_rates,dates_list):
	x=dates_list
	y2=teamB_net_rates
	y1=teamA_net_rates

	dates = dte.date2num(x)

	plt.clf()

	plt.plot_date(dates, y2)
	plt.plot_date(dates, y1)

	plt.xlabel("dates")
	plt.ylabel("peformance (net run rate)")
	plt.title(teamA+"vs"+teamB)

	plt.gcf().autofmt_xdate()
	plt.legend([teamB,teamA], loc='upper left')
	plt.savefig(teamA+"vs"+teamB+'.png')

	