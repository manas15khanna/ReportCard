import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
import subprocess
import os

# Some fixed rules for the CSV:
# Must have a Name column, roll number column,
# and the rest of the columns would be subjects and marks.
path = input("Enter the path to the CSV file: ")

data = pd.read_csv(path)
subjects = [x for x in data.columns if x != "name" and x != "roll_no"]

for i in subjects:
    data[f'rank_{i}'] = data[i].rank(method='min',ascending=False)

data['average_score'] = data[subjects].mean(axis=1)
data['rank'] = data['average_score'].rank(method="min", ascending=False)


env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.tex')

function_dict = {"min": min}
template.globals.update(function_dict)

os.system("mkdir out || rm out/*")
os.system("mkdir charts || rm charts/*")

# Generating Graphs...
for i in subjects:
    counts, bins, patches = plt.hist(data[i], bins=[0, 5, 10, 15, 20, 25], color='skyblue')

    for j in range(5):
        for k in range(j):
            patches[k].set_facecolor('skyblue')
        patches[j].set_facecolor('blue')

        plt.xlabel(i)
        plt.ylabel("Frequency")
        plt.savefig(f"charts/{i}_{j}.png")
    plt.cla()

for index, row in data.iterrows():
    latex_code = template.render(
        name=row['name'],
        roll_no=row['roll_no'],
        length=len(subjects),
        subjects=subjects,
        scores=row[subjects],
        subrank=row[[f"rank_{i}" for i in subjects]],

        average_score=row['average_score'],
        rank=row['rank']
    )

    with open(f"out/report_card_{row['roll_no']}.tex", 'w') as f:
        f.write(latex_code)

    # Compile LaTeX
    subprocess.run(['pdflatex', '-output-directory=out', f"out/report_card_{row['roll_no']}.tex"])
    subprocess.run(['rm', f'out/report_card_{row['roll_no']}.aux'])
    subprocess.run(['rm', f'out/report_card_{row['roll_no']}.log'])
    subprocess.run(['rm', f'out/report_card_{row['roll_no']}.tex'])

