# Soccer standings simulator
This python3 program runs given number of simulations and outputs "probabilities" for each given team for each ranking. We assume that each team has one home game against every
other team. We assume that all teams are equally strong but probability for a tie is given by user.
## Output
Output is a table of ranking occurrence percentages in simulations.
```
team,1,2,3,4,5,6
Italy,67.64,21.73,7.50,2.53,0.57,0.03
Finland,21.74,43.01,20.24,9.88,4.40,0.73
Armenia,6.58,17.30,31.94,24.33,15.26,4.60
Greece,2.17,8.75,17.21,25.55,32.49,13.84
Bosnia,1.81,8.34,19.28,28.39,27.37,14.81
Liechtenstein,0.07,0.87,3.83,9.32,19.91,66.00
```
This says that Finland had second place in 43.01% of simulations. 

## Input

```
python3 probability.py --sample-size 100000 --tie-probability 0.186842105263158 -t Italy Finland Armenia Bosnia Greece Liechtenstein -er example-existing-results.txt
```
* -s, --sample-size: Number of simulations
* -tp, --tie-probability: Probability of a tie. Premier league schedule in 2018-2019 had 380 games of which 71 ended in a tie resulting 0.186842105263158,
* -t, --teams: List of participating teams
* -er, --existing-results: Path to file containing existing results.

Example of existing results file:
```
#2019-03-23
Bosnia,Armenia,1
Italy,Finland,1
Liechtenstein,Greece,2
#2019-03-26
Armenia,Finland,2
Bosnia,Greece,X
Italy,Liechtenstein,1
#2019-06-08
Armenia,Liechtenstein,1
Finland,Bosnia,1
Greece,Italy,2
#2019-06-11
Greece,Armenia,2
Italy,Bosnia,1
Liechtenstein,Finland,2
```
