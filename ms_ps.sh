#!/bin/bash

ARGS=$(getopt -o "S:" -- "$@")

eval set -- "$ARGS"

SELFING=false
S="0.0"

# scan the presence of '-P' flag indicating the presence of partial-selfing with rate "S".
while true; do
    case "$1" in
        -S)
            SELFING=true
            S="$2"
            shift 2;;
        --)
            shift
            break;;
        *)
            shift;;
    esac
done

if [ x"$SELFING" = "xtrue" ]; then
    # When partial selfing is present, two things have to be performed before invoking ms.
    # - Determine if there any pair of samples is taken from a single individual.
    #   + If this is the case, determine if such pairs coalescece immediately.
    #   + If they coalesce immediately, change the number of samples to pass on to ms.
    # - Rescale parameters (coalescence and recombination rate).

    declare -a PARAMS=()

    while true; do
        case "$1" in
            # TODO: add special flags that need to be modified.
            -a)
                ;;
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
