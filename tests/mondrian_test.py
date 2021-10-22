import anonypy
from anonypy import util
import pandas as pd

names = (
    "age",
    "workclass",  # Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
    "fnlwgt",  # "weight" of that person in the dataset (i.e. how many people does that person represent) -> https://www.kansascityfed.org/research/datamuseum/cps/coreinfo/keyconcepts/weights
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
    "income",
)

categorical = set(
    (
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "relationship",
        "sex",
        "native-country",
        "race",
        "income",
    )
)


def test_k_anonymity():
    data = [
        [6, "1", "test1", "x", 20],
        [6, "1", "test1", "y", 30],
        [8, "2", "test2", "x", 50],
        [8, "2", "test3", "x", 45],
        [8, "1", "test2", "y", 35],
        [4, "2", "test3", "y", 20],
    ]
    df = pd.DataFrame(data=data, columns=["col1", "col2", "col3", "col4", "col5"])
    print(df)

    categorical = set(("col2", "col3", "col4"))
    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"
    m = anonypy.Mondrian(df, feature_columns, sensitive_column)
    finished_partitions = m.partition(k=2)
    print(finished_partitions)

    rows = anonypy.build_anonymized_dataset(
        df, finished_partitions, feature_columns, sensitive_column
    )
    dfn = pd.DataFrame(rows)
    print(dfn)


def test_l_diversity():
    path = "data/adult.test.txt"
    df = pd.read_csv(path, sep=", ", names=names, engine="python")

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["age", "education"]
    sensitive_column = "income"

    m = anonypy.Mondrian(df, feature_columns, sensitive_column)
    finished_partitions = m.partition(k=3, l=2)

    print(len(finished_partitions))
    print(finished_partitions[0])

    indexes = util.build_indexes(df)
    column_x, column_y = feature_columns[:2]
    rects = util.get_partition_rects(
        df, finished_partitions, column_x, column_y, indexes, offsets=[0.1, 0.1]
    )

    print(rects[:10])

    rows = anonypy.build_anonymized_dataset(
        df, finished_partitions, feature_columns, sensitive_column
    )
    dfn = pd.DataFrame(rows)
    print(dfn.sort_values(feature_columns + [sensitive_column]))


def test_t_closeness():
    path = "data/adult.test.txt"
    df = pd.read_csv(path, sep=", ", names=names, engine="python")

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["age", "education-num"]
    sensitive_column = "income"

    global_freqs = {}
    total_count = float(len(df))
    group_counts = df.groupby(sensitive_column)[sensitive_column].agg("count")
    for value, count in group_counts.to_dict().items():
        p = count / total_count
        global_freqs[value] = p

    m = anonypy.Mondrian(df, feature_columns, sensitive_column)
    finished_partitions = m.partition(k=3, global_freqs=global_freqs)

    rows = anonypy.build_anonymized_dataset(
        df, finished_partitions, feature_columns, sensitive_column
    )
    dfn = pd.DataFrame(rows)
    print(dfn.sort_values(feature_columns + [sensitive_column]))


def test_get_spans():
    path = "data/adult.test.txt"
    df = pd.read_csv(path, sep=", ", names=names, engine="python")

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["age", "education-num"]
    m = anonypy.Mondrian(df, feature_columns)
    spans = m.get_spans(df.index)

    assert {"age": 73, "education-num": 15} == spans

    feature_columns = ["sex", "income", "native-country", "race"]
    m = anonypy.Mondrian(df, feature_columns)
    spans = m.get_spans(df.index)

    assert {"income": 2, "sex": 2, "native-country": 41, "race": 5} == spans
