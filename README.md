##Esta es una aplicación desarrollada con [FastAPI](https://fastapi.tiangolo.com/) que expone un conjunto de endpoints RESTful. Está dockerizada para facilitar su despliegue y pruebas locales o en producción.


 Requisitos
- [Docker](https://docs.docker.com/get-docker/) instalado

## Cómo correr la aplicación con Docker
1. Construir la imagen, te ubicas en la carpeta del proyecto a nivel del archivo dockerfile
2. Ejecutar
```bash
docker build -t app .
```
3. Crear el contenedor
```bash
docker run -d --name fastapi-container -p 8000:8000 fastapi-app
```
4. Acceder a la API
- La aplicación estará disponible en:
    - http://localhost:8000
- La documentación interactiva de la API (Swagger UI):
    - http://localhost:8000/docs