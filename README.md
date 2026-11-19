# Portal Web TechAndes S.A.S.

## 1. Descripción del proyecto

TechAndes es una aplicación web desarrollada para gestionar las actividades de una empresa dedicada a la venta de productos tecnológicos. El sistema permite administrar productos, clientes, ventas, pedidos e informes.

## 2. Tecnologías utilizadas

- Python
- Flask
- MySQL
- HTML5
- CSS3
- Jinja2
- PyMySQL

## 3. Módulos del sistema

El portal cuenta con los siguientes módulos:

- Inicio de sesión.
- Panel principal.
- Gestión de productos.
- Gestión de clientes.
- Registro de ventas.
- Gestión de pedidos.
- Informes de ventas.
- Control de acceso por roles.

## 4. Roles de usuario

**Administrador (ADMIN):** cuenta con permisos para gestionar los diferentes módulos del sistema y consultar los informes.

**Vendedor (VENDEDOR):** puede realizar las funciones correspondientes a la gestión de ventas, clientes, productos y pedidos, según sus permisos.

## 5. Estructura del proyecto

- `app.py`: archivo principal de la aplicación.
- `db.py`: conexión con la base de datos.
- `seguridad.py`: funciones de seguridad y permisos.
- `rutas/`: contiene las rutas de los módulos.
- `templates/`: contiene las páginas HTML.
- `static/`: contiene los archivos CSS e imágenes.
- `sql/`: contiene los scripts de la base de datos.
- `requirements.txt`: lista de dependencias del proyecto.
- `.env.example`: ejemplo de configuración de variables de entorno.

## 6. Instalación y ejecución

Para ejecutar el proyecto se requiere tener instalado Python y MySQL.

1. Descargar el repositorio de GitHub.
2. Crear un entorno virtual de Python.
3. Instalar las dependencias incluidas en `requirements.txt`.
4. Configurar las variables de conexión a MySQL en el archivo `.env`.
5. Ejecutar los scripts SQL para preparar la base de datos.
6. Iniciar la aplicación mediante `python app.py`.
7. Abrir el navegador en `http://127.0.0.1:5000`.

## 7. Usuarios de prueba

El sistema dispone de usuarios de prueba con dos roles: ADMIN y VENDEDOR. Las cuentas y sus respectivas credenciales se encuentran configuradas en la base de datos.

## 8. Repositorio

Proyecto alojado en GitHub:

https://github.com/xXORLANDOXx726/techandes-portal

## 9. Autor

Proyecto académico desarrollado para el taller de aplicación web con Flask.