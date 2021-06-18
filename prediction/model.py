import pandas as pd

from prediction import AGE_COLUMN, DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN


class ModelAge:
    def __init__(self, algorithm, random_state):
        from sklearn.linear_model import ElasticNet
        from lightgbm import LGBMRegressor

        self.algorithm = algorithm
        self.random_state = random_state

        if self.algorithm == "elastic_net":  # Randomness comes from feature selection
            self.net = ElasticNet(selection="random", random_state=self.random_state, max_iter=2000)
        elif self.algorithm == "light_gbm":
            self.net = LGBMRegressor(importance_type="gain", random_state=self.random_state)

    def set(self, **hyperparameters):
        self.net.set_params(**hyperparameters)

    def fit(self, samples):
        self.net.fit(samples[samples.columns[samples.columns != AGE_COLUMN]].values, samples[AGE_COLUMN].values)

    def predict(self, samples):
        return pd.Series(self.net.predict(samples[samples.columns[samples.columns != AGE_COLUMN]]), index=samples.index, name="prediction")


class ModelSurvival:
    def __init__(self, algorithm, random_state):
        from sksurv.linear_model import CoxnetSurvivalAnalysis
        from sksurv.ensemble import GradientBoostingSurvivalAnalysis

        self.algorithm = algorithm
        self.random_state = random_state

        if self.algorithm == "elastic_net":
            self.net = CoxnetSurvivalAnalysis(n_alphas=1, max_iter=1000)
        elif self.algorithm == "light_gbm":
            self.net = GradientBoostingSurvivalAnalysis(random_state=self.random_state)
        
    def set(self, **hyperparameters):
        if self.algorithm == "elastic_net":
            self.net.alphas = [hyperparameters["alpha"]]
            self.net.l1_ratio = hyperparameters["l1_ratio"]
        elif self.algorithm == "light_gbm":
            self.net.max_leaf_nodes = hyperparameters["max_leaf_nodes"]
            self.net.learning_rate = hyperparameters["learning_rate"]
            self.net.n_estimators = hyperparameters["n_estimators"]
            self.net.min_samples_leaf = hyperparameters["min_samples_leaf"]
            self.net.subsample = hyperparameters["subsample"]
            
    def fit(self, samples):   
        from sksurv.util import Surv

        labels = Surv.from_arrays(samples[DEATH_COLUMN], samples[FOLLOW_UP_TIME_COLUMN])
        self.net.fit(samples[samples.columns[~samples.columns.isin([DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN])]], labels)

    def predict(self, samples):
        return pd.Series(self.net.predict(samples[samples.columns[~samples.columns.isin([DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN])]]), index=samples.index, name="prediction")