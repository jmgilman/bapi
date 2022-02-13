#!/bin/sh

set -e

# Activate venv
. /opt/pysetup/.venv/bin/activate

# Exec passed command
exec "$@"