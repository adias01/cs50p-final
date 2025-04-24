# Municipal Newcomer Statistics Tool
Author: [@adias01](https://github.com/adias01)
#### Video Demo:  <URL HERE>
#### Description:
A Python program that uses CLI to parse a text (.txt) file containing data on a municipality's new citizens, converts it to a CSV file for further processing and then outputs two formatted tables and ASCII art for the corresponding month.

The first table shows the age of the newcomers, whereas the second table shows how many newcomers come from other municipalities in the region, in addition to the capital.

### Features:
- Converts a .txt file with newcomer data into a .csv file.
- Calculates age distribution of new residents.
- Shows how many people have moved from municipalities of interest.
- Displays results in a visually clear format using tabulate and rich.
- Highlights the month of the data file using ASCII art via pyfiglet.

### Clarifications / Known Limitations:
The program...
- assumes the name of the text file begins with year and month, in the following format: YYYYMM.
- assumes the text file's data set is for det previous month, meaning a text file named 202504.txt contains data for March 2025.
- assumes the text file contains columns separated by semicolons and containing year of birth, name, address 1, address 2, zip code, city, date of moving, the municipality of origin's identification number and the name of the municipality (in the respective order mentioned).
- only handles municipalities pre-defined by their identification number.

### Requirements:
#### Interpreter:
- Python 3

#### Python Standard Libraries:
- argparse
- csv
- datetime
- os
- pathlib
- sys

#### External Libraries:
- pyfiglet
- rich
- tabulate
  
 ```bash
 # For installing required libraries
 pip install -r requirements.txt
 ```

### Usage:
<ul>
<li><b>Input:</b> You provide a .txt file as a command-line argument.</li>

```bash
python project.py -f 202504.txt
```

<li><b>Validation:</b> The script checks if the file is readable and a .txt file.</li>
<li><b>Conversion:</b> Data is written to a .csv with headers.</li>
<li><b>Analysis:</b>
    <ul>
        <li>Age groups are calculated based on the birth year.</li>
        <li>The number of newcomers coming from municipalities of interest is categorized.</li>
    </ul>
<li><b>Output:</b> Results are displayed in the terminal with tables and formatted headings. The data's corresponding month is displayed in ASCII art at the top.</li>

![Visual presentation of project output](assets/images/project_output.png)




