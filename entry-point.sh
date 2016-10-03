#!/bin/bash
set -e

# this if will check if the first argument is a flag
# but only works if all arguments require a hyphenated flag
# -v; -SL; -f arg; etc will work, but not arg1 arg2
if [ "${1:0:1}" = '-' ]; then
    set -- python /application/manage.py "$@";
fi

# check for the expected command
case "$1" in
    dumpdata|loaddata|makemigrations|migrate|runserver|changepassword|createsuperuser)
        set -- python /application/manage.py "$@";
    ;;
esac

# else default to run whatever the user wanted like "bash"
exec "$@"
