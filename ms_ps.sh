#!/bin/bash

SELFING=false
S="0.0"
SUBPOPS=false
N="0"

# scan the presence of '-S' flag. '-S' is a new flag indicating the precense
# of partial-selfing with rate specified by the immediately following parameter.
# while getopts "S:I:" opt; do
# while true; do
ORIGARGV="$@"
while true; do
    case "$1" in
        -S) SELFING=true
            S="$2"
            shift;;

        -I) SUBPOPS=true
            N="$2"
            shift;;
        *) shift;;
    esac
    if [ $# -le 0 ]; then
        break
    fi
done

set -- $ORIGARGV

if [ x"$SELFING" = "xtrue" ]; then
    # When partial selfing is present, two things have to be performed before invoking ms.
    # - Determine if there any pair of samples is taken from a single individual.
    #   + If this is the case, determine if such pairs coalescece immediately.
    #   + If they coalesce immediately, change the number of samples to pass on to ms.
    # - Rescale parameters (coalescence and recombination rate).

    declare -a PARAMS=()

    if [ x"$SUBPOPS" = "xtrue" ] & [ "$N" -gt 1 ]; then

    fi

    PARAMS=("${PARAMS[@]}" "$2")
    shift 2

    while true; do
        case "$1" in
            -S) shift 2;;       # skip "-S" and its mandatory parameter.
            # TODO: add special flags that need to be modified.
            *) # Otherwise, just store the unmodified parameters.
                PARAMS=("${PARAMS[@]}" "$1")
                shift;;
        esac
        if [ $# -le 0 ]; then
            break
        fi
    done
    echo ms "${PARAMS[@]}"
else
    # When partial selfing is not present, all parameters should be passed to ms as-is.
    echo ms "$@"
fi
