from prediction import AGE_COLUMN, COLUMNS_TO_DROP_FOR_SCALE, COLUMNS_TO_ADD_AFTER_SCALE


def scale_age(data):
    columns_to_scale = data.columns.drop(COLUMNS_TO_DROP_FOR_SCALE)

    return (data[columns_to_scale] - data[columns_to_scale].mean()) / (data[columns_to_scale].std() + 1e-16), data[AGE_COLUMN].mean(), data[AGE_COLUMN].std()


def scale_survival(data):
    columns_to_scale = data.columns.drop(COLUMNS_TO_DROP_FOR_SCALE)

    scaled_data = (data[columns_to_scale] - data[columns_to_scale].mean()) / (data[columns_to_scale].std() + 1e-16)

    scaled_data[COLUMNS_TO_ADD_AFTER_SCALE] = data[COLUMNS_TO_ADD_AFTER_SCALE]

    return scaled_data