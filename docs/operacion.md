# Respaldo y restauración
## Copia coherente
`python3 scripts/backup.py` detiene app, archiva data+config completos y guarda .env/Compose con hashes. Reinicia app si estaba activa. Al detenerla, copia SQLite junto a archivos y claves sin escrituras de la aplicación. Evite CLI, otras réplicas y cambios manuales durante la ventana.

Los respaldos incluyen archivos de clientes, hashes, tokens y claves de descifrado. Cifre y guarde fuera del VPS con acceso restringido. El manifiesto completed indica que terminaron las copias, no que se haya probado una restauración. SHA-256 detecta daños, no autenticidad. No se programa automáticamente: configure frecuencia, retención y alertas según contrato.

## Restauración en destino vacío
1. Prepare otro directorio/VPS con mismas imágenes. Genere .env y VOLUME_PREFIX nuevo. No inicie app ni configure de nuevo.
2. `python3 scripts/restore.py /ruta/respaldo`. Verifica producto, versión, hashes, rutas y que ambos volúmenes estén vacíos. No sobrescribe ni fusiona.
3. Mantenga dominio de producción sin apuntar al destino todavía. Inicie por bootstrap y túnel para comprobar cuentas y configuración. Como se conserva la URL original, los enlaces pueden apuntar al origen: use una resolución DNS/hosts de ensayo con HTTPS para validar el mismo dominio en el destino.
4. No cambie cifrado/salts/contraseñas para «arreglar» una restauración. Verifique descarga y descifrado de archivos de prueba, caducidad y contadores, y la integridad de la SQLite con las herramientas que corresponda antes de entregar.
5. Revoque enlaces o claves que no deban reactivarse y revise expiraciones recuperadas. Una copia antigua puede contener archivos que luego fueron eliminados del origen.
6. Marque INITIAL_SETUP_COMPLETE=true y quite bootstrap. Tras aceptación, haga corte DNS y mantenga una única instancia activa. Si cambia dominio, use reconfiguración nativa cuidadosamente y actualice enlaces donde corresponda.

Si una restauración falla parcialmente, investigue y prepare otro destino vacío; nunca borre el origen para reintentar. El script rechaza enlaces simbólicos y tipos especiales en los archivos. Conserve el ZIP, ajustes de proxy/DNS y secretos fuera del volumen si hubiera elegido alguno.

Este respaldo cubre SOLO SQLite y almacenamiento LOCAL. Si se habilita Redis o S3/R2, debe agregarse su exportación/copia antes de considerar completo el backup. No basta con conservar cloudconfig.yml para respaldar objetos remotos.

## Mantenimiento
Respaldar, probar actualización en clon, revisar cambios upstream y después actualizar digest. Bajar solo imagen no garantiza revertir migraciones; restaurar data+config coherentes. Monitorizar disco, errores HTTP, tiempo de carga/descarga y copias. El healthcheck verifica HTTP, no garantiza todos los flujos ni integridad del contenido.
