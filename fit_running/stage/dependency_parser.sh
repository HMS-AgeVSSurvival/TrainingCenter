#!/bin/bash

function clear_dependency_arguments() {
    unset RANDOM_STATE
    unset STATE
    unset TIME_LIMIT
    unset MEMORY_LIMIT
    unset PARTITION
    unset N_INNER_SEARCH
}


function usage_dependency_parser() {
    cat << HEREDOC

    Usage: $understand_state [-rs RANDOM_STATE] [-s STATE] [-t TIME_LIMIT] [-m MEMORY_LIMIT] [-p PARTITION] [-nis N_INNER_SEARCH]

    optional arguments:
        -h, --help                              show this help message and exit
        -rs, --random_state RANDOM_STATE        the random state
        -s, --state STATE                       the output state
        -t, --time_limit TIME_LIMIT             the time limit
        -m, --memory_limit MEMORY_LIMIT         the memory limit
        -p, --partition PARTITION               the partition
        -nis, --n_inner_search N_INNER_SEARCH   int, number of hyperparameter search

HEREDOC
}


function parse_dependency_info() {
    local HELP_CALLED=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -h | --help ) 
                usage_dependency_parser >&2
                local HELP_CALLED=true
                shift
                ;;
            -rs | --random_state)
                RANDOM_STATE=$2
                shift
                shift
                ;;
            -s | --state)
                STATE=$2
                shift
                shift
                ;;
            -t | --time_limit)
                TIME_LIMIT=$2
                shift
                shift
                ;;
            -m | --memory_limit)
                MEMORY_LIMIT=$2
                shift
                shift
                ;;
            -p | --partition)
                PARTITION=$2
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
}