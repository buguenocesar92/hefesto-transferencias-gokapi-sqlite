# Cifrado, caducidad y límites
El asistente ofrece distintos niveles de cifrado. El kit no impone ni afirma que el cifrado esté activado: debe seleccionarlo y comprobarlo en la instancia. La documentación upstream indica que su cifrado no ha sido auditado; no presentar el servicio como certificado para cualquier dato sensible.

Las claves/configuración y los archivos se respaldan juntos. Si se pierde una clave necesaria, no se promete recuperar archivos cifrados. Si se elige una contraseña maestra de arranque, deberá introducirse después de cada reinicio y diseñar su custodia; el Compose no resuelve ese paso interactivo.

**No cambie las opciones de cifrado sobre archivos existentes sin revisar el procedimiento upstream y guardar una copia comprobada.** La documentación de esta versión advierte que cambiar configuración relacionada con cifrado puede borrar archivos ya cifrados. Activarlo después tampoco cifra retroactivamente todos los archivos previos.

La caducidad y el límite de descargas forman parte de la política de entrega. Pruebe límites con archivos de ensayo; reproducciones/previsualizaciones y descargas concurrentes pueden afectar expectativas. Al restaurar una copia antigua pueden volver contadores/estados anteriores; revise enlaces y expiración antes de hacerla pública.

Una transferencia temporal no es un archivo documental permanente. No prometa conservación indefinida. Defina tamaños, espacio total, retención y disponibilidad por cliente. La reserva mínima de disco no es una cuota por cuenta; monitorice volumen y copias.

La contraseña del enlace no sustituye autenticación del operador. Compártala por un canal separado cuando corresponda. Los destinatarios pueden reenviar enlaces o copias descargadas; no se puede revocar una copia ya obtenida.

No incluye antivirus ni análisis de contenido. Usuarios autorizados cargan archivos; la creación de solicitudes para invitados no está habilitada por defecto para todos. El administrador debe revisar permisos si decide habilitarla. La API está oculta a usuarios no administradores por configuración, pero debe revisar y proteger las claves que existan.
