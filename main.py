import pandas as pd
from jinja2 import Environment, FileSystemLoader
import subprocess

# Some fixed rules for the CSV:
# Must have a Name column, roll number column,
# and the rest of the columns would be subjects and marks.
path = input("Enter the path to the CSV file: ")

data = pd.read_csv(path)
subjects = [x for x in data.columns if x != "name" and x != "roll_no"]
ranks = []

for i in subjects:
    data[f'rank_{i}'] = data[i].rank(ascending=False)

data['average_score'] = data[subjects].mean(axis=1)
data['rank'] = data['average_score'].rank(ascending=False)

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.tex')

for index, row in data.iterrows():
    latex_code = template.render(
        name=row['name'],
        roll_no=row['roll_no'],
        subjects=subjects,
        score=row[subjects],
        subrank=row[[f"rank_{i}" for i in subjects]],

        average_score=row['average_score'],
        rank=row['rank']
    )

    with open(f"report_card_{row['roll_no']}.tex", 'w') as f:
        f.write(latex_code)

    # Compile LaTeX
    subprocess.run(['pdflatex', f"report_card_{row['roll_no']}.tex"])
