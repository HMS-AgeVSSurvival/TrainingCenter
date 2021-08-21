#!/bin/bash

function clear_training_arguments() {
    unset JOB_ID_RUN
    unset TRAINING_TYPE
    unset MAIN_CATEGORY
    unset CATEGORY
    unset TARGET
    unset ALGORITHM
    unset N_INNER_SEARCH
}


function usage_training_parser() {
    cat << HEREDOC

    Usage: $parse_training_arguments [-jir JOB_ID_RUN] [-tt TRAINING_TYPE] [-t TARGET] [-mc MAIN_CATEGORY] [-c CATEGORY] [-a ALGORITHM] [-nis N_INNER_SEARCH]

    optional arguments:
        -h, --help                              show this help message and exit
        -jir, --job_id_run JOB_ID_RUN           the dependent job id
        -tt, --training_type TRAINING_TYPE      "basic_prediction", "prediction" or "feature_importances"
        -mc, --main_category MAIN_CATEGORY      "examination", "laboratory" or "questionnaire"
        -c, --category CATEGORY                 the category
        -t, --target TARGET                     "age", "all", "cvd" or "cancer"
        -a, --algorithm ALGORITHM               "elastic_net" or "light_gbm"
        -nis, --n_inner_search N_INNER_SEARCH   int, number of hyperparameter search

HEREDOC
}


function parse_training_arguments() {
    local HELP_CALLED=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -h | --help ) 
                usage_training_parser >&2
                local HELP_CALLED=true
                shift
                ;;
            -jir | --job_id_run)
                JOB_ID_RUN=$2
                shift
                shift
                ;;
            -tt | --training_type)
                case $2 in
                    basic_prediction | prediction | feature_importances) 
                        TRAINING_TYPE=$2;;
                    *)
                        echo "training_type: $2 not in basic_prediction, prediction or feature_importances" >&2
                        usage_training_parser
                        exit;;
                esac
                shift
                shift
                ;;
            -mc | --main_category)
                case $2 in
                    examination | laboratory | questionnaire) 
                        MAIN_CATEGORY=$2;;
                    *)
                        echo "main_category: $2 not in examination, laboratory or questionnaire" >&2
                        usage_training_parser
                        exit;;
                esac
                shift
                shift
                ;;
            -c | --category)
                CATEGORY=$2
                shift
                shift
                ;;
            -t | --target)
                case $2 in
                    age | all | cvd | cancer) 
                        TARGET=$2;;
                    *)
                        echo "target: $2 not in age, all, cvd or cancer" >&2
                        usage_training_parser
                        exit;;
                esac
                shift
                shift
                ;;
            -a | --algorithm)
                case $2 in
                    elastic_net | light_gbm) 
                        ALGORITHM=$2;;
                    *)
                        echo "algorithm: $2 not in elastic_net or light_gbm" >&2
                        usage_training_parser
                        exit;;
                esac
                shift
                shift
                ;;
            -nis | --n_inner_search)
                N_INNER_SEARCH=$2
                shift
                shift
                ;;
            -?*)
                printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
                exit
                ;;
        esac
    done


    if [ !$HELP_CALLED ];
    then
        if [[ $TRAINING_TYPE == "" ]]
        then
            echo "TRAINING_TYPE is missing" >&2
            usage_training_parser
            exit
        elif [[ $MAIN_CATEGORY == "" ]]
        then
            echo "MAIN_CATEGORY is missing" >&2
            usage_training_parser
            exit
        elif [[ $CATEGORY == "" ]]
        then
            echo "CATEGORY is missing" >&2
            usage_training_parser
            exit
        elif [[ $TARGET == "" ]]
        then
            echo "TARGET is missing" >&2
            usage_training_parser
            exit
        elif [[ $ALGORITHM == "" ]]
        then
            echo "ALGORITHM is missing" >&2
            usage_training_parser
            exit
        elif [[ $N_INNER_SEARCH == "" ]]
        then
            echo "N_INNER_SEARCH is missing" >&2
            usage_training_parser
            exit
        fi
    fi
}