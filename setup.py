from setuptools import setup

setup(
    name="training_center",
    version="0.1",
    description="Trains algorithms from NHANES dataset.",
    packages=["fold_maker", "prediction", "feature_importances", "utils", "test"],
    requires=["setuptools", "wheel"],
    install_requires=[
        "numpy",
        "pandas",
        "pyarrow",
        "hyperopt",
        "scikit-learn==0.23.2",
        "scikit-survival",
        "lightgbm",
        "hyperopt",
        "gspread",
        "matplotlib", 
        "openpyxl"
    ],
    extras_require={
        "dev": ["tqdm", "jupyter", "ipympl", "black"]
    },
    entry_points={
        "console_scripts": [
            "make_folds=fold_maker.fold_maker:fold_maker_cli",
            "prediction=prediction.compute_prediction:prediction_cli",
            "feature_importances=feature_importances.compute_feature_importances:feature_importances_cli",
        ]
    },
)
