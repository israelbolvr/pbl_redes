#!/usr/bin/env bash
# Use este script para testar se um determinado host/porta TCP está disponível

TIMEOUT=15
QUIET=0
HOST=""
PORT=""

echoerr() { if [ "$QUIET" -ne 1 ]; then echo "$@" 1>&2; fi }

usage()
{
    echo "Usage: $0 host:port [-s] [-t timeout] [-- command args]"
    exit 1
}

wait_for()
{
    if [ "$TIMEOUT" -gt 0 ]; then
        echoerr "Waiting for $HOST:$PORT for $TIMEOUT seconds..."
    else
        echoerr "Waiting for $HOST:$PORT without a timeout..."
    fi

    start_ts=$(date +%s)
    while :
    do
        if nc -z "$HOST" "$PORT"; then
            end_ts=$(date +%s)
            echoerr "Connected to $HOST:$PORT after $((end_ts - start_ts)) seconds."
            break
        fi
        sleep 1
    done
    return 0
}

while [ $# -gt 0 ]
do
    case "$1" in
        *:* )
        HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
        PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
        shift 1
        ;;
        --)
        shift
        break
        ;;
        *)
        usage
        ;;
    esac
done

if [ "$HOST" = "" ] || [ "$PORT" = "" ]; then
    echo "Error: you need to provide a host and port to test."
    usage
fi

wait_for

exec "$@"
