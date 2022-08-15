import argparse
import json
import random
from datetime import date, datetime, timedelta


def generate_mondays_until_date(to_date: date):
    d = date.today()
    d = d + timedelta(days=-d.weekday(), weeks=1)  ## set date to next monday
    if to_date < d:
        raise ValueError(f"Date to generate data to is in the past {to_date=}")
    while d < to_date:
        yield d.strftime("%d %B %Y")
        d += timedelta(days=7)


def generate_dict(values, to_date=date(year=date.today().year, month=12, day=31)):
    if len(set(values)) != len(values):
        raise ValueError(f"List of objects has a duplicate {values=}")
    dct = {}
    r = None
    for monday in generate_mondays_until_date(to_date):
        while not r:
            r = random.sample(values, len(values))
            if dct and list(dct.values())[-1] == r[0]:
                r = None
        dct[monday] = r[0]
        r.remove(dct[monday])

    return dct

def convert_date(d):
    return  datetime.strptime(d, '%d/%m/%Y').date()


def main():
    parser = argparse.ArgumentParser(description="Small script to randomize team members assigned to support")
    parser.add_argument('--names', type=str, nargs='+',
                        help='List of names to generate. Separated by space')
    parser.add_argument('--date', type=convert_date,
                    help='Date until you want the list to be generated: Must be in format DD/MM/YYYY')

    args = parser.parse_args()
    if not args.names:
        raise ValueError("You need to provide a list of names")
    values = args.names
    to_date = date(year=date.today().year, month=12, day=31) if not args.date else args.date
    dict_str = '\n'.join([f"{k}: {v}" for k, v in generate_dict(values, to_date).items()])
    print(dict_str)
    with open('round_robin.txt', 'w') as f:
        f.write(dict_str)



if __name__ == "__main__":
    main()
