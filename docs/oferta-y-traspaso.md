# Oferta y entrega
Servicio sugerido: portal de transferencia con marca, usuarios autorizados, límites definidos, alojamiento, copias y soporte. Casos: entrega de diseños, fotografías, documentación de proyectos y archivos de trabajo.

Cotice por espacio contratado, transferencia, usuarios y atención; no se fijan precios ficticios ni SLA sin medir. Para carpetas compartidas, edición colaborativa e historial documental, utilizar Nextcloud. Para expedientes o archivo permanente, otra herramienta con ese propósito. Gokapi cubre entrega temporal de archivos.

## Plantilla manual de entrega al cliente
Registrar proyecto/referencia, archivo, tamaño, destinatario, caducidad, límite de descargas y quién autorizó la entrega. Verificar el enlace en un navegador separado. No introducir información sensible en nombres de archivo o URL si no debe ser pública.

## Traspaso
Entregar dominio/proxy, servidor, versión/digest, volúmenes, cuentas administradoras, configuración de cifrado y copia restaurada de prueba. Transferir secretos mediante gestor y revocar accesos del operador anterior. Una instalación por cliente; si comparte host use COMPOSE_PROJECT_NAME y VOLUME_PREFIX únicos y consistentes.

## Odoo y otras herramientas
Puede adjuntar el enlace de una entrega a una tarea o comunicación Odoo. Es un vínculo temporal, no un adjunto permanente: conservar el original donde corresponda y mostrar la caducidad. No se incluye conector Odoo/n8n ni envío automático de mensajes.

Para pasar los archivos a Nextcloud u otro repositorio, descargar mediante el flujo autorizado y cargar en el destino; los blobs cifrados de data no son necesariamente archivos legibles. Conservar solo la SQLite no traslada los archivos. Probar un lote pequeño y cotejar hashes de los archivos descargados antes del corte.

Conservar créditos y obligaciones AGPL-3.0 de Gokapi y las dependencias aplicables. El kit ofrece despliegue y operación; no presenta el motor como desarrollo original de Hefesto.
