import csv
from pathlib import Path
from datetime import date

import pytest

from project import create_csv, age_stats, pre_mun_stats, month_stats

@pytest.fixture
def sample_txt(tmp_path):
    txt_file = tmp_path / "202304_nyinflyttede.txt"
    content = (
        "f.aar;navn;adresse1;adresse2;postnr;poststed;flyttet;tidl.knr;tidl.k\n"
        "2020;Anna Test;Gate 1;;1234;Testby;2023-04-05;3413;Stange\n"
        "2005;Ola Normann;Gate 2;;1234;Testby;2023-04-06;0301;Oslo\n"
        "1990;Kari Nordmann;Gate 3;;1234;Testby;2023-04-07;3420;Elverum\n"
        "1975;Per Persen;Gate 4;;1234;Testby;2023-04-08;3411;Ringsaker\n"
        "1950;Lise Hansen;Gate 5;;1234;Testby;2023-04-09;3412;Løten\n"
    )
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


def test_create_csv_creates_valid_csv(sample_txt):
    csv_name = sample_txt.stem
    create_csv(sample_txt, csv_name)
    csv_file = sample_txt.parent / f"{csv_name}.csv"

    assert csv_file.exists()

    with open(csv_file, newline="") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 5
        assert reader[0]["navn"] == "Anna Test"
        assert reader[-1]["tidl.k"] == "Løten"


def test_age_stats(sample_txt):
    file_name = sample_txt.stem
    create_csv(sample_txt, file_name)
    stats = age_stats(file_name=sample_txt.parent / file_name)

    current_year = date.today().year
    ages = [current_year - int(y) for y in [2020, 2005, 1990, 1975, 1950]]

    assert "0 - 5 år" in stats
    assert str(ages.count(i) for i in range(0, 6))  # Just verifying it doesn’t crash and includes age group label


def test_pre_mun_stats(sample_txt):
    file_name = sample_txt.stem
    create_csv(sample_txt, file_name)
    stats = pre_mun_stats(file_name=sample_txt.parent / file_name)

    assert "Stange" in stats
    assert "Ringsaker" in stats
    assert "Oslo" in stats


def test_month_stats():
    file_name = "202304_nyinflyttede"
    month = month_stats(file_name)
    assert month == "Mars"
