import argparse
import csv
import pyfiglet
import os
import sys

from datetime import date
from pathlib import Path
from tabulate import tabulate, SEPARATING_LINE

cwd = Path.cwd()

def parse_arg():
    parser = argparse.ArgumentParser(
        usage="Generate statistics on the municipality's new citizens related"
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
            ["0 - 5 år", age_0_5],
            ["6 - 19 år", age_6_19],
            ["20 - 44 år", age_20_44],
            ["45 - 66 år", age_45_66],
            ["67+ år", age_67_etc],
            SEPARATING_LINE,
            ["TOTAL", total]
        ]
        headers = ["Alder", "Antall"]
        
        return tabulate(table, headers=headers, tablefmt="simple")


def pre_mun_stats(file_name):
    with open(f"{cwd}/{file_name}.csv") as file:
        reader = csv.DictReader(file)

        stange = 0
        ringsaker = 0
        loten = 0
        elverum = 0
        oslo = 0

        for row in reader:
            mun_no = row["tidl.knr"]

            if mun_no == "3413":
                stange += 1

            elif mun_no == "3411":
                ringsaker += 1

            elif mun_no == "3412":
                loten += 1

            elif mun_no == "3420":
                elverum += 1

            elif mun_no == "0301":
                oslo += 1

        table = [
            ["Stange", stange],
            ["Ringsaker", ringsaker],
            ["Løten", loten],
            ["Elverum", elverum],
            ["Oslo", oslo],
        ]
        headers = ["Kommune", "Antall"]
        
        return tabulate(table, headers=headers, tablefmt="simple")


def month_stats(file_name):
    months = {
        1: "Januar",
        2: "Februar",
        3: "Mars",
        4: "April",
        5: "Mai",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember"
        }
    
    month_no = int(file_name[4:6]) - 1
    if month_no == 0:
        month_no == 12
    
    month_name = months.get(month_no)
    return month_name 


def main():
    args = parse_arg()  
    txtfile = args.file

    file_name, file_ext = os.path.splitext(txtfile)

    validate_txtfile(txtfile, file_ext)
    create_csv(txtfile, file_name)

    month = month_stats(file_name) 

    print(
        f"{pyfiglet.figlet_format(month, font="small")}\n"
        f"{age_stats(file_name)}\n\n"
        f"{pre_mun_stats(file_name)}\n"
        )


if __name__ == "__main__":
    main()