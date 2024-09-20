import anonypy
from anonypy import attack
import pandas as pd


columns = [f"col{i+1}" for i in range(12)]
categorical = set(("col1", "col3", "col4", "col5", "col11"))


def test_attack():

    types = {
        "col1": str,
        "col2": float,
        "col3": str,
        "col4": str,
        "col5": str,
        "col6": float,
        "col7": int,
        "col8": int,
        "col9": int,
        "col10": int,
        "col11": str,
        "col12": int,
    }

    df = pd.read_csv("data/NHANES.csv", header=None, names=columns, dtype=types)
    print(f"\n{df.head()}")
    print(df.dtypes)

    df_attack = pd.read_csv(
        "data/NHANES_attack.csv", header=None, names=columns, dtype=types
    )
    print(f"\n{df_attack.head()}")

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"

    p = anonypy.Preserver(df, feature_columns, sensitive_column)
    rows = p.count_k_anonymity(k=2)

    # Anonymized data
    dfn = pd.DataFrame(rows).loc[:, ["col1", "col2", "col3"]]

    # this is attackers knowledge
    knowledge = df_attack.loc[:, ["col1", "col2", "col3"]]

    rl = attack.attack(dfn, knowledge)
    print(rl)
