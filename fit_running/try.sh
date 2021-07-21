#!/bin/bash
TIME_LIMIT="09:1:00"

IFS=":" read -ra SPLIT_TIME_LIMIT <<< $TIME_LIMIT
HOURS=$(( 10#${SPLIT_TIME_LIMIT[0]} ))
MINUTES=$(( 10#${SPLIT_TIME_LIMIT[1]} ))
SECONDS=$(( 10#${SPLIT_TIME_LIMIT[2]} ))

echo "The dependency has been running out of time: $TIME_LIMIT"

if (( $HOURS < 10 ));  # Add 30 minutes
then
    if (( $MINUTES + 30 < 60 ));
    then
        new_time_limit=$HOURS:$(( $MINUTES + 30 )):$SECONDS
    else
        new_time_limit=$(( $HOURS + 1 )):$(( ($MINUTES + 30) % 60 )):$SECONDS
    fi
else  # Add 2 hours
    new_time_limit=$(( $HOURS + 2 )):$(( $MINUTES )):$SECONDS
fi

IFS=":" read -ra SPLIT_NEW_TIME_LIMIT <<< $new_time_limit
NEW_HOURS=$(( 10#${SPLIT_NEW_TIME_LIMIT[0]} ))

if (( $NEW_HOURS < 12 ));
then
    new_partition="short"
else
    new_partition="medium"
fi

echo "Rescheduling the job with more time: $new_time_limit. Same memory $MEMORY_LIMIT"
echo "new_partition $new_partition"