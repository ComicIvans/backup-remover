# Backup remover

 Script de python para eliminar las copias de seguridad de Miniecraft echas en Minio siguiendo un criterio de conservación.

Para probarlo:
1. Clonar repositorio.
2. Crear un entorno virtual de Python con `python3 -m venv .env`.
3. Cambiar al entorno virtual desde Visual Studio con `Ctrl + Shift + P` y seleccionar intérprete o desde la terminal con `source .env/bin/activate`.
4. Instalar los paquetes necesarios `pip3 install minio` y `pip3 install pyyaml`.
5. Crear el archivo `config.yml` con:
```yml
MINIO_URL: localhost:9000
MINIO_ACCESS_KEY: abc
MINIO_SECRET_KEY: abc123
MINIO_BUCKETS: [
  bucket-name,
  ]
MINIO_SECURE: true
MINIO_REGION: es
```
6. Ejecutar `python3 main.py`.