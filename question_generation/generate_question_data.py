"""
    Scripts for generating questions for the DiMeN data challenge.
    Each question should have two functions, one to generate the data for the question, and one to generate the solution.
    Function names should be the same as the question.
"""

from pathlib import Path
import shutil
import pandas as pd
import faker
import numpy as np
from scipy import stats


def expression_expedition_q():

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


def expression_expedition_sol():

    data = pd.read_csv("./expression_expedition_data.csv")

    log_data = np.log2(data.iloc[:, 1:])

    lfc = log_data.iloc[:, 5:].mean(axis=1) - log_data.iloc[:, :5].mean(axis=1)
    p_val = stats.ttest_ind(log_data.iloc[:, 5:], log_data.iloc[:, :5], axis=1)[1]

    results = pd.DataFrame({"symbol": data["symbol"], "LFC": lfc, "p_val": p_val})

    results["abs_lfc"] = np.abs(results["LFC"])


def heartbeat_hero_q():

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

    print(mean_qts)


if __name__ == "__main__":
    # expression_expedition_q()
    # expression_expedition_sol()

    heartbeat_hero_q()
