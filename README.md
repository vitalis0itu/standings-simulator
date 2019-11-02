# Standings simulator
This python3 program runs given number of simulations and outputs "probabilities" for each given team for each ranking.
## Output
Output is a table of ranking occurrence percentages in simulations.
```
team,1,2,3,4,5,6
Italy,67.64,21.73,7.50,2.53,0.57,0.03
Finland,21.74,43.01,20.24,9.88,4.40,0.73
Armenia,6.58,17.30,31.94,24.33,15.26,4.60
Greece,2.17,8.75,17.21,25.55,32.49,13.84
Bosnia,1.81,8.34,19.28,28.39,27.37,14.81
Swe Den,0.07,0.87,3.83,9.32,19.91,66.00
```
This says that Finland had second place in 43.01% of simulations. 

## Input

```
python3 probability.py -ps f -wpff -ss 100000 -tp 0.186842 -t Italy Finland Armenia Bosnia Greece "Swe Den" -er example-existing-results.txt -r 2
python3 probability.py -ps f -wpw -ss 100000 -tp 0.186842 -t Italy Finland Armenia Bosnia Greece "Swe Den" -ag all-games.txt
python3 probability.py -ps 3ph -wpff -ss 100000 -tp 0.186842 -t Italy Finland Armenia Bosnia Greece "Swe Den" -r 4
```

* `-s`, `--sample-size`:
  * Number of simulations
* `-tp`, `--tie-probability`:
  * Probability of a tie. Premier league schedule in 2018-2019 had 380 games of which 71 ended in a tie resulting 0.186842105263158,
* `-wpff`, `--win-probability-fifty-fifty`:
  * Probability of win is assumed to be equal between any two teams. This is the default behaviour at the moment, so the switch is redundant.
* `-wpw`, `--win-probability-weighted`:
  * Probability of win is weighted by points percentage of existing game results. This option will give odd results if no existing results are given.
* `-tp`, `--tie-probability`:
  * Probability of a tie. Premier league schedule in 2018-2019 had 380 games of which 71 ended in a tie resulting 0.186842105263158,
* `-t`, `--teams`:
  * List of participating teams
* `-ps`, `--points-system`:
  * Points system, "f" for football (1X2: 3-0 or 1-1), "3ph" for 3 point hockey (0-1-2-3) system
* `-r`, `--rounds`:
  * How many rounds are played against each other. Do not use with `--all-games`. Probably will not work well if the number is odd.
* `-er`, `--existing-results`:
  * Path to file containing existing results. Rounds argument should be used with this.
* `-ag`, `--all-games`:
  * Path to file containing all games. Game result should be written in third column.

Example of existing results file:
```
#2019-03-23
Bosnia,Armenia,1
Italy,Finland,1
Swe Den,Greece,2
#2019-03-26
Armenia,Finland,2
Bosnia,Greece,X
Italy,Swe Den,1
#2019-06-08
Armenia,Swe Den,1
Finland,Bosnia,1
Greece,Italy,2
#2019-06-11
Greece,Armenia,2
Italy,Bosnia,1
Swe Den,Finland,2
```

Example of all games file:
```
#2019-03-23
Bosnia,Armenia,1
Italy,Finland,1
Swe Den,Greece,2
#2019-03-26
Armenia,Finland,2
Bosnia,Greece,X
Italy,Swe Den,1
#2019-06-08
Armenia,Swe Den
Finland,Bosnia
Greece,Italy
#2019-06-11
Greece,Armenia
Italy,Bosnia
Swe Den,Finland
```
