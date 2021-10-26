import anonypy
import pandas as pd

data = [
    [6, "1", "test1", "x", 20],
    [6, "1", "test1", "x", 30],
    [8, "2", "test2", "x", 50],
    [8, "2", "test3", "w", 45],
    [8, "1", "test2", "y", 35],
    [4, "2", "test3", "y", 20],
    [4, "1", "test3", "y", 20],
    [2, "1", "test3", "z", 22],
    [2, "2", "test3", "y", 32],
]

columns = ["col1", "col2", "col3", "col4", "col5"]
categorical = set(("col2", "col3", "col4"))


def test_k_anonymity():
    df = pd.DataFrame(data=data, columns=columns)
    print(df)

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"

    p = anonypy.Preserver(df, feature_columns, sensitive_column)
    rows = p.anonymize_k_anonymity(k=2)

    dfn = pd.DataFrame(rows)
    print(dfn)


def test_count_k_anonymity():
    df = pd.DataFrame(data=data, columns=columns)
    print(df)

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"

    p = anonypy.Preserver(df, feature_columns, sensitive_column)
    rows = p.count_k_anonymity(k=2)

    dfn = pd.DataFrame(rows)
    print(dfn)


def test_l_diversity():
    df = pd.DataFrame(data=data, columns=columns)

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"

    p = anonypy.Preserver(df, feature_columns, sensitive_column)
    rows = p.anonymize_l_diversity(k=2, l=2)

    dfn = pd.DataFrame(rows)
    print(dfn)


def test_t_closeness():
    df = pd.DataFrame(data=data, columns=columns)

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"

    p = anonypy.Preserver(df, feature_columns, sensitive_column)
    rows = p.anonymize_t_closeness(k=2, p=0.2)

    dfn = pd.DataFrame(rows)
    print(dfn)
