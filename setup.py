from setuptools import setup

setup(
    name="training_center",
    version="0.1",
    description="Trains algorithms from NHANES dataset.",
    packages=[
        "fold_maker",
        "shape_age_range",
        "fit_running",
        "prediction",
        "feature_importances",
        "utils",
        "test",
    ],
    requires=["setuptools", "wheel"],
    install_requires=[
        "numpy==1.16.6",
        "pandas==1.2.4",
        "pyarrow==4.0.1",
        "hyperopt==0.2.5",
        "scikit-learn==0.23.2",
        "scikit-survival==0.14.0",
        "lightgbm==3.2.1",
        "gspread==3.7.0",
        "matplotlib==3.4.2",
        "openpyxl==3.0.7",
    ],
    extras_require={"dev": ["tqdm==4.61.1", "jupyter==1.0.0", "ipympl==0.7.0", "black==21.6b0"]},
    entry_points={
        "console_scripts": [
            "make_folds=fold_maker.fold_maker:fold_maker_cli",
            "prediction=prediction.compute_prediction:prediction_cli",
            "basic_prediction=prediction.compute_prediction:basic_prediction_cli",
            "feature_importances=feature_importances.compute_feature_importances:feature_importances_cli",
        ]
    },
)
