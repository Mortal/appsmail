#!/bin/bash

set -euo pipefail

MAIL_FROM=rav@cs.au.dk
RELAY_HOST=smtp-clients.au.dk
RELAY_PORT=587
RELAY_USER=au306325@uni.au.dk
read -p "Password for $RELAY_USER at $RELAY_HOST: " -s RELAY_PASS
echo
export MAIL_FROM RELAY_HOST RELAY_PORT RELAY_USER RELAY_PASS
venv/bin/python -m appsmail
