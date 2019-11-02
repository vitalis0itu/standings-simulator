import argparse
import itertools
import random
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Callable, Tuple


class Game:
    def __init__(self, home: str, away: str):
        self.home = home
        self.away = away

    def __eq__(self, game):
        return self.home == game.home and self.away == game.away

    def __str__(self) -> str:
        return ''.join(['Game{', self.home, ',', self.away, '}'])


class GameResult:
    def __init__(self, game: Game, result: str):
        self.game = game
        self.result = result

    def __str__(self) -> str:
        return ''.join(['GameResult{', self.game, ',', self.result, '}'])


class TeamRanking:
    def __init__(self, team: str, ranking: int):
        self.team = team
        self.ranking = ranking


class Standings:
    def __init__(self, teams, point_system: str):
        self.teams = teams
        self.point_system = point_system
        self.points_table = {}
        self.results_by_team = {}
        for team in teams:
            self.points_table[team] = 0
            if point_system == 'f':
                self.results_by_team[team] = {'G': 0, 'W': 0, 'T': 0, 'L': 0}
            if point_system == '3ph':
                self.results_by_team[team] = {'G': 0, 'W': 0, 'OTW': 0, 'OTL': 0, 'L': 0}

    def add_match_result(self, result: GameResult):
        game = result.game
        if self.point_system == 'f':
            if result.result == '1':
                self.add_points(game.home, 3)
                self.add_team_result(game.home, 'W')
                self.add_team_result(game.away, 'L')
            elif result.result == '2':
                self.add_points(game.away, 3)
                self.add_team_result(game.home, 'L')
                self.add_team_result(game.away, 'W')
            elif result.result == 'X':
                self.add_points(game.home, 1)
                self.add_points(game.away, 1)
                self.add_team_result(game.home, 'T')
                self.add_team_result(game.away, 'T')
            else:
                print('got unexpected results:', result)
        if self.point_system == '3ph':
            if result.result == '1':
                self.add_points(game.home, 3)
                self.add_team_result(game.home, 'W')
                self.add_team_result(game.away, 'L')
            elif result.result == '2':
                self.add_points(game.away, 3)
                self.add_team_result(game.home, 'L')
                self.add_team_result(game.away, 'W')
            elif result.result == '1OT':
                self.add_points(game.home, 2)
                self.add_points(game.away, 1)
                self.add_team_result(game.home, 'OTW')
                self.add_team_result(game.away, 'OTL')
            elif result.result == '2OT':
                self.add_points(game.home, 1)
                self.add_points(game.away, 2)
                self.add_team_result(game.home, 'OTL')
                self.add_team_result(game.away, 'OTW')
            else:
                print('got unexpected results:', result)

    def add_match_results(self, results: List[GameResult]):
        for result in results:
            self.add_match_result(result)

    def clone(self):
        copy_standings = Standings(self.teams, self.point_system)
        copy_standings.points_table = dict(self.points_table)
        for team in self.teams:
            copy_standings.results_by_team[team] = dict(self.results_by_team[team])
        return copy_standings

    def add_team_result(self, team: str, result: str):
        self.results_by_team[team]['G'] += 1
        self.results_by_team[team][result] += 1

    def get_team_result(self, team: str):
        return self.results_by_team[team]

    def add_points(self, team: str, points: int):
        self.points_table[team] = self.points_table[team] + points

    def set_points(self, team: str, points: int):
        self.points_table[team] = points

    def to_rankings(self) -> List[TeamRanking]:
        def my_key(team) -> Tuple:
            team_result = self.get_team_result(team)
            if self.point_system == '3ph':
                return self.points_table[team], team_result['W'], team_result['OTW'], team_result['OTL']
            if self.point_system == 'f':
                return self.points_table[team], team_result['W'], team_result['T']

        ranked_teams = sorted(self.teams, key=my_key, reverse=True)
        return [TeamRanking(ranked_teams[i], i + 1) for i in range(len(ranked_teams))]

    def __str__(self) -> str:
        standing_lines = []
        if self.point_system == '3ph':
            standing_lines.append(('team', 'Games', 'Win', 'OT Win', 'OT Loss', 'Loss', 'Points'))
            for team_ranking in self.to_rankings():
                team = team_ranking.team
                result = self.results_by_team[team]
                standing_lines.append((team, result['G'], result['W'], result['OTW'], result['OTL'], result['L'], self.points_table[team]))

        if self.point_system == 'f':
            standing_lines.append(('team', 'Games', 'Win', 'Tie', 'Loss', 'Points'))
            for team_ranking in self.to_rankings():
                team = team_ranking.team
                result = self.results_by_team[team]
                standing_lines.append((team, result['G'], result['W'], result['T'], result['L'], self.points_table[team]))
        return '\n'.join([','.join([str(y) for y in x]) for x in standing_lines])


class Summary:
    def __init__(self, teams: List[str]):
        self.teams = teams
        self.ranks = {}
        for team in teams:
            self.ranks[team] = {}
            for ranking in range(1, len(teams) + 1):
                self.ranks[team][ranking] = 0
        self.standing_count = 0

    def add_standing(self, standing: Standings):
        self.standing_count = self.standing_count + 1
        rankings = standing.to_rankings()
        for ranking in rankings:
            team = ranking.team
            team_rank = ranking.ranking
            if team_rank in self.ranks[team]:
                self.ranks[team][team_rank] = self.ranks[team][team_rank] + 1
            else:
                self.ranks[team][team_rank] = 1


def generate_games(teams: List[str], rounds: int) -> List[Game]:
    games = []
    for pair in itertools.combinations(teams, 2):
        for round in range(rounds):
            games.append(Game(pair[round % 2], pair[(round + 1) % 2]))
    return games


def filter_remaining_matches(existing_results: List[GameResult], games: List[Game]) -> List[Game]:
    for existing_result in existing_results:
        for index in range(len(games)):
            game = games[index]
            if existing_result.game != game:
                continue
            games.pop(index)
            break
    return games


def random_result(tie_probability: float, point_system: str):
    rand = random.random()
    if rand < tie_probability:
        if point_system == 'f':
            return 'X'
        elif point_system == '3ph':
            if random.random() < 0.5:
                return '1OT'
            else:
                return '2OT'
        else:
            raise NotImplementedError('Unsupported point system ' + point_system)
    rand = random.random()
    if rand < 0.5:
        return '1'
    return '2'


def random_results(length: int, tie_probability: float, point_system: str):
    return [random_result(tie_probability, point_system) for i in range(length)]


def read_lines(filename: str, callback: Callable[[List[str]], None]):
    with open(filename, 'r') as file:
        for line in file:
            strip = line.strip()
            if strip == '' or strip[0] == '#':
                continue
            items = strip.split(',')
            callback(items)
        file.close()


def read_existing_results(filename: str) -> List[GameResult]:
    results = []

    def callback(items: List[str]) -> None:
        if len(items) >= 3:
            results.append(GameResult(Game(items[0], items[1]), items[2]))

    read_lines(filename, callback)
    return results


def read_games_without_results(filename: str) -> List[Game]:
    results = []

    def callback(items: List[str]) -> None:
        if len(items) == 2:
            results.append(Game(items[0], items[1]))

    read_lines(filename, callback)
    return results


def game_not_in_teams(game: Game, teams: List[str]) -> bool:
    return game.home not in teams or game.away not in teams


def main():
    parser = argparse.ArgumentParser(description='Standings simulator')
    parser.add_argument('-ss', '--sample-size', required=True, help='Number of simulations')
    parser.add_argument('-tp', '--tie-probability', required=True, help='Probability of a tie')
    parser.add_argument('-t', '--teams', nargs='+', required=True, help='Teams, teams with white spaces in their names should be written in double brackets: "FC Barcelona"')
    parser.add_argument('-ps', '--point-system', required=True, help='Points system, "f" for football (1X2: 3-0 or 1-1), "3ph" for 3 point hockey (0-1-2-3) system')
    parser.add_argument('-r', '--rounds', help='How many rounds are played against each other. Do not use with --all-games', type=int)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-er', '--existing-results', help='File containing only existing results')
    group.add_argument('-ag', '--all-games', help='File containing all games with some games having results')
    args = parser.parse_args()
    teams = args.teams
    games = None
    existing_results = []
    if args.all_games is not None:
        if args.rounds is not None:
            raise Exception('Argument --rounds should not be used with --all-games')
        games = read_games_without_results(args.all_games)
        existing_results = read_existing_results(args.all_games)
    if args.existing_results is not None:
        existing_results = read_existing_results(args.existing_results)
    if games is None:
        if args.rounds is None:
            raise Exception('Argument --rounds was not found')
        games = generate_games(teams, args.rounds)
    print('Got', len(existing_results), 'existing results')
    print('Sample size:', args.sample_size)
    print('Tie probability:', args.tie_probability)
    for existing_result in existing_results:
        if game_not_in_teams(existing_result.game, teams):
            print('unexpected team', existing_result)
    for game in games:
        if game_not_in_teams(game, teams):
            print('unexpected team', game)

    remaining_matches = filter_remaining_matches(existing_results, games)
    standings = Standings(teams, args.point_system)
    standings.add_match_results(existing_results)
    print('Current standings:')
    print(standings)
    summary = Summary(teams)
    for i in range(int(args.sample_size)):
        results_arr = random_results(len(remaining_matches), Decimal(args.tie_probability), args.point_system)
        new_standings = standings.clone()
        for i in range(len(remaining_matches)):
            new_standings.add_match_result(GameResult(remaining_matches[i], results_arr[i]))
        summary.add_standing(new_standings)

    def my_key(team):
        return [summary.ranks[team][i + 1] for i in range(len(teams))]

    def to_row(team):
        elements = [team]
        for i in range(len(teams)):
            share = Decimal(100 * summary.ranks[team][i + 1] / summary.standing_count)
            elements.append(str(Decimal(share.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))))
        return elements

    def print_result():
        print('Simulated probabilities:')
        print(','.join(['team'] + [str(x) for x in range(1, len(teams) + 1)]))
        for team in sorted([k for k in summary.ranks], key=my_key, reverse=True):
            print(','.join(to_row(team)))

    print_result()


main()
