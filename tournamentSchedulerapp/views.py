from django.http import JsonResponse
from datetime import datetime,timedelta
from rest_framework.decorators import api_view
import json
from .serializers import TeamSerializer

class Match(object):
	def __init__(self,date, day,team_1, team_2): # Match between team_1 and team_2 on date, day
		self.date = date
		self.day = day
		self.team_1 = team_1
		self.team_2 = team_2

def validate(date_text): #validation function
    try:
        datetime.strptime(date_text, '%d/%m/%Y') #checking the correct format of date
    except ValueError:
        raise ValueError("Incorrect data format, should be DD/MM/YYYY") #error

@api_view(['POST', ])
def index(request):
	date = request.data.get("date") 				# input was date 
	validate(date) 									# date being validated
	l = list(date.split('/')) 						# splitting date to three strings of day, month, year
	date = datetime(int(l[2]),int(l[1]),int(l[0])) 	# creating date using datetime library
	week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

	n = 6  				# No of Teams. You can give any even number greater than 4 and get the schedule.
	matchlist = [] 		# out output initialised to null 
	# For simplicity I am refering teams as numbers starting from 0 ie Team 0, Team 1 and so on... 
	# 1. creating matches as consecutive numbers even Vs odd and then rescheduling them again
	for j in range (2):
		for i in range(0,n,2):
			if(i!=0 or j != 0): 							# as for i==0 we have the date given to us as input so no need to increment it.
				date += timedelta(days=1) 					# next date
			day = week_days[date.weekday()] 				# day on particular date being calculated
			date_1 = date.strftime("%d/%m/%Y") 				# converting date to string in the required format
			a = Match(date= date_1,day = day,team_1=i,team_2=i+1) # match created
			matchlist.append(a) 							# match appended to matchlist
	
	#2. creating matches as odd vs odd and even vs even in increasing order
	for i in range(0,n,2):
		for j in range(i+2, n, 2):
			for k in range(4): #even vs even -> odd vs odd -> even vs even -> odd vs odd  
				date += timedelta(days=1)
				day = week_days[date.weekday()]
				date_1 = date.strftime("%d/%m/%Y")
				if( k % 2 == 0): 			# for creating alternate matches of odd vs odd and even vs even so that no team has match no consecutive days
					a = Match(date= date_1,day = day,team_1=i,team_2=j)
				else:
					a = Match(date= date_1,day = day,team_1=i+1,team_2=j+1)
				matchlist.append(a)	
	#3. Creating matches as even vs odd now excluding the consecutive integers in increasing order 		
	for i in range(0,n,2):
		for j,j1 in zip(range(i+3, n, 2), range(i+2,n,2)):
			for k in range(4): 
				date += timedelta(days=1)
				day = week_days[date.weekday()]
				date_1 = date.strftime("%d/%m/%Y")
				if( k % 2 == 0):
					a = Match(date= date_1,day = day,team_1=i+1,team_2=j1)
				else:
					a = Match(date= date_1,day = day,team_1=i,team_2=j)
				matchlist.append(a)	
			
	serializer = TeamSerializer(matchlist, many=True) # serializing the data

	return JsonResponse(serializer.data, safe = False) # sending the Json response
