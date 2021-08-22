# TrainingCenter

[![Super linter](https://github.com/HMS-Internship/TrainingCenter/actions/workflows/linter.yml/badge.svg)](https://github.com/TrainingCenter/Website/actions/workflows/linter.yml)

Trains machine learning algorithms to predict the age and the risk of dying for participants of NHANES dataset

Feel free to start a discussion to ask anything [here](https://github.com/HMS-Internship/TrainingCenter/discussions).


To setup the virtual environment:
```Bash
pip install pip==20.0.2
pip install -e .
```

## Pipelines
There are three pipelines available. Before launching them, you need to set the folds properly by executing the following:
```Bash
make_folds --main_category MAIN_CATEGORY --category CATEGORY --number_folds NUMBER_FOLDS
```

#### Predictions
To predict the biological age or the risk of dying, you can use the command line made for that purpose:
```Bash
prediction --main_category MAIN_CATEGORY --category CATEGORY --target TARGET --algorithm ALGORITHM --random_state RANDOM_STATE --n_inner_search N_INNER_SEARCH
```

#### Basic predictions
To have the control on the survival predictions, you can train the models with only age, sex and ethnicities by using this command line:
```Bash
basic_prediction --main_category MAIN_CATEGORY --category CATEGORY --target TARGET --algorithm ALGORITHM --random_state RANDOM_STATE --n_inner_search N_INNER_SEARCH
```

#### Feature importances
To get the feature importances of the models, you can use:
```Bash
feature_importances --main_category MAIN_CATEGORY --category CATEGORY --target TARGET --algorithm ALGORITHM --random_state RANDOM_STATE --n_inner_search N_INNER_SEARCH
```

## Results
All the results are available in this [spread sheet](https://docs.google.com/spreadsheets/d/1IZDQmitlE5fU_5wbu2T8jF2_4i7I7Q_VTTjv6buVFwc/edit#gid=750005196). The results are automatically updated to the spread sheet when the computations are done.

Executing the file _./shape_age_range/export_information.py_ will add the shapes and the age ranges to the [spread sheet](https://docs.google.com/spreadsheets/d/1IZDQmitlE5fU_5wbu2T8jF2_4i7I7Q_VTTjv6buVFwc/edit#gid=750005196) for each category and each target.

## Launching jobs
The folder [__fit_running__](./fit_running/) gathers all the scripts for you to launch jobs on a cluster of computers using Slurm without you having to tell how much memory or time limit you need.

## To run the tests
```{bash}
python -m unittest
```