#!/bin/bash

set -e

# Activate venv
. /opt/pysetup/.venv/bin/activate

if [[ -z "${USE_EXAMPLE}" ]]; then
    echo "Generating example Beancount data..."
    bean-example -o "$BAPI_WORK_DIR/$BAPI_ENTRYPOINT"
fi

# Exec passed command
exec "$@"