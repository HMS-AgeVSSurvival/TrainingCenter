#!/bin/bash

function check_if_relaunch() {
    local RANDOM_STATE=$1
    if [[ $RANDOM_STATE == "1" ]]
    then 
        local STATE=$STATE_1
    else
        local STATE=$STATE_2
    fi

    if [[ $STATE == "COMPLETED" ]] || [[ $STATE == "" ]]
    then
        echo "The dependency with random state $RANDOM_STATE has been run successfully"
        cat out/$PATH_OUTPUTS/$ALGORITHM\_$RANDOM_STATE.out >> out/$PATH_OUTPUTS/memory_$ALGORITHM\_$RANDOM_STATE.out
        rm out/$PATH_OUTPUTS/$ALGORITHM\_$RANDOM_STATE.out
        RELAUNCH=false
    elif [[ $STATE == "FAILED" ]]
    then
        echo "The dependency with random state $RANDOM_STATE has failed" >&2
        cat out/$PATH_OUTPUTS/$ALGORITHM\_$RANDOM_STATE.out >> out/$PATH_OUTPUTS/memory_$ALGORITHM\_$RANDOM_STATE.out
        rm out/$PATH_OUTPUTS/$ALGORITHM\_$RANDOM_STATE.out
        mv out/$PATH_OUTPUTS/memory_$ALGORITHM\_$RANDOM_STATE.out error/$PATH_OUTPUTS/
        RELAUNCH=false
    elif [[ $STATE == "OUT_OF_MEMORY" ]]
    then
        echo "The dependency with random state $RANDOM_STATE has been running out of memory: $MEMORY_LIMIT"
        RELAUNCH=true
    elif [[ $STATE == "TIMEOUT" ]]
    then
        echo "The dependency with random state $RANDOM_STATE has been running out of time: $TIME_LIMIT"
        RELAUNCH=true
    else
        echo "The dependency with random state $RANDOM_STATE has been ending with an unknown state : $STATE" >&2
        cat out/$PATH_OUTPUTS/$ALGORITHM\_$RANDOM_STATE.out >> out/$PATH_OUTPUTS/memory_$ALGORITHM\_$RANDOM_STATE.out
        rm out/$PATH_OUTPUTS/$ALGORITHM\_$RANDOM_STATE.out
        mv out/$PATH_OUTPUTS/memory_$ALGORITHM\_$RANDOM_STATE.out error/$PATH_OUTPUTS/
        RELAUNCH=false
    fi
}

function add_memory() {
    echo "Add memory"

    if [[ $new_memory_limit =~ "M" ]];  # Double the memory limit
    then
        local memory_digits=${new_memory_limit%M*}
        if (( 2 * $memory_digits < 1000 ));
        then 
            new_memory_limit=$(( 2 * $memory_digits ))Mc
        else
            local new_memory_digits=$(( 2 * $memory_digits / 1000 ))
            if ((  2 * $memory_digits % 1000 > 500 ));
            then
                local new_memory_digits=$(( $new_memory_digits + 1 ))
            fi
            new_memory_limit=$new_memory_digits\Gc
        fi
    elif [[ $new_memory_limit =~ "G" ]]  # Add 1 gigabyte
    then
        new_memory_limit=$(( ${new_memory_limit%G*} + 1 ))Gc
    else
        echo "Weird format memory limit: $new_memory_limit"
        exit
    fi
}


function add_time() {
    echo "Add time"

    if [[ $new_time_limit =~ "-" ]]; 
    then
        IFS="-" read -ra SPLIT_TIME_LIMIT <<< $new_time_limit
        local NEW_DAYS=$(( 10#${SPLIT_TIME_LIMIT[0]} ))
        local HOURS_MINUTES_SECONDS=${SPLIT_TIME_LIMIT[1]}
    else
        local NEW_DAYS=$(( 10#0 ))
        local HOURS_MINUTES_SECONDS=$new_time_limit
    fi

    IFS=":" read -ra SPLIT_HOURS_MINUTES_SECONDS_LIMIT <<< $HOURS_MINUTES_SECONDS
    local NEW_HOURS=$(( 10#${SPLIT_HOURS_MINUTES_SECONDS_LIMIT[0]} ))
    local NEW_MINUTES=$(( 10#${SPLIT_HOURS_MINUTES_SECONDS_LIMIT[1]} ))
    local NEW_SECONDS=$(( 10#${SPLIT_HOURS_MINUTES_SECONDS_LIMIT[2]} ))

    if (( $NEW_HOURS < 3 )) && (( $NEW_DAYS == 0 ));  # Add 30 minutes
    then
        if (( $NEW_MINUTES + 30 < 60 ));
        then
            NEW_MINUTES=$(( $NEW_MINUTES + 30 ))
        else
            NEW_HOURS=$(( $NEW_HOURS + 1 ))
            NEW_MINUTES=$(( ($NEW_MINUTES + 30) % 60 ))
        fi
    elif (( $NEW_HOURS == 0 ));  # Add 12 hours
    then
        NEW_HOURS=12
    else # Double the amount of hours
        NEW_HOURS=$(( 2 * $NEW_HOURS ))
    fi

    if (( $NEW_HOURS < 12 )) && (( $NEW_DAYS == 0 ));
    then
        new_partition="short"
        new_time_limit=$NEW_HOURS:$NEW_MINUTES:$NEW_SECONDS
    else
        new_partition="medium"
        new_n_inner_search=$(( $new_n_inner_search / 2 > 0 ? $new_n_inner_search / 2 : 1 ))

        if (( $NEW_HOURS < 24 ));
        then
            new_time_limit=$NEW_DAYS-$NEW_HOURS:$NEW_MINUTES:$NEW_SECONDS
        else
            new_time_limit=$(( $NEW_DAYS + 1 ))-$(( $NEW_HOURS % 24 )):$NEW_MINUTES:$NEW_SECONDS
        fi

    fi
}


function update_requirements() {
    if [[ $STATE_1 == "OUT_OF_MEMORY" || $STATE_2 == "OUT_OF_MEMORY" ]]
    then
        add_memory
    fi
    if [[ $STATE_1 == "TIMEOUT" || $STATE_2 == "TIMEOUT" ]]
    then
        add_time
    fi
}