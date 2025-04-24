import csv
from datetime import date
from pathlib import Path
import pytest

from project import create_csv, age_stats, pre_mun_stats, month_stats
# 🔁 Replace 'your_script' with the filename of your main Python script (without .py)


@pytest.fixture
def sample_txt(tmp_path):
    txt_file = tmp_path / "202304_newcomers.txt"  # ✅ FIX: using / instead of +
    content = (
        "f.aar;navn;adresse1;adresse2;postnr;poststed;flyttet;tidl.knr;tidl.k\n"
        "2020;Alice Smith;Street 1;;1000;CityA;2023-04-01;3413;Mun1\n"
        "2008;Bob Johnson;Street 2;;1001;CityB;2023-04-02;0301;Capital\n"
        "1985;Carol White;Street 3;;1002;CityC;2023-04-03;3420;Mun4\n"
        "1970;David Black;Street 4;;1003;CityD;2023-04-04;3411;Mun2\n"
        "1955;Eve Green;Street 5;;1004;CityE;2023-04-05;3412;Mun3\n"
    )
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


def test_create_csv_creates_valid_csv(sample_txt):
    file_name = sample_txt.stem
    create_csv(sample_txt, file_name)

    csv_file = sample_txt.parent + f"{file_name}.csv"
    assert csv_file.exists()

    with open(csv_file, newline="") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 5
        assert reader[0]["navn"] == "Alice Smith"
        assert reader[-1]["tidl.k"] == "Mun3"


def test_age_stats_output(sample_txt):
    file_name = sample_txt.stem
    create_csv(sample_txt, file_name)

    stats = age_stats(file_name=sample_txt.parent / file_name)
    assert "Age" in stats
    assert "TOTAL" in stats


def test_pre_mun_stats_output(sample_txt):
    file_name = sample_txt.stem
    create_csv(sample_txt, file_name)

    stats = pre_mun_stats(file_name=sample_txt.parent / file_name)
    assert "Municipality 1" in stats
    assert "Municipality 2" in stats
    assert "Capital" in stats


def test_month_stats_correct_month():
    file_name = "202304_newcomers"
    month = month_stats(file_name)
    assert month == "March"


def test_month_stats_wraparound():
    file_name = "202301_newcomers"
    month = month_stats(file_name)
    assert month == "December"
