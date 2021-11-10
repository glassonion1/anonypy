import anonypy
import pandas as pd
from datetime import datetime, date


def calculate_age(born):
    born = datetime.strptime(born, "%Y/%m")
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def test_receipt():
    path = "data/receipt.csv"
    df = pd.read_csv(path)

    # カテゴリ属性の設定
    categorical = set(
        (
            "r_type",
            "sex",
            "family",
            "icd10",
        )
    )
    for name in categorical:
        df[name] = df[name].astype("category")

    print(len(df))
    print(df.head())

    df["birth_ym"] = df["birth_ym"].map(lambda x: calculate_age(x))

    feature_columns = ["sex", "family", "birth_ym"]
    sensitive_column = "iid"

    p = anonypy.Preserver(df, feature_columns, sensitive_column)
    rows = p.anonymize_k_anonymity(k=2)

    dfn = pd.DataFrame(rows)
    print(len(dfn))
    print(dfn.head())
