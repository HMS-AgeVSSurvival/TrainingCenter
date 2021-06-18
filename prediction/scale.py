from prediction import AGE_COLUMN, COLUMNS_TO_DROP_FOR_SCALE


def scale(data):
    columns_to_scale = data.columns.drop(COLUMNS_TO_DROP_FOR_SCALE)

    return (data[columns_to_scale] - data[columns_to_scale].mean()) / (data[columns_to_scale].std() + 1e-16), data[AGE_COLUMN].mean(), data[AGE_COLUMN].std()