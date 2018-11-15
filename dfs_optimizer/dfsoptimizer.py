from collections import OrderedDict
import csv
import heapq

from lineup import Lineup
from player import Player

SITE = 1 # 0 for draftkings, 1 for fanduel
MAX_LINEUPS = 10
MAX_SAL = 50000 if SITE == 0 else 60000
MIN_POINTS_POS_PLAYER = 5 if SITE == 0 else 2
PROJ_ADJ = 0.1 # experimenting, used when adjusting projs based off rankings
PROJ_FILE = 'projections-dk.csv' if SITE == 0 else 'projections-fd.csv'
EXCLUDED_TEAMS = ['DEN', 'ARI', 'TEN', 'LAC', 'CIN', 'KC', 'NYG', 'ATL'] # list of teams not to use
FLEX_OPTION = 1 # 1 for wr, 2 for rb/wr, 3 for rb/wr/te


def read_player_data(qbs, rbs, wrs, tes, defenses):
    """ Function to get list of players and their attributes
        Uses a projections file called projections.csv which should be located
        in the same directory as this file.
    """

    with open(PROJ_FILE, encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row['Team'] in EXCLUDED_TEAMS:     # todo: give user ability to exclude teams
                continue

            try:
                if '/' in row['Sal']:  # skip N/A salary
                    continue
            except TypeError:
                print(row)

            rank = int(row['Rnk'])
            name = row['Name']
            team = row['Team']
            pos = row['Pos']
            points = float(row['Pts'])
            salary = row['Sal']
            player = Player(rank, name, team, pos, points, salary)

            if pos != 'dst' and points < MIN_POINTS_POS_PLAYER:
                continue

            if pos == 'qb':
                qbs.append(player)
            if pos == 'rb':
                rbs.append(player)
            if pos == 'wr':
                wrs.append(player)
            if pos == 'te':
                tes.append(player)
            if pos =='dst':
                defenses.append(player)

def sort_player_data(qbs, rbs, wrs, tes, defenses):
    """ Function that sorts players within their positions
        Uses the rank as the value to sort by
    """
    return sort_by_rank(qbs), sort_by_rank(rbs), sort_by_rank(wrs), sort_by_rank(tes), sort_by_rank(defenses)

def sort_by_rank(players):
    return sorted(players, key=lambda player: -player.value)

def adjust_projections(qbs, rbs, wrs, tes, defenses):
    """ Function that adjust projections for players that are ranked higher
        but are projection lower point totals than lower ranked players
    """

    for players in (qbs, rbs, wrs, tes, defenses):
        minProj = None
        for p in reversed(players): # lower rank to higher
            if minProj is not None and p.points <= minProj:
                p.points = minProj + PROJ_ADJ
            minProj = p.points

def customize_optimization(qbs, rbs, wrs, tes, defenses, lineup):
    """ Ugly customization through command line. This is going to change once moved to web app
    """

    helpMenu = "Menu options:\na: add player to lineup\ne: exclude player from optimizer\nc: clear current position from lineup\nspace bar: next position)\n"
    print('\n\n')
    print(helpMenu)
    print("When adding/excluding a player option please attach an id to command. ie. a1, e5\n\n")

    for players in (qbs, rbs, wrs, tes, defenses):
        while True:
            strBuilder = ''
            idx = 1
            for p in players:
                strBuilder += f'{idx} {p.player_dfs_info():<30}\t'
                if idx % 3 == 0:
                    strBuilder += '\n'
                idx += 1

            print(strBuilder + '\n')
            print(f"Current lineup:\n{[(v) for k, v in lineup.items() if v is not None]}\n")
            action = input("Enter Option: ")

            try:
                if ord(action) == 32: # if space bar pressed move on to next position
                    break
            except TypeError:
                pass
            try:
                if action == 'c':
                    if p.pos == 'rb':
                        lineup['rb2' if lineup['rb2'] else 'rb1'] = None
                    elif p.pos == 'wr':
                        lineup['wr3' if lineup['wr3'] else 'wr2' if lineup['wr2'] else 'wr1'] = None
                    else:
                        lineup[p.pos] = None
                    continue
                elif len(action) < 2:
                    print('Invalid Input\n')
                    continue

                playerIdx = int(action[1:])

                if playerIdx >= idx:
                    print('No player with that id\n')
                    continue
                elif action[0] == 'a': # add player
                    p = players[playerIdx-1]
                    if p.pos == 'rb':
                        if not lineup['rb1'] or lineup['rb1'] != p:
                            lineup['rb1' if not lineup['rb1'] else 'rb2'] = p
                    elif p.pos == 'wr':
                        if not lineup['wr1'] or lineup['wr1'] != p or lineup['wr2'] != p:
                            lineup['wr1' if not lineup['wr1'] else 'wr2' if not lineup['wr2'] else 'wr3' if not lineup['wr3'] else 'flex'] = p
                    else:
                        lineup[p.pos] = p
                elif action[0] == 'e':
                    del players[playerIdx-1]
                else:
                    print('Invalid Input\n')

            except ValueError:
                print('Invalid Input\n')
                continue

    return qbs, rbs, wrs, tes, defenses

def remove_suboptimal_players(qbs, rbs, wrs, tes, defenses):
    """ Remove any players that have salary greater than or equal to a player ranked higher
    """
    for players in (qbs, rbs, wrs, tes, defenses):
        maxSal = 999999

        for p in players[:]:
            if p.salary <= maxSal:
                maxSal = p.salary
            else:
                players.remove(p)

    return qbs, rbs, wrs, tes, defenses

def get_players(players, max_sal):
    return (p for p in players if p.salary <= max_sal)

def generate_lineups(qbs, rbs, wrs, tes, defenses, lineup):
    print('Generating lineups...\n\n')
    remaining_salary = MAX_SAL

    for qb in get_players(qbs, remaining_salary) if not lineup['qb'] else [lineup['qb']]:
        remaining_salary -= qb.salary
        rb1s = rbs[:]
        rb2s = rbs[:]

        for rb1 in get_players(rb1s, remaining_salary) if not lineup['rb1'] else [lineup['rb1']]:
            remaining_salary -= rb1.salary

            if rb1 in rb2s:
                rb2s.remove(rb1)

            if FLEX_OPTION != 1:
                flexes = rb2s[:]

            for rb2 in get_players(rb2s, remaining_salary) if not lineup['rb2'] else [lineup['rb2']]:
                remaining_salary -= rb2.salary
                wr1s = wrs[:]
                wr2s = wrs[:]
                wr3s = wrs[:]

                if FLEX_OPTION != 1 and rb2 in flexes:
                    flexes.remove(rb2)

                for wr1 in get_players(wr1s, remaining_salary) if not lineup['wr1'] else [lineup['wr1']]:
                    remaining_salary -= wr1.salary

                    if wr1 in wr2s:
                        wr2s.remove(wr1)
                    if wr1 in wr3s:
                        wr3s.remove(wr1)

                    for wr2 in get_players(wr2s, remaining_salary) if not lineup['wr2'] else [lineup['wr2']]:
                        remaining_salary -= wr2.salary

                        if wr2 in wr3s:
                            wr3s.remove(wr2)

                        flexes = flexes + [wr for wr in wr3s if wr not in flexes] if FLEX_OPTION != 1 else wr3s[:]

                        for wr3 in get_players(wr3s, remaining_salary) if not lineup['wr3'] else [lineup['wr3']]:
                            remaining_salary -= wr3.salary

                            if wr3 in flexes:
                                flexes.remove(wr3)

                            if FLEX_OPTION == 3:
                                flexes += [te for te in tes if te not in flexes]

                            for te in get_players(tes, remaining_salary) if not lineup['te'] else [lineup['te']]:
                                remaining_salary -= te.salary

                                if FLEX_OPTION == 3 and te in flexes:
                                    flexes.remove(te)

                                for flex in flexes if not lineup['flex'] else [lineup['flex']]:
                                    if flex.name in [p.name for p in [rb1, rb2, wr1, wr2, wr3, te]]:
                                        continue

                                    remaining_salary -= flex.salary

                                    for d in get_players(defenses, remaining_salary) if not lineup['dst'] else [lineup['dst']]:
                                        remaining_salary -= d.salary
                                        l = {'qb' : qb, 'rb1' : rb1, 'rb2' : rb2, 'wr1' : wr1, 'wr2' : wr2, 'wr3' : wr3, 'flex': flex, 'te' : te, 'dst' : d}
                                        total_points = int(sum([p.points for p in l.values()]) * 10) / 10
                                        total_salary = MAX_SAL - remaining_salary

                                        if total_salary <= MAX_SAL:
                                            yield l, total_points, total_salary

                                        remaining_salary += d.salary
                                    remaining_salary += flex.salary
                                remaining_salary += te.salary
                            remaining_salary += wr3.salary
                        remaining_salary += wr2.salary
                    remaining_salary += wr1.salary
                remaining_salary += rb2.salary
            remaining_salary += rb1.salary
        remaining_salary += qb.salary

if __name__ == '__main__':
    qbs = []
    rbs = []
    wrs = []
    tes = []
    defenses = []
    lineup = { 'qb' : None, 'rb1' : None, 'rb2' : None, 'wr1' : None,
               'wr2' : None, 'wr3' : None, 'flex': None, 'te' : None, 'dst' : None }

    read_player_data(qbs, rbs, wrs, tes, defenses)
    qbs, rbs, wrs, tes, defenses = sort_player_data(qbs, rbs, wrs, tes, defenses)
    #adjust_projections(qbs, rbs, wrs, tes, defenses)

    customize = input("Do you want to add/exclude players to/from your lineup? (y/n) ")

    if customize == 'y':
        qbs, rbs, wrs, tes, defenses = customize_optimization(qbs, rbs, wrs, tes, defenses, lineup)
    else:
        print('\n\n')

    #qbs, rbs, wrs, tes, defenses = remove_suboptimal_players(qbs, rbs, wrs, tes, defenses)
    lineups = []

    minPoints = 999

    for lineup, points, salary in generate_lineups(qbs, rbs, wrs, tes, defenses, lineup):
        if len(lineups) < MAX_LINEUPS:
            l = Lineup(lineup['qb'], lineup['rb1'], lineup['rb2'], lineup['wr1'], lineup['wr2'], lineup['wr3'], lineup['te'], lineup['flex'], lineup['dst'], points, salary)
            heapq.heappush(lineups, l)
            minPoints = points if points < minPoints else minPoints
        elif points > minPoints:
            l = Lineup(lineup['qb'], lineup['rb1'], lineup['rb2'], lineup['wr1'], lineup['wr2'], lineup['wr3'], lineup['te'], lineup['flex'], lineup['dst'], points, salary)
            heapq.heappushpop(lineups, l)
            minPoints = lineups[0].points

    for l in heapq.nlargest(MAX_LINEUPS, lineups):
        print(f'{l.display_lineup()}\n')
