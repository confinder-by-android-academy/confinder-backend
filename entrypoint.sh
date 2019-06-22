#!/usr/bin/env bash
set -e

# Choose command
case "$1" in
app)
    shift
    exec aioworkers -c confinder/config.yaml
    ;;
tests)
    shift
    pipenv install --dev --system
    pytest
    ;;
*) exec "$@"
esac

exit $?
