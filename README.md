# AnonyPy
Anonymization library for python.
AnonyPy provides following privacy preserving techniques for the anonymization.
- K Anonymity
- L Diversity
- T Closeness

## The Anonymization method
- Anonymization method aims at making the individual record be indistinguishable among a group record by using techniques of generalization and suppression.
- Turning a dataset into a k-anonymous (and possibly l-diverse or t-close) dataset is a complex problem, and finding the optimal partition into k-anonymous groups is an NP-hard problem.
- AnonyPy uses "Mondrian" algorithm to partition the original data into smaller and smaller groups
- The algorithm assumes that we have converted all attributes into numerical or categorical values and that we are able to measure the “span” of a given attribute Xi.

## Install
```
$ pip install anonypy
```

## Usage
```python
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

def main():
    df = pd.DataFrame(data=data, columns=columns)

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"

    p = anonypy.Preserver(df, feature_columns, sensitive_column)
    rows = p.anonymize_k_anonymity(k=2)

    dfn = pd.DataFrame(rows)
    print(dfn)
```

Original data
```bash
   col1 col2   col3 col4  col5
0     6    1  test1    x    20
1     6    1  test1    x    30
2     8    2  test2    x    50
3     8    2  test3    w    45
4     8    1  test2    y    35
5     4    2  test3    y    20
6     4    1  test3    y    20
7     2    1  test3    z    22
8     2    2  test3    y    32
```

The created anonymized data is below(Guarantee 2-anonymity).
```bash
  col1 col2         col3 col4  count
0  2-4    2        test3    y      2
1  2-4    1        test3    y      1
2  2-4    1        test3    z      1
3  6-8    1  test1,test2    x      2
4  6-8    1  test1,test2    y      1
5    8    2  test3,test2    w      1
6    8    2  test3,test2    x      1
```
