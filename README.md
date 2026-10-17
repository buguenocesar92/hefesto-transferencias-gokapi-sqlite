# Hefesto Transferencias — Gokapi + SQLite
Kit para entregar archivos a clientes mediante enlaces con caducidad, límite de descargas y opciones de contraseña. Basado en Gokapi 2.2.4; incluye Compose para Coolify/VPS, alta privada, volúmenes, respaldos y restauración.

## Stack y alcance
- Imagen del proyecto fijada por digest, ejecución de app UID/GID 1000.
- SQLite nativo y archivos locales en /app/data; configuración y claves en /app/config.
- No usa Supabase: esta versión soporta SQLite/Redis, no PostgreSQL como motor de metadatos.
- No se configura S3/R2, Redis, correo, cobros, antivirus ni integraciones externas.
- Cuentas y opciones de cifrado se definen en el asistente. No se incluyen contraseñas de fábrica ni datos reales.

Empiece por docs/instalacion.md. Requiere Docker, Compose v2, Python 3.11+, dominio HTTPS y espacio de almacenamiento.

**Estado:** revisión estática del kit y código/documentación de la versión. No se ejecutaron Docker, asistente, cifrado ni descargas reales. Requiere aceptación antes de producción.
