import pandas as pd

from sklearn.linear_model import ElasticNet
from lightgbm import LGBMRegressor

from prediction import AGE_COLUMN


class Model:
    def __init__(self, algorithm, random_state):
        self.algorithm = algorithm
        self.random_state = random_state

        if self.algorithm == "elastic_net":  # Randomness comes from feature selection
            self.net = ElasticNet(selection="random", random_state=self.random_state)
        elif self.algorithm == "light_gbm":
            self.net = LGBMRegressor(importance_type="gain", random_state=self.random_state)

    def set(self, **hyperparameters):
        self.net.set_params(**hyperparameters)

    def fit(self, samples):
        self.net.fit(samples[samples.columns[samples.columns != AGE_COLUMN]].values, samples[AGE_COLUMN].values)

    def predict(self, samples):
        return pd.Series(self.net.predict(samples[samples.columns[samples.columns != AGE_COLUMN]]), index=samples.index, name="prediction")