from anonypy import mondrian


class Preserver:
    def __init__(self, df, feature_columns, sensitive_column):
        self.modrian = mondrian.Mondrian(df, feature_columns, sensitive_column)

    def __anonymize(self, k, l=0, p=0.0):
        partitions = self.modrian.partition(k, l, p)
        return anonymize(
            self.modrian.df,
            partitions,
            self.modrian.feature_columns,
            self.modrian.sensitive_column,
        )

    def anonymize_k_anonymity(self, k):
        return self.__anonymize(k)

    def anonymize_l_diversity(self, k, l):
        return self.__anonymize(k, l=l)

    def anonymize_t_closeness(self, k, p):
        return self.__anonymize(k, p=p)

    def __count_anonymity(self, k, l=0, p=0.0):
        partitions = self.modrian.partition(k, l, p)
        return count_anonymity(
            self.modrian.df,
            partitions,
            self.modrian.feature_columns,
            self.modrian.sensitive_column,
        )

    def count_k_anonymity(self, k):
        return self.__count_anonymity(k)

    def count_l_diversity(self, k, l):
        return self.__count_anonymity(k, l=l)

    def count_t_closeness(self, k, p):
        return self.__count_anonymity(k, p=p)


def agg_categorical_column(series):
    # this is workaround for dtype bug of series
    series.astype("category")
    return [",".join(set(series))]


def agg_numerical_column(series):
    # return [series.mean()]
    minimum = series.min()
    maximum = series.max()
    if maximum == minimum:
        string = str(maximum)
    else:
        string = f"{minimum}-{maximum}"
    return [string]


def anonymize(df, partitions, feature_columns, sensitive_column, max_partitions=None):
    aggregations = {}
    for column in feature_columns:
        if df[column].dtype.name == "category":
            aggregations[column] = agg_categorical_column
        else:
            aggregations[column] = agg_numerical_column
    rows = []
    for i, partition in enumerate(partitions):
        if max_partitions is not None and i > max_partitions:
            break
        grouped_columns = df.loc[partition].agg(aggregations, squeeze=False)
        sensitive_counts = (
            df.loc[partition].groupby(sensitive_column).agg({sensitive_column: "count"})
        )
        values = grouped_columns.iloc[0].to_dict()
        for sensitive_value, count in sensitive_counts[sensitive_column].items():
            if count == 0:
                continue
            values.update(
                {
                    sensitive_column: sensitive_value,
                    "count": count,
                }
            )
            rows.append(values.copy())
    return rows


def count_anonymity(
    df, partitions, feature_columns, sensitive_column, max_partitions=None
):
    aggregations = {}
    for column in feature_columns:
        if df[column].dtype.name == "category":
            aggregations[column] = agg_categorical_column
        else:
            aggregations[column] = agg_numerical_column
    aggregations[sensitive_column] = "count"
    rows = []
    for i, partition in enumerate(partitions):
        if max_partitions is not None and i > max_partitions:
            break
        grouped_columns = df.loc[partition].agg(aggregations, squeeze=False)
        values = grouped_columns.iloc[0].to_dict()
        rows.append(values.copy())
    return rows
