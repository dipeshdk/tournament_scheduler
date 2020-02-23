from django.http import JsonResponse
from datetime import datetime,timedelta
from rest_framework.decorators import api_view
import json
from .serializers import TeamSerializer

class Match(object):
	def __init__(self,date, day,team_1, team_2): # Match between team_1 and team_2
		self.date = date
		self.day = day
		self.team_1 = team_1
		self.team_2 = team_2

def validate(date_text):
    try:
        datetime.strptime(date_text, '%d/%m/%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD/MM/YYYY")
        

@api_view(['POST', ])
def index(request):
	date = request.data.get("date")
	validate(date)
	l = list(date.split('/'))
	date = datetime(int(l[2]),int(l[1]),int(l[0]))
	week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

	n = 6  # No of Teams. You can give any even number greater than 4 and get the schedule.
	matchlist = []

	for i in range(0,n,2):
		if(i!=0):
			date += timedelta(days=1) #next date
		day = week_days[date.weekday()]
		date_1 = date.strftime("%d/%m/%Y")
		a = Match(date= date_1,day = day,team_1=i,team_2=i+1)
		matchlist.append(a)

	for i in range(0,n,2):
		date += timedelta(days=1)
		day = week_days[date.weekday()]
		date_1 = date.strftime("%d/%m/%Y")
		a = Match(date= date_1,day = day,team_1=i,team_2=i+1)
		matchlist.append(a)	

	for i in range(0,n,2):
		for j in range(i+2, n, 2):
			for k in range(4):
				date += timedelta(days=1)
				day = week_days[date.weekday()]
				date_1 = date.strftime("%d/%m/%Y")
				if( k % 2 == 0):
					a = Match(date= date_1,day = day,team_1=i,team_2=j)
				else:
					a = Match(date= date_1,day = day,team_1=i+1,team_2=j+1)
				matchlist.append(a)	

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

	return JsonResponse(serializer.data, safe = False)
