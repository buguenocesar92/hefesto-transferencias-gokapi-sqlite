#!/usr/bin/env python3
"""Restauracion de hefesto-transferencias en un destino nuevo y vacio.

Sin --confirmar CONFIRMAR_RESTAURACION no se escribe nada; con --dry-run se
simula. El volumen de configuracion, cifrado con age, se restaura solo si el
operador entrega su clave privada (AGE_IDENTITY_FILE): es un insumo externo.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from respaldo_contrato import (RespaldoError, auditar, descifrar_con_age, ejecutar,
                               ejecutar_check, escribir_informe, opciones_restore)

SOFTWARE = "hefesto-transferencias"
VERSION = "2.2.4"
DATABASE = "sqlite"
RAIZ = Path(__file__).resolve().parents[1]
os.chdir(RAIZ)
os.umask(0o077)
PROHIBIDOS = ["config.tar.gz", "config.json"]


def dc(*a, **kw):
    return subprocess.run(["docker", "compose", *a], check=True, **kw)


def main():
    modo, origen = opciones_restore(sys.argv[1:])
    origen = Path(origen).resolve()
    ejecutar_check(str(origen), SOFTWARE, VERSION, DATABASE, prohibidos=PROHIBIDOS)
    if modo == "dry-run":
        print("Simulacion: el respaldo es integro y no se escribio nada.")
        print("Para restaurar de verdad: --confirmar CONFIRMAR_RESTAURACION")
        return 0
    if dc("ps", "--status", "running", "-q", "app", capture_output=True, text=True).stdout.strip():
        raise RespaldoError("Detener app antes de restaurar", 5)
    for volumen in ("data", "config"):
        ocupado = dc("run", "--rm", "--no-deps", "-T", "--entrypoint", "find", "filetools",
                     "/" + volumen, "-mindepth", "1", "-maxdepth", "1",
                     capture_output=True, text=True).stdout.strip()
        if ocupado:
            raise RespaldoError("Volumen no vacio: " + volumen, 5)
    with (origen / "data.tar.gz").open("rb") as f:
        dc("run", "--rm", "--no-deps", "-T", "--entrypoint", "tar", "filetools",
           "-xzf", "-", "-C", "/data", stdin=f)
    if (origen / "config.tar.gz.age").is_file():
        with tempfile.TemporaryDirectory(prefix="hefesto-transferencias-restore-") as d:
            plano = Path(d) / "config.tar.gz"
            descifrar_con_age(origen / "config.tar.gz.age", plano)
            with plano.open("rb") as f:
                dc("run", "--rm", "--no-deps", "-T", "--entrypoint", "tar", "filetools",
                   "-xzf", "-", "-C", "/config", stdin=f)
    else:
        print("El respaldo no trae la configuracion cifrada: hay que reconfigurar el token "
              "de API en el destino (ver docs).")
    dc("run", "--rm", "--no-deps", "permissions")
    escribir_informe(origen, software=SOFTWARE, version=VERSION, database=DATABASE,
                     modo="confirmado", resultado="restaurado", destino=str(RAIZ))
    auditar(RAIZ, operacion="restore", kit=SOFTWARE, origen=str(origen), destino=str(RAIZ),
            resultado="restaurado")
    print("Datos restaurados. Probar los enlaces por entorno privado antes del corte DNS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(ejecutar(main))
