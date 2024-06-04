"""
    Scripts for generating questions for the DiMeN data challenge.
    Each question should have two functions, one to generate the data for the question, and one to generate the solution.
    Function names should be the same as the question.
"""

from pathlib import Path
import random
import shutil
import pandas as pd
import faker
import numpy as np
from scipy import stats
from statsmodles.formula.api import ols
import statsmodels as sm


def expression_expedition():

    # Load the data
    data = pd.read_csv("./genes.csv")

    # Generate gene expression data
    means = np.random.uniform(10, 1000, len(data))
    means = means.reshape(-1, 1)
    means = np.tile(means, 10)

    means *= np.random.triangular(0.5, 1, 2, means.shape)
    means = pd.DataFrame(means, columns=[f"Sample_{i}" for i in range(10)])

    # Choose 5 random genes
    means = pd.concat([data, means], axis=1)
    genes = np.random.choice(data["symbol"], 5)

    print("Solution to Expression Expedition:")
    print(sorted(genes.tolist()))
    means.loc[
        means["symbol"].isin(genes.tolist()[:3]), [f"Sample_{i}" for i in range(5, 10)]
    ] *= np.random.uniform(2**7, 2**8, (3, 5))

    means.loc[
        means["symbol"].isin(genes.tolist()[3:]), [f"Sample_{i}" for i in range(5, 10)]
    ] /= np.random.uniform(2**7, 2**8, (2, 5))

    # Save the data
    means.to_csv("./expression_expedition_data.csv", index=False)

    with open("./expression_expedition_val_sol.txt", "w") as f:
        f.write("\n".join(genes.tolist()))

    data = pd.read_csv("./expression_expedition_data.csv")

    log_data = np.log2(data.iloc[:, 1:])

    lfc = log_data.iloc[:, 5:].mean(axis=1) - log_data.iloc[:, :5].mean(axis=1)
    p_val = stats.ttest_ind(log_data.iloc[:, 5:], log_data.iloc[:, :5], axis=1)[1]

    results = pd.DataFrame({"symbol": data["symbol"], "LFC": lfc, "p_val": p_val})

    results["abs_lfc"] = np.abs(results["LFC"])


def heartbeat_hero():

    fak = faker.Faker()
    data_folder = Path("./heartbeat_hero_data")

    # Delete folder if it exists
    if data_folder.exists():
        shutil.rmtree(data_folder)

    data_folder.mkdir(exist_ok=True)
    mean_qts = {}

    for i in range(10):

        name = fak.name()

        labels = ["P", "Q", "R", "S", "T"] * 100
        values = np.random.uniform(10, 100, len(labels))

        mean_qt = np.mean([sum(values[i + 1 : i + 4]) for i in range(100)])

        data = pd.DataFrame({"label": labels, "value": values})
        data.to_csv(data_folder / f"./{name}.csv", index=False)

        mean_qts[name] = mean_qt

    qts = pd.DataFrame(mean_qts.items(), columns=["Name", "Mean_QT"])
    qts = qts.sort_values("Mean_QT", ascending=False).head(1)

    # Zip heartbeat folder
    shutil.make_archive("./heartbeat_hero_data", "zip", data_folder)

    with open("./heartbeat_hero_sol.txt", "w") as f:
        f.write(qts["Name"].values[0])


def monkey_masses():
    """
    Generate data for the Monkey Masses question
    """
    mean_1 = np.random.uniform(10, 30)
    mean_2 = np.random.uniform(10, 30)

    if mean_1 > mean_2:
        mean_1, mean_2 = mean_2, mean_1

    std_1 = np.random.uniform(1, 2)
    std_2 = np.random.uniform(1, 2)

    inactive_monkeys = np.random.normal(mean_1, std_1, 100)
    active_monkeys = np.random.normal(mean_2, std_2, 100)

    data = pd.DataFrame({"gym_provided": active_monkeys, "no_gym": inactive_monkeys})

    data.to_csv("./monkey_masses.csv")

    # Solution
    pval = stats.ttest_ind(active_monkeys, inactive_monkeys)[1]

    with open("./monkey_masses_sol.txt", "w") as f:
        f.write(pval)


def sugar_squeeze_pt1():

    means = np.random.uniform(70, 150, 5)

    data = np.random.normal(means, 10, (5, 100))

    data = pd.DataFrame(data, columns=[f"Group {i+ 1}" for i in range(5)])

    data.to_csv("./sugar_squeeze_pt1.csv")

    pval = stats.f_oneway(data.values)[1]

    with open("./sugar_squeeze_pt1_sol.txt", "w") as f:
        f.write(pval)


def sugar_squeeze_pt2():

    means = np.random.uniform(70, 150, 25)

    data = np.random.normal(means, 10, (25, 100))

    sucrose_groups = [f"Group {(i % 5) + 1}" for i in range(25)]
    fructose_groups = [f"Group {(i // 5) + 1}" for i in range(25)]

    master_data = []
    for idx, (g1, g2) in enumerate(zip(sucrose_groups, fructose_groups)):
        for point in data[idx]:
            master_data.append([g1, g2, point])

    data = pd.DataFrame(
        master_data, columns=["Sucrose Group", "Fructose Group", "Weight (kg)"]
    )

    data.to_csv("./sugar_squeeze_pt2.csv")

    lm = ols(
        "Weight ~ C(Sucrose_Group) * C(Fructose_Group) + C(Sucrose_Group):C(Fructose_Group)",
        data,
    ).fit()

    table = sm.stats.anova_lm(lm, typ=2)

    # Table to text
    table.to_csv("./sugar_squeeze_pt2_sol.txt", sep="\t")


def drunk_dilemma():

    values = np.random.uniform(0, 100, (2, 2))

    data = pd.DataFrame(
        values, columns=["Sober", "Drinks"], index=["No Drugs", "Drugs"]
    )

    data.to_csv("./drunk_dilemma.csv")

    # Chi squared contigency table test
    pval = stats.fisher_exact(values)[1]

    with open("./drunk_dilemma_sol.txt", "w") as f:
        f.write(pval)


def nebulous_nucleotides():

    fak = faker.Faker()

    data_folder = Path("./nebulous_nucleotides")

    # Delete folder if it exists
    if data_folder.exists():
        shutil.rmtree(data_folder)

    best_name = ""
    best_count = 0

    for i in range(10):
        name = fak.name()

        string = np.random.choice(["A", "C", "G", "T"], 1000)
        string = "".join(string)

        count = string.count("ACGTGCA")
        if best_count < count:
            best_count = count
            best_name = name

        with open(f"./nebulous_nucleotides/{name}.txt", "w") as f:
            f.write(string)

    # Zip heartbeat folder
    shutil.make_archive("./nebulous_nucleotides", "zip", data_folder)

    with open("./nebulous_nucleotides_sol.txt", "w") as f:
        f.write(best_name)


def performance_pulse():

    x = np.random.uniform(5, 40, 100)
    m = np.random.uniform(1, 2)
    c = np.random.uniform(130, 140)
    y = m * x + c + np.random.normal(0, 10, 100)

    data = pd.DataFrame({"Speed (mph)": x, "Heart Rate": y})

    data.to_csv("./performance_pulse.csv")

    # Solution
    m, c, r, p, se = stats.linregress(x, y)

    with open("./performance_pulse_sol.txt", "w") as f:
        f.write(f"P-value: {p}")


def tricky_tests():

    x = np.random.exponential(5, 1000)

    data = pd.DataFrame({"Time (s)": x})

    data.to_csv("./tricky_tests.csv")

    # Solution
    pval = stats.shapiro(x)[1]

    with open("./tricky_tests_sol.txt", "w") as f:
        f.write(f"P-value: {pval}")


def response_riddle():

    x = np.random.normal(0, 1, 1000)
    y = np.random.lognormal(0, 1, 1000)

    data = pd.DataFrame({"Control": x, "Drug Positive": y})

    data.to_csv("./response_riddle.csv")

    # Solution
    # KS test
    ks_pval = stats.ks_2samp(x, y)[1]

    with open("./response_riddle_sol.txt", "w") as f:
        f.write(f"KS P-value: {ks_pval}")


def wicked_westerns():

    # Generate fake western data
    ladder = range(50, 250, 10)
    points = np.random.choice(ladder).tolist()
    question_gene = "PRDX"

    other_genes = np.random.choice(pd.read_csv("./genes.csv").to_numpy().flatten(), 9)
    housekeeper = 20
    names = random.shuffle(other_genes.tolist().append(question_gene))
    values = [housekeeper] + points

    data = []
    housekeeper_values = np.random.normal(200, 20, 20)
    control_values = np.random.normal(np.random.uniform(10, 100), 20, (10, 10))
    upreg_values = np.random.normal(np.random.uniform(100, 150), 20, (10, 10))

    all_values = np.hstack([control_values, upreg_values])
    all_values = np.vstack([housekeeper_values, all_values])

    all_values = {f"Cell {idx}": all_values[idx] for idx in range(20)}

    data_df = pd.DataFrame({"Gene": names, "Weights": values, **all_values})

    data_df.to_csv("wicked_westerns.csv")


if __name__ == "__main__":
    expression_expedition()
    heartbeat_hero()
    monkey_masses()
    sugar_squeeze_pt1()
    sugar_squeeze_pt2()
    drunk_dilemma()
    nebulous_nucleotides()
    performance_pulse()
    tricky_tests()
    response_riddle()
    wicked_westerns()
