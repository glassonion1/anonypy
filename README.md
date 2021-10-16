# AnonyPy
Anonymization library for python

## Install
```
$ pip install anonypy
```

## Usage
```python
import anonypy
import pandas as pd

def main():
    path = 'data/adult.test.txt'
    df = pd.read_csv(path, sep=', ', names=names, engine='python')

    for name in categorical:
        df[name] = df[name].astype('category')

    feature_columns = ['age', 'education-num']
    m = anonypy.Mondrian(df, feature_columns)
    partitions = m.partition(anonypy.is_k_anonymous)
    print(partitions)
```
