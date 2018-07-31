import csv
from app import db
from db import Player_Game_Stats

positions = ['qb', 'rb', 'wr', 'te']#, 'defense', 'kicker']
years = ['2015', '2016', '2017'] # last 3 seasons


def gen_csv_files():
    # Generate list of csv files

    file = dict()
    for pos in positions:
        for yr in years:
            for wk in range(18):
                if wk == 0:
                    name = f'data/{pos}s-{yr}.csv'
                    wk = None  # total season stats
                elif pos == 'kicker':  # right now only track season stats for kickers so skip other weeks
                    continue
                else:
                    name = f'data/{pos}s-{yr}-wk{wk}.csv'

                file = {
                    'name': name,
                    'yr' : yr,
                    'wk' : wk,
                    'pos' : pos
                }
                yield file


def read_csv(file):
    # Read a csv file, insert data into db

    with open(file['name']) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            row['yr'] = file['yr']
            row['wk'] = file['wk']
            row['pos'] = file['pos']

            # Convert nulls to None to avoid issues when adding to DB
            for i in range(len(row)):
                if row[i] == 'null':
                    row[i] = None

            if file['pos'] not in ['kicker', 'defense']:
                Player_Game_Stats.stats_from_dict(row)


if __name__ == '__main__':
    for file in gen_csv_files():
        read_csv(file)
