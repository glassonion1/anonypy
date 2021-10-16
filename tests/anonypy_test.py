import anonypy
from anonypy import util
from anonypy import mondrian
import pandas as pd

names = (
    'age',
    'workclass', #Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
    'fnlwgt', # "weight" of that person in the dataset (i.e. how many people does that person represent) -> https://www.kansascityfed.org/research/datamuseum/cps/coreinfo/keyconcepts/weights
    'education',
    'education-num',
    'marital-status',
    'occupation',
    'relationship',
    'race',
    'sex',
    'capital-gain',
    'capital-loss',
    'hours-per-week',
    'native-country',
    'income',
)

categorical = set((
    'workclass',
    'education',
    'marital-status',
    'occupation',
    'relationship',
    'sex',
    'native-country',
    'race',
    'income',
))

def test_build_anonymized_dataset():
    path = 'data/adult.test.txt'
    df = pd.read_csv(path, sep=', ', names=names, engine='python')

    for name in categorical:
        df[name] = df[name].astype('category')

    feature_columns = ['age', 'education-num']
    m = mondrian.Mondrian(df, feature_columns)
    finished_partitions = m.partition(anonypy.is_k_anonymous)

    print(len(finished_partitions))
    print(finished_partitions[0])

    indexes = util.build_indexes(df)    
    column_x, column_y = feature_columns[:2]
    rects = util.get_partition_rects(df, finished_partitions, column_x, column_y, indexes, offsets=[0.1, 0.1])

    print(rects[:10])

    sensitive_column = 'income'
    rows = anonypy.build_anonymized_dataset(df, finished_partitions, feature_columns, sensitive_column)
    dfn = pd.DataFrame(rows)
    print(dfn.sort_values(feature_columns+[sensitive_column]))

def test_get_spans():
    path = 'data/adult.test.txt'
    df = pd.read_csv(path, sep=', ', names=names, engine='python')

    for name in categorical:
        df[name] = df[name].astype('category')

    feature_columns = ['age', 'education-num']
    m = mondrian.Mondrian(df, feature_columns)
    spans = m._get_spans(df.index)

    assert {'age': 73, 'education-num': 15} == spans

    feature_columns = ['sex', 'income', 'native-country', 'race']
    m = mondrian.Mondrian(df, feature_columns)
    spans = m._get_spans(df.index)

    assert {'income': 2, 'sex': 2, 'native-country': 41, 'race': 5} == spans
    
