#!/bin/sh
Xvfb :1 &

timeout 10 sh -c 'while ! xset q &>/dev/null; do echo "Waiting for Xvfb..."; sleep 1; done'
if ! xset q &>/dev/null; then
  echo "Xvfb failed to start within 10 seconds."
fi

/ansys_inc/v261/fluent/bin/fluent "$@"
