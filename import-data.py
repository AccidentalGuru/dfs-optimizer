import csv
import dal

positions = ['qb', 'rb', 'wr', 'te', 'defense', 'kicker']
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
        reader = csv.reader(csv_file)
        header = next(reader)

        for row in reader:
            row.append(file['yr'])
            row.append(file['wk'])

            # Convert nulls to None to avoid issues when adding to DB
            for i in range(len(row)):
                if row[i] == 'null':
                    row[i] = None

            if file['pos'] == 'qb':
                dal.insert_qb_data(row)
            elif file['pos'] == 'rb':
                dal.insert_rb_data(row)
            elif file['pos'] == 'wr':
                dal.insert_wr_data(row)
            elif file['pos'] == 'te':
                dal.insert_te_data(row)
            elif file['pos'] == 'defense':
                dal.insert_defense_data(row)
            elif file['pos'] == 'kicker':
                dal.insert_kicker_data(row)

if __name__ == '__main__':
    for file in gen_csv_files():
        read_csv(file)
