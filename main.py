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


def generate_dict(values, to_date=date(year=date.today().year, month=12, day=31), previous_names=None):
    if len(set(values)) != len(values):
        raise ValueError(f"List of objects has a duplicate {values=}")
    dct = {}
    r = None
    for monday in generate_mondays_until_date(to_date):
        while not r:
            r = random.sample(values, len(values))
            if previous_names:
                [r.remove(name) for name in previous_names]
                previous_names = None
            if dct and list(dct.values())[-1] == r[0]:
                r = None
        dct[monday] = r[0]
        r.remove(dct[monday])

    return dct


def convert_date(d):
    return datetime.strptime(d, "%d/%m/%Y").date()

def get_reverse_sublist_until_repeat(l):
    unique_l = []
    for i in l:
        if i in unique_l:
            return l
        else:
            unique_l.append(i)
def deserialise_file(file):
    with open(file, "r+") as f:
        return get_reverse_sublist_until_repeat([
            r.split(":")[1].strip()
            for r in f.readlines()
            if datetime.strptime(r.split(":")[0], "%d %B %Y") < date.today()
        ])


def main():
    parser = argparse.ArgumentParser(
        description="Small script to randomize team members assigned to support"
    )
    parser.add_argument(
        "--names",
        type=str,
        nargs="+",
        help="List of names to generate. Separated by space",
    )
    parser.add_argument(
        "--date",
        type=convert_date,
        help="Date until you want the list to be generated: Must be in format DD/MM/YYYY",
    )
    previous_names_args = parser.add_mutually_exclusive_group()
    previous_names_args.add_argument(
        "--previous_names", type=str, nargs="+", help="List of names to ignore in the last generation. Must be separated by spaces"
    )
    previous_names_args.add_argument(
        "--previous_names_file", type=str, help="previous round robin file"
    )

    args = parser.parse_args()
    if not args.names:
        raise ValueError("You need to provide a list of names")
    previous_names = None
    if args.previous_names:
        if [name for name in args.previous_names if name not in args.names]:
            raise ValueError(f"{args.previous_names=} not inclusive in {args.names=}")
        previous_names = args.previous_names
    if args.previous_names_file:
        previous_names = deserialise_file(args.previous_file_name)
    to_date = (
        date(year=date.today().year, month=12, day=31) if not args.date else args.date
    )
    dict_str = "\n".join(
        [
            f"{k}: {v}"
            for k, v in generate_dict(args.names, to_date, previous_names).items()
        ]
    )
    print(dict_str)
    with open("round_robin.txt", "w") as f:
        f.write(dict_str)


if __name__ == "__main__":
    main()
