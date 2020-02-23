from rest_framework import serializers

class TeamSerializer(serializers.Serializer):
	date = serializers.DateTimeField()
	day = serializers.CharField(max_length=10)
	team_1 = serializers.IntegerField()
	team_2 = serializers.IntegerField()