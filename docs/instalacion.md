# Instalación privada
1. `python3 scripts/configure.py`. Configure VOLUME_PREFIX único y límites en .env. No se genera contraseña: el propietario la elige durante el asistente.
2. `docker compose -f compose.yaml -f compose.bootstrap.yaml config --quiet`
3. `docker compose -f compose.yaml -f compose.bootstrap.yaml up -d app`. La tarea permissions prepara volúmenes para UID/GID 1000. La app conserva el lanzador nativo con tini.
4. Desde su equipo: `ssh -L 8100:127.0.0.1:8100 usuario@servidor`.
5. Abra http://localhost:8100/setup. Elija autenticación interna con usuario/contraseña robusta, SQLite y almacenamiento local /app/data. Mantenga la DB dentro de ese directorio, por ejemplo sqlite:///app/data/gokapi.sqlite. No seleccione Redis ni almacenamiento cloud para este kit.
6. Configure el nombre Hefesto Transferencias o la marca del cliente y la URL HTTPS final del servicio. El servidor interno escucha HTTP 53842; el proxy termina TLS. No cargue archivos de clientes hasta usar la URL definitiva y comprobar enlaces.
7. Revise opciones de cifrado antes de la primera carga. Lea docs/cifrado-y-limites.md. Para reinicio desatendido, no seleccione una opción que exija escribir contraseña maestra manualmente en cada arranque. Conserve claves/configuración y pruebe recuperación.
8. Finalice y compruebe autenticación. Marque INITIAL_SETUP_COMPLETE=true en .env; es una confirmación del operador, no una auditoría automática de la configuración.
9. `docker compose up -d --force-recreate app` sin override. Asigne dominio HTTPS de Coolify a app, puerto interno 53842. Compruebe que 8100 desapareció. Cree un archivo de ensayo y pruebe todos los enlaces desde otro navegador.

## Coolify y proxy
Importe el directorio completo, preserve ops y los dos volúmenes. Use el mismo proyecto Compose durante bootstrap y producción; de lo contrario puede conectar volúmenes vacíos.

Configure un límite de cuerpo y tiempos de espera coherentes con los archivos y fragmentos: upstream recomienda timeout de 300 segundos. El kit inicia con fragmentos de 20 MB, archivo máximo de 1024 MB y reserva mínima de 2048 MB de disco; ajuste recursos y límite del proxy sin confundir tamaño por fragmento con tamaño total.

Si usa Cloudflare, revise sus límites y comportamiento antes de ofrecer archivos grandes. Mantenga el control de CORS; no lo desactive para ocultar un error de URL. Gokapi puede confiar automáticamente en la red Docker: revise GOKAPI_TRUSTED_PROXIES y su proxy real para evitar confiar en cabeceras de clientes externos.

## Cambiar configuración posteriormente
Muchos parámetros persistentes solo se aplican en el primer asistente. Cambiar MAX_FILESIZE_MB en .env no garantiza que reemplace la configuración ya guardada. Use el procedimiento nativo:

`docker compose stop app`

`docker compose run --rm --no-deps -p 127.0.0.1:8100:53842 --entrypoint /app/run.sh app --reconfigure`

La herramienta muestra credenciales temporales de acceso al asistente en su salida. Trátelas como secretas. Acceda por el mismo túnel, cambie únicamente lo necesario y conserve cifrado/claves. Al terminar, detenga el contenedor temporal y ejecute `docker compose up -d app`.

Respaldar antes de reconfigurar. No ejecutar dos instancias sobre la misma SQLite. No elegir «sin autenticación» salvo diseñar y validar expresamente autenticación externa; este kit utiliza login interno.
