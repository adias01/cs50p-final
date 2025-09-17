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
cwd_text_files = cwd / "text_files"
cwd_csv_files = cwd / "csv_files"

def validate_txtfile(file_name, file_ext):
    if file_ext != ".txt":
        sys.exit(f"ERROR: {file_name}{file_ext} is not a text file")

    try:
        with open(f"{cwd_text_files}\\{file_name}{file_ext}") as file:
            file.readable
    except OSError:
        sys.exit(f"ERROR: {file_name}{file_ext} could not be read")


def convert_to_csv(file_name, file_ext):
    txtfile = cwd_text_files / f"{file_name}{file_ext}"
    file_name = Path(file_name)
    
    file_path = cwd_csv_files / f"{file_name.stem}.csv"
    with open(txtfile, encoding="utf-8") as txt, open(file_path, "w", encoding="utf-8", newline="") as csvf:
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
                    item = "N/A"

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
    file_path = Path(f"{cwd_csv_files}/{file_name}.csv") if isinstance(file_name, str) else file_name.with_suffix(".csv")
    with open(file_path, encoding="utf-8") as file:
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
        
    return total, age_0_5, age_6_19, age_20_44, age_45_66, age_67_etc


def pre_mun_stats(file_name):
    file_path = Path(f"{cwd_csv_files}/{file_name}.csv") if isinstance(file_name, str) else file_name.with_suffix(".csv")
    with open(file_path, encoding="utf-8") as file:
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

    return stange, ringsaker, loten, elverum, oslo

def month_stats(file_name):
    months = {
        1: "januar",
        2: "februar",
        3: "mars",
        4: "april",
        5: "mai",
        6: "juni",
        7: "juli",
        8: "august",
        9: "september",
        10: "oktober",
        11: "november",
        12: "desember"
        }
    
    month_no = int(file_name[4:6]) - 1
    if month_no == 0:
        month_no = 12
    
    month_name = months.get(month_no)
    return month_name 

def main():
    fieldnames = [
        "måned", "antall innflyttere",
        "0-5", "6-19", "20-44", "45-66", "67+",
        "stange", "ringsaker", "løten", "elverum", "oslo"
    ]
    with open("statistikk_innflyttere.csv", "w", encoding="utf-8", newline="") as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        writer.writeheader()
        

        for file in cwd_text_files.glob("**/*.txt"):
            file_path, file_ext = os.path.splitext(file)
            file_name = file_path.split("\\")[-1]

            validate_txtfile(file_name, file_ext)
            convert_to_csv(file_name, file_ext)

            month = month_stats(file_name) 

            total, age_0_5, age_6_19, age_20_44, age_45_66, age_67_etc = age_stats(file_name)
            stange, ringsaker, loten, elverum, oslo = pre_mun_stats(file_name)

            writer.writerow(
                {
                "måned": month, 
                "antall innflyttere": total,
                "0-5": age_0_5,
                "6-19": age_6_19,
                "20-44": age_20_44,
                "45-66": age_45_66,
                "67+": age_67_etc,
                "stange": stange,
                "ringsaker": ringsaker,
                "løten": loten,
                "elverum": elverum,
                "oslo": oslo
                }
            )

    with open("statistikk_innflyttere.csv", encoding="utf-8") as csvf:
        reader = csv.DictReader(csvf)
        stat_dict = [row for row in reader]
        print("\n", tabulate(stat_dict, headers="keys", tablefmt="grid"), "\n")

if __name__ == "__main__":
    main()
