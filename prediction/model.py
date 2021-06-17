import pandas as pd

from sklearn.linear_model import ElasticNet
from lightgbm import LGBMRegressor
from sklearn.metrics import r2_score

from prediction import COLUMNS_TO_DROP


# from sksurv.linear_model import CoxnetSurvivalAnalysis
# from sksurv.ensemble import GradientBoostingSurvivalAnalysis
# from sksurv.util import Surv

# from sksurv.metrics import concordance_index_censored


class Model:
    def __init__(self, algorithm, random_state):
        self.algorithm = algorithm
        self.random_state = random_state
        self.predictors = None

        if self.algorithm == "elastic_net":
            self.net = ElasticNet(selection="random", random_state=self.random_state)
        elif self.algorithm == "light_gbm":
            self.net = LGBMRegressor(importance_type="gain", random_state=self.random_state)

        self.score = r2_score

    def set(self, **hyperparameters):
        self.net.set_params(**hyperparameters)

    def fit(self, samples):
        self.predictors = samples.columns.drop(COLUMNS_TO_DROP)
        # SCALE
        self.net.fit(samples[self.predictors].values, samples[self.target].values)

    def predict(self, samples):
        return pd.Series(self.net.predict(samples[self.predictors]), index=samples.index)

    def get_score(self, samples):
        if self.prediction:
            return self.score(samples[self.target], self.predict(samples))
        else:  # Survival
            return self.score(samples[self.target["event"]], samples[self.target["duration"]], self.predict(samples))[0]