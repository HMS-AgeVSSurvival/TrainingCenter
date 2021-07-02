import unittest
import os
import pandas as pd
import numpy as np

from fold_maker.fold_maker import get_folds


class TestFolds(unittest.TestCase):
    def test_get_folds(self):
        # Test if it woks with empty indexes
        self.assertTrue(len(get_folds(range(0), 10)) == 0)

        indexes = pd.Index(np.random.randint(0, 10000, size=1000)).drop_duplicates()

        # Test if returned indexes are the same
        returned_indexes = get_folds(indexes, 10).index
        self.assertTrue(all(returned_indexes.isin(indexes)))
        self.assertTrue(all(indexes.isin(returned_indexes)))

        # Test if returned folds are all present 
        n_folds = np.random.randint(1, 100)
        returned_folds = get_folds(indexes, n_folds).drop_duplicates()
        self.assertTrue(all(returned_folds.isin(range(n_folds))))
        self.assertTrue(all(pd.Index(range(n_folds)).isin(returned_folds)))

        # Test if returned folds are equally spread
        n_folds = np.random.randint(1, 100)
        number_per_fold = list(map(lambda group: group[1].shape[0], get_folds(indexes, n_folds).to_frame().groupby(by=["fold"])))

        self.assertTrue(max(number_per_fold) - min(number_per_fold) <= 1)
