# Backup remover

 Script de python para eliminar las copias de seguridad de Miniecraft echas en Minio siguiendo un criterio de conservación.

Para probarlo:
1. Clonar repositorio.
2. Crear un entorno virtual de Python con `python3 -m venv .env`.
3. Cambiar al entorno virtual desde Visual Studio con `Ctrl + Shift + P` y seleccionar intérprete o desde la terminal con `source .env/bin/activate`.
4. Instalar los paquetes necesarios `pip3 install minio` y `pip3 install python-dotenv`.
5. Crear el archivo `minio.env` con:
```dotenv
MINIO_URL="localhost:9000"
MINIO_ACCESS_KEY="your_access_key"
MINIO_SECRET_KEY="your_secret_key"
MINIO_BUCKET="bucket-name"
MINIO_SECURE="False"
MINIO_REGION="es"
```
6. Ejecutar `python3 main.py`.