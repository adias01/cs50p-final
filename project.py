import argparse
import csv
import pyfiglet
import os
import sys

from datetime import date
from pathlib import Path
from rich.console import Console 
from tabulate import tabulate, SEPARATING_LINE

cwd = Path.cwd()

def parse_arg():
    parser = argparse.ArgumentParser(
        usage="Generates statistics on the municipality's new citizens"
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="text (.txt) file containing data on the newcomers"
    )
    return parser.parse_args()


def validate_txtfile(txtfile, file_ext):
    if file_ext != ".txt":
        sys.exit(f"ERROR: {txtfile} is not a text file")

    try:
        with open(txtfile) as file:
            file.readable
    except OSError:
        sys.exit(f"ERROR: {txtfile} could not be read")


def create_csv(txtfile, file_name):
    with open(txtfile) as txt, open(f"{cwd}/{file_name}.csv", "w", newline="") as csvf:
        reader = txt.readlines()
        reader.pop(0)

        fieldnames = [
            "f.aar",
            "navn",
            "adresse1",
            "adresse2",
            "postnr",
            "poststed",
            "flyttet",
            "tidl.knr",
            "tidl.k",
        ]
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            newcomer = row.split(";")

            for item in newcomer:
                if item == "":
                    item == "N/A"

            year, name, address1, address2, zipcode, city, moved, pre_mun_no, pre_mun = (
                newcomer
            )
            writer.writerow(
                {
                    "f.aar": year,
                    "navn": name,
                    "adresse1": address1,
                    "adresse2": address2,
                    "postnr": zipcode,
                    "poststed": city,
                    "flyttet": moved,
                    "tidl.knr": pre_mun_no,
                    "tidl.k": pre_mun.removesuffix("\n"),
                }
            )


def age_stats(file_name):
    with open(f"{cwd}/{file_name}.csv") as file:
        today = date.today()
        this_year = today.year

        reader = csv.DictReader(file)

        age_0_5 = 0
        age_6_19 = 0
        age_20_44 = 0
        age_45_66 = 0
        age_67_etc = 0

        for row in reader:
            age = this_year - int(row["f.aar"])

            if 0 <= age <= 5:
                age_0_5 += 1

            elif 6 <= age <= 19:
                age_6_19 += 1

            elif 20 <= age <= 44:
                age_20_44 += 1

            elif 45 <= age <= 66:
                age_45_66 += 1

            elif 67 <= age:
                age_67_etc += 1

        total = age_0_5 + age_6_19 + age_20_44 + age_45_66 + age_67_etc

        table = [
            ["0 - 5", age_0_5],
            ["6 - 19", age_6_19],
            ["20 - 44", age_20_44],
            ["45 - 66", age_45_66],
            ["67+", age_67_etc],
            SEPARATING_LINE,
            ["TOTAL", total]
        ]
        headers = ["Age", "Amount"]
        
        return tabulate(table, headers=headers, tablefmt="simple")


def pre_mun_stats(file_name):
    with open(f"{cwd}/{file_name}.csv") as file:
        reader = csv.DictReader(file)

        mun1 = 0
        mun2 = 0
        mun3 = 0
        mun4 = 0
        capital = 0

        for row in reader:
            mun_no = row["tidl.knr"]

            if mun_no == "3413":
                mun1 += 1

            elif mun_no == "3411":
                mun2 += 1

            elif mun_no == "3412":
                mun3 += 1

            elif mun_no == "3420":
                mun4 += 1

            elif mun_no == "0301":
                capital += 1

        table = [
            ["Municipality 1", mun1],
            ["Municipality 2", mun2],
            ["Municipality 3", mun3],
            ["Municipality 4", mun4],
            ["Capital", capital],
        ]
        headers = ["Municipality", "Amount"]
        
        return tabulate(table, headers=headers, tablefmt="simple")


def month_stats(file_name):
    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
        }
    
    month_no = int(file_name[4:6]) - 1
    if month_no == 0:
        month_no = 12
    
    month_name = months.get(month_no)
    return month_name 


def main():
    console = Console()
    args = parse_arg()  
    txtfile = args.file

    file_name, file_ext = os.path.splitext(txtfile)

    validate_txtfile(txtfile, file_ext)
    create_csv(txtfile, file_name)

    month = month_stats(file_name) 

    console.print(
        f"{pyfiglet.figlet_format(month, font="small")}\n"
        f"[bold]Age of new residents:[/bold]\n"
        f"{age_stats(file_name)}\n\n"
        f"[bold]Number of new residents who have moved from[/bold]\n"
        f"[bold]neighboring municipalities and the capital:[/bold]\n"
        f"{pre_mun_stats(file_name)}\n"
        )


if __name__ == "__main__":
    main()
