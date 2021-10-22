from anonypy import anonymity


class Mondrian:
    def __init__(self, df, feature_columns, sensitive_column=None):
        self.df = df
        self.feature_columns = feature_columns
        self.sensitive_column = sensitive_column

    def is_valid(self, partition, k=2, l=0, p=0.0):
        # k-anonymous
        if not anonymity.is_k_anonymous(partition, k):
            return False
        # l-diverse
        if l > 0 and self.sensitive_column is not None:
            diverse = anonymity.is_l_diverse(
                self.df, partition, self.sensitive_column, l
            )
            if not diverse:
                return False
        # t-close
        if p > 0.0 and self.sensitive_column is not None:
            global_freqs = anonymity.get_global_freq(self.df, self.sensitive_column)
            close = anonymity.is_t_close(
                self.df, partition, self.sensitive_column, global_freqs, p
            )
            if not close:
                return False

        return True

    def get_spans(self, partition, scale=None):
        spans = {}
        for column in self.feature_columns:
            if self.df[column].dtype.name == "category":
                span = len(self.df[column][partition].unique())
            else:
                span = (
                    self.df[column][partition].max() - self.df[column][partition].min()
                )
            if scale is not None:
                span = span / scale[column]
            spans[column] = span
        return spans

    def split(self, column, partition):
        dfp = self.df[column][partition]
        if dfp.dtype.name == "category":
            values = dfp.unique()
            lv = set(values[: len(values) // 2])
            rv = set(values[len(values) // 2 :])
            return dfp.index[dfp.isin(lv)], dfp.index[dfp.isin(rv)]
        else:
            median = dfp.median()
            dfl = dfp.index[dfp < median]
            dfr = dfp.index[dfp >= median]
            return (dfl, dfr)

    def partition(self, k=3, l=0, p=0.0):
        scale = self.get_spans(self.df.index)

        finished_partitions = []
        partitions = [self.df.index]
        while partitions:
            partition = partitions.pop(0)
            spans = self.get_spans(partition, scale)
            for column, span in sorted(spans.items(), key=lambda x: -x[1]):
                lp, rp = self.split(column, partition)
                if not self.is_valid(lp, k, l, p) or not self.is_valid(rp, k, l, p):
                    continue
                partitions.extend((lp, rp))
                break
            else:
                finished_partitions.append(partition)
        return finished_partitions
