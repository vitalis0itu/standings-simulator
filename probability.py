import itertools
import random
import argparse
from decimal import Decimal, ROUND_HALF_UP

class Standings:
    def __init__(self, teams):
        self.teams = teams
        self.points_table = {}
        for team in teams:
            self.points_table[team] = 0
        self.order = {}
        self.order_in_sync = False

    def add_match_result(self, result):
        if result['result'] == '1':
            self.add_points(result['home'], 3)
        elif result['result'] == '2':
            self.add_points(result['away'], 3)
        elif result['result'] == 'X':
            self.add_points(result['home'], 1)
            self.add_points(result['away'], 1)
        else:
            print('got unexpected results:', result)

    def add_match_results(self, results):
        for result in results:
            self.add_match_result(result)

    def add_points(self, team, points):
        self.order_in_sync = False
        self.points_table[team] = self.points_table[team] + points

    def set_points(self, team, points):
        self.order_in_sync = False
        self.points_table[team] = points

    def sync_order(self):
        dictlist = []
        for key, value in self.points_table.items():
            temp = [key,value]
            dictlist.append(temp)
        dictlist = sorted(dictlist, key=lambda temp: temp[1], reverse=True)
        for i in range(len(dictlist)):
            self.order[dictlist[i][0]] = i + 1
        self.order_in_sync = True

    def get_rank(self, team):
        if not self.order_in_sync:
            self.sync_order()
        return self.order[team]


class Summary:
    def __init__(self, teams):
        self.teams = teams
        self.ranks = {}
        for team in teams:
            self.ranks[team] = {}
        self.standing_count = 0
    
    def add_standing(self, standing):
        self.standing_count = self.standing_count + 1
        for team in self.teams:
            team_rank = standing.get_rank(team)
            if team_rank in self.ranks[team]:
                self.ranks[team][team_rank] = self.ranks[team][team_rank] + 1
            else:
                self.ranks[team][team_rank] = 1


def copy_standings(standings):
    new_standings = Standings(standings.teams)
    points_table = standings.points_table
    for key, value in points_table.items():
        new_standings.set_points(key, value)
    return new_standings


def generate_matches(teams):
    matches = []
    for pair in itertools.combinations(teams, 2):
        matches.append({'home': pair[0], 'away': pair[1]})
        matches.append({'home': pair[1], 'away': pair[0]})
    return matches


def read_existing_results(filename):
    with open(filename, 'r') as file:
        results = []
        for line in file:
            strip = line.strip()
            if strip == '' or strip[0] == '#':
                continue
            items = strip.split(',')
            results.append({'home': items[0], 'away': items[1], 'result': items[2]})
        file.close()
        return results


def filter_remaining_matches(existing_results, matches):
    def existing_match(match):
        for existing_result in existing_results:
            if existing_result['home'] != match['home']:
                continue
            if existing_result['away'] == match['away']:
                return True
        return False
    return [match for match in matches if not existing_match(match)]


def random_result(tie_probability):
    rand = random.random()
    if rand < tie_probability:
        return 'X'
    rand = random.random()
    if rand < 0.5:
        return '1'
    return '2'


def random_results(length, tie_probability):
    return [random_result(tie_probability) for i in range(length)]


def main():
    parser = argparse.ArgumentParser(description='EURO 2020 QUALIFICATION GROUP J PROBABILITIES')
    parser.add_argument('-s', '--sample-size', required=True)
    parser.add_argument('-tp', '--tie-probability', required=True)
    parser.add_argument('-t', '--teams', nargs='+', required=True)
    parser.add_argument('-er', '--existing-results', required=True)
    args = parser.parse_args()
    teams = args.teams
    existing_results = read_existing_results(args.existing_results)
    print('got', len(existing_results), 'existing results')
    print('Sample size:', args.sample_size)
    print('Tie probability:', args.tie_probability)
    for existing_result in existing_results:
        if existing_result['home'] not in teams:
            print('unexpected home team', existing_result)
        if existing_result['away'] not in teams:
            print('unexpected away team', existing_result)
    matches = generate_matches(teams)
    remaining_matches = filter_remaining_matches(existing_results, matches)
    standings = Standings(teams)
    standings.add_match_results(existing_results)
    summary = Summary(teams)
    for i in range(int(args.sample_size)):
        results_arr = random_results(len(remaining_matches), Decimal(args.tie_probability))
        new_standings = copy_standings(standings)
        for i in range(len(remaining_matches)):
            new_standings.add_match_result({'home': remaining_matches[i]['home'], 'away': remaining_matches[i]['away'], 'result': results_arr[i]})
        summary.add_standing(new_standings)
    def my_key(team):
        return summary.ranks[team][1]
    def to_row(team):
        elements = [team]
        for i in range(len(teams)):
            share = Decimal(100 * summary.ranks[team][i+1] / summary.standing_count)
            elements.append(str(Decimal(share.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))))
        return elements
    print('team,1,2,3,4,5,6')
    for team in sorted([k for k in summary.ranks], key=my_key, reverse=True):
        print(','.join(to_row(team)))


main()
