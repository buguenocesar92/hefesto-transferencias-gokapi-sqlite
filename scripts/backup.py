#!/usr/bin/env python3
"""Respaldo de hefesto-transferencias (Gokapi + SQLite).

Reglas de material sensible:
- El .env nunca se copia en claro: solo env.vars y, si hay receptor age, el
  .env cifrado (env.age).
- El volumen de configuracion contiene config.json con el token de API y la
  clave de administracion: se cifra en linea con age (config.tar.gz.age) o no
  viaja y el manifiesto lo declara. Nunca queda en claro en el disco.
Ver docs/CONTRATO-RESPALDO.md.
"""
import datetime
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from respaldo_contrato import (RespaldoError, cifrar_con_age, escribir_manifiesto,
                               ejecutar, exportar_env, marcar_fallido, receptor_age)

SOFTWARE = "hefesto-transferencias"
VERSION = "2.2.4"
DATABASE = "sqlite"
RAIZ = Path(__file__).resolve().parents[1]
os.chdir(RAIZ)
os.umask(0o077)


def dc(*a, **kw):
    return subprocess.run(["docker", "compose", *a], check=True, **kw)


def main():
    carpeta = RAIZ / "backups" / datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    carpeta.mkdir(parents=True, mode=0o700)
    running = bool(dc("ps", "--status", "running", "-q", "app", capture_output=True, text=True).stdout.strip())
    try:
        dc("stop", "app")
        # Archivos compartidos: no contienen secretos.
        with (carpeta / "data.tar.gz").open("wb") as f:
            dc("run", "--rm", "--no-deps", "-T", "--entrypoint", "tar", "filetools",
               "-czf", "-", "-C", "/data", ".", stdout=f)
        meta = exportar_env(RAIZ, carpeta)
        if meta.get("env_cifrado"):
            # El volumen de configuracion lleva el token de API: se cifra en linea.
            receptor = receptor_age()
            cifrar_con_age(
                lambda flujo: dc("run", "--rm", "--no-deps", "-T", "--entrypoint", "tar",
                                 "filetools", "-czf", "-", "-C", "/config", ".", stdout=flujo),
                carpeta / "config.tar.gz.age", receptor)
            meta["config"] = "config.tar.gz.age (cifrado con age)"
        else:
            meta["config"] = ("excluido: el volumen de configuracion contiene el token de API "
                              "y no hay receptor age configurado")
        if (RAIZ / "compose.yaml").is_file():
            shutil.copy2(RAIZ / "compose.yaml", carpeta / "compose.yaml")
        artefactos = [n for n in ("data.tar.gz", "env.vars", "compose.yaml")
                      if (carpeta / n).is_file()]
        for n in ("env.age", "config.tar.gz.age"):
            if (carpeta / n).is_file():
                artefactos.append(n)
        escribir_manifiesto(carpeta, SOFTWARE, VERSION, DATABASE, artefactos, extra=meta)
    except Exception:
        marcar_fallido(carpeta, SOFTWARE, VERSION, DATABASE)
        raise
    finally:
        if running:
            dc("start", "app")
    print("Respaldo completo:", carpeta)
    print("El .env y el volumen de configuracion no viajan en claro: solo cifrados con age "
          "o fuera del respaldo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(ejecutar(main))
