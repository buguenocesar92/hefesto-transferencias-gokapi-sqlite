#!/bin/sh
set -eu
if [ "${HEFESTO_BOOTSTRAP:-false}" != true ]; then
  [ "${INITIAL_SETUP_COMPLETE:-false}" = true ] || { echo 'Complete el asistente privado antes de produccion'; exit 1; }
  [ -s /app/config/config.json ] || { echo 'Falta configuracion; no abrir asistente publico'; exit 1; }
fi
exec /app/run.sh
