# tournament_scheduler

HOW TO RUN THE API?

Here is what you need to do to run this api.
1. Open postman and send a post request on localhost:8000
2. Give the starting date of the tournament as Json object in the body of the request in the dd/mm/yyyy format. The sample code is shown below:
		{'date' : 23/02/2020} 
3. Now, just click on the send button to send the request and get the tournament schedule as response.

HOW THE CODE WORKS?

Let's take the numbers from 0 to 5 as team numbers.

				0 1
				2 3
				4 5
First we go row wise and schedule the matches.
ie 0 vs 1, 2 vs 3, 4 vs 5 and then repeat them again in the same order.

Then we go column wise first grouping even and odds together.
Even vs Even and Odd vs Odd




