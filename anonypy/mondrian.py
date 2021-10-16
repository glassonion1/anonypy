class Mondrian:
    df = []
    def __init__(self, df, feature_columns):
        self.df = df[feature_columns]

    def _get_spans(self, partition, scale=None):
        spans = {}
        for column in self.df.columns:
            if self.df[column].dtype.name == 'category':
                span = len(self.df[column][partition].unique())
            else:
                span = self.df[column][partition].max()-self.df[column][partition].min()
            if scale is not None:
                span = span/scale[column]
            spans[column] = span
        return spans

    def _split(self, column, partition):
        dfp = self.df[column][partition]
        if dfp.dtype.name == 'category':
            values = dfp.unique()
            lv = set(values[:len(values)//2])
            rv = set(values[len(values)//2:])
            return dfp.index[dfp.isin(lv)], dfp.index[dfp.isin(rv)]
        else:        
            median = dfp.median()
            dfl = dfp.index[dfp < median]
            dfr = dfp.index[dfp >= median]
            return (dfl, dfr)

    def partition(self, is_valid):
        scale = self._get_spans(self.df.index)

        finished_partitions = []
        partitions = [self.df.index]
        while partitions:
            partition = partitions.pop(0)
            spans = self._get_spans(partition, scale)
            for column, span in sorted(spans.items(), key=lambda x:-x[1]):
                lp, rp = self._split(column, partition)
                if not is_valid(self.df, lp) or not is_valid(self.df, rp):
                    continue
                partitions.extend((lp, rp))
                break
            else:
                finished_partitions.append(partition)
        return finished_partitions
        
