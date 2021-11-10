import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree
import category_encoders as ce


class RecordLinkage:
    def __init__(self, df, knowledge):
        self.df = df
        self.knowledge = knowledge

        categories = (df.dtypes == "object").keys().to_list()
        self.enc = ce.OneHotEncoder(cols=categories, drop_invariant=False)
        df_concat = pd.concat([self.df, self.knowledge], ignore_index=True)
        self.enc.fit(df_concat)

    def execute(self, k=3):
        enc_df = self.enc.transform(self.df).astype("float64").values
        enc_knowledge = self.enc.transform(self.knowledge).astype("float64").values

        tree = KDTree(enc_df)
        dist, index = tree.query(enc_knowledge, k=k)
        return dist, index


def attack(df, knowledge):
    k = 3
    a = RecordLinkage(df, knowledge)
    dist, index = a.execute(k)

    di = pd.DataFrame(np.hstack((index, dist)))

    di.loc[di[3] > di[3].median(), :] = -1
    # Display the top three
    return di.iloc[:, 0:k].astype(int)
