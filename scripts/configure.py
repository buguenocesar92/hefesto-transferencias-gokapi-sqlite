#!/usr/bin/env python3
import os
from pathlib import Path
r=Path(__file__).resolve().parents[1]
try:fd=os.open(r/'.env',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
except FileExistsError:raise SystemExit('Ya existe .env; no se sobrescribe')
with os.fdopen(fd,'w') as f:f.write((r/'.env.example').read_text())
print('.env creado 0600. La contraseña administrativa se elige en el asistente privado, no en este archivo.')
