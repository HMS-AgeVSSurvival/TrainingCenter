from setuptools import setup

setup(
    name="training_center",
    version="0.1",
    description="Trains algorithms from NHANES dataset.",
    packages=["fold_maker"],
    requires=["setuptools", "wheel"],
    install_requires=["numpy", "pandas", "pyarrow"],
    extras_require={"dev": ["tqdm", "jupyter", "ipympl", "black", "matplotlib", "openpyxl"]},
    entry_points={
        "console_scripts": [
            "make_folds=fold_maker.fold_maker:fold_maker_cli",
        ]
    },
)
