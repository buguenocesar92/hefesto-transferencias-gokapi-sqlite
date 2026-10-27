# Política de tratamiento de datos personales — Transferencias (Hefesto Studio)

Estado: vigente desde 2026-10-20. Responsable del tratamiento: el cliente que
opera el kit. Este documento describe qué datos guarda el kit, por qué, cuánto
tiempo los retiene y cómo se exercise los derechos del titular (Ley 21.719).

## 1. Qué datos guarda este kit

El kit de transferencias (Gokapi) guarda, por archivo compartido:

- **Archivos**: nombre, contenido, tamano y fecha de subida de cada archivo que
  el usuario comparte a traves de un enlace.
- **Metadatos del enlace**: identificador unico, fecha de creacion, numero de
  descargas, direccion IP de quien descarga y expiracion.
- **Token de API**: la clave del servicio en `config.json` (volumen `config`).
  Es una credencial de la aplicacion, no del usuario, pero da acceso a los
  enlaces.
- **Cuentas**: usuario, hash de contrasena y rol.
- **Copias locales de respaldo**: `backups/<timestamp>/` con los archivos
  compartidos (`data.tar.gz`), la configuracion cifrada (`config.tar.gz.age`) y
  los nombres de variable del `.env` (`env.vars`).

La direccion IP de quien descarga y la fecha son datos personales de quien
descarga, aunque el kit no los vincule a un nombre.

## 2. Qué datos NO guarda este kit

- El `.env` **no** se copia en claro al respaldo: solo sus nombres de
  variable (`env.vars`) y, si hay un receptor `age` configurado, el `.env`
  cifrado (`env.age`).
- El volumen de configuracion, que contiene el token de API, **tampoco** viaja
  en claro: se cifra con `age` (`config.tar.gz.age`) o no se incluye y el
  manifiesto lo declara. Ver `docs/CONTRATO-RESPALDO.md`, regla 5.
- El kit no guarda el contenido de los enlaces en ningun indice externo ni
  envia archivos a servicios de terceros.

## 3. Base legal y deberes

- **Minimización**: el kit guarda lo necesario para servir el archivo por enlace. No guarda
  metadatos del dispositivo, ni el contenido fuera del volumen de datos, ni
  el historial de navegacion de quien descarga.
- **Finalidad**: compartir archivos mediante enlaces temporales. Los datos no se usan para otros fines ni se ceden a terceros.
- **Seguridad**: los respaldos se cifran en reposo con `age` hacia el destino del operador, la clave privada no está en este servidor, el `.env` y el token de API nunca salen en claro.
- **Auditoría**: cada respaldo y cada restauración dejan registro en `logs/restore.log` con origen, sha256 verificado, destino y resultado. Es registro de actividades de tratamiento: no guarda valores de secretos ni tokens.

## 4. Retención

| Dato | Dónde | Retención por defecto | Quién lo borra |
|---|---|---|---|
| Archivos compartidos | volumen `data` (SQLite) | hasta la expiracion que el operador defina en Gokapi | el operador |
| Metadatos de descargas (IP, fecha) | volumen `data` | mientras el operador los mantenga | el operador |
| Token de API | volumen `config`, cifrado en el respaldo | mientras el kit este en uso; rotar si se sospecha uso indebido | el operador |
| Respaldos en disco | `backups/<timestamp>/` | **a definir por el operador**; el kit no borra nada por su cuenta | el operador |
| Registro de auditoría | `logs/restore.log` | append-only; se trunca por política del cliente | el operador |

**El kit no borra respaldos ni datos por su cuenta.** Borrar es una decisión del
operador, porque un respaldo borrado no se recupera.

## 5. Derechos del titular (acceso, rectificación y supresión)

El cliente que opera el kit debe poder atender las solicitudes de las
personas que descargan de un enlace:

1. **Acceso**: entregar a quien lo solicite la informacion de descargas de un
   enlace concreto (fecha e IP), dentro de lo que la ley permita.
2. **Rectificación**: corregir la expiracion de un enlace o regenerarlo.
3. **Supresión**: eliminar el archivo compartido y los respaldos que lo
   contengan, y dejar constancia en el registro de auditoria.
4. **Revocación del consentimiento**: eliminar el enlace y sus metadatos de
   descarga.

El contenido de los archivos lo decide el cliente: el kit no sabe quien es el
titular de un archivo, por eso el operador es quien debe responder.

## 6. Verificación

- `bats tests/backup_restore.bats` comprueba, con datos sintéticos, que el
  `.env` ni el volumen de configuracion quedan en claro, que el manifiesto lleva
  las cinco claves, que un artefacto alterado se rechaza y que un destino no
  vacío aborta la restauración.
- `gitleaks` corre en CI sobre el repositorio y su historial.
