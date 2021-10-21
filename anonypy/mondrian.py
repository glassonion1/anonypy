import types

def is_k_anonymous(partition, k):
    if len(partition) < k:
        return False
    return True

def is_l_diverse(sensitive_series, partition, l):
    diversity = len(sensitive_series[partition].unique())
    return diversity >= l

def t_closeness(df, partition, column, global_freqs):
    total_count = float(len(partition))
    d_max = None
    group_counts = df.loc[partition].groupby(column)[column].agg('count')
    for value, count in group_counts.to_dict().items():
        p = count/total_count
        d = abs(p-global_freqs[value])
        if d_max is None or d > d_max:
            d_max = d
    return d_max

def is_t_close(df, partition, sensitive_column, global_freqs, p):
    return t_closeness(df, partition, sensitive_column, global_freqs) <= p

class Mondrian:
    def __init__(self, df, feature_columns, sensitive_column=None):
        self.df = df
        self.feature_columns = feature_columns
        self.sensitive_column = sensitive_column
    
    def is_valid(self, partition, k=2, l=0, global_freqs=None, p=0.2):
        # k-anonymous
        if not is_k_anonymous(partition, k):
            return False
        # l-diverse
        if l > 0 and self.sensitive_column is not None:
            diverse = is_l_diverse(self.df[self.sensitive_column], partition, l)
            if not diverse:
                return False
        # t-close
        if global_freqs is not None and self.sensitive_column is not None:
            close = is_t_close(self.df, partition, self.sensitive_column, global_freqs, p)
            if not close:
                return False
            
        return True
        
    def get_spans(self, partition, scale=None):
        spans = {}
        for column in self.feature_columns:
            if self.df[column].dtype.name == 'category':
                span = len(self.df[column][partition].unique())
            else:
                span = self.df[column][partition].max()-self.df[column][partition].min()
            if scale is not None:
                span = span/scale[column]
            spans[column] = span
        return spans

    def split(self, column, partition):
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

    def partition(self, k=3, l=0, global_freqs=None, p=0.2):
        scale = self.get_spans(self.df.index)

        finished_partitions = []
        partitions = [self.df.index]
        while partitions:
            partition = partitions.pop(0)
            spans = self.get_spans(partition, scale)
            for column, span in sorted(spans.items(), key=lambda x:-x[1]):
                lp, rp = self.split(column, partition)
                if not self.is_valid(lp, k, l, global_freqs, p) \
                   or not self.is_valid(rp, k, l, global_freqs, p):
                    continue
                partitions.extend((lp, rp))
                break
            else:
                finished_partitions.append(partition)
        return finished_partitions
        
