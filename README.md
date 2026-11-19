# Portal Web TechAndes S.A.S.

## 1. Descripción del proyecto

TechAndes es una aplicación web desarrollada para gestionar las actividades de una empresa dedicada a la comercialización de productos tecnológicos. El sistema permite administrar productos, clientes, ventas, pedidos e informes mediante una plataforma web con acceso por usuarios y roles.

## 2. Tecnologías utilizadas

- Python 3
- Flask
- MySQL 8
- HTML5
- CSS3
- Jinja2
- PyMySQL
- python-dotenv
- Cryptography

## 3. Requisitos

Para ejecutar el proyecto se necesita:

- Python 3.10 o superior.
- MySQL 8 en ejecución.
- Visual Studio Code u otro editor de código.
- MySQL Workbench para administrar la base de datos.
- Navegador web.

## 4. Base de datos

La aplicación utiliza una base de datos MySQL llamada `techandes`.

Los archivos SQL se encuentran organizados de la siguiente manera:

1. `Base de datos_ clase (1).sql`: contiene la creación de la base de datos y la estructura de las tablas principales: categorías, clientes, empleados, productos, pedidos y detalle de pedidos.
2. `sql/01_usuarios.sql`: crea la tabla de usuarios, configura los roles de acceso y registra las cuentas de prueba.
3. `sql/02_permisos.sql`: crea el usuario de conexión `techandes_api` y le asigna permisos para consultar, insertar, actualizar y eliminar registros en la base de datos.

**Orden de ejecución:** primero se debe ejecutar el archivo original de la base de datos, después el archivo de usuarios y finalmente el archivo de permisos.

Nota: antes de ejecutar el script de usuarios deben existir los ocho empleados correspondientes, ya que las cuentas están relacionadas con sus registros mediante una llave foránea.

## 5. Instalación y configuración

Para instalar y ejecutar el proyecto en Windows, siga estos pasos:

**1. Abrir el proyecto**

Descargar el repositorio de GitHub y abrir la carpeta `techandes-portal` en Visual Studio Code.

**2. Crear el entorno virtual**

```bash
python -m venv .venv
```

**3. Activar el entorno virtual**

```bash
.venv\Scripts\activate
```

**4. Instalar las dependencias**

```bash
pip install -r requirements.txt
```

**5. Crear el archivo de configuración**

```bash
copy .env.example .env
```

**6. Configurar la conexión**

Abrir el archivo `.env` y configurar las variables de conexión a MySQL:

- DB_HOST: localhost
- DB_PORT: 3306
- DB_USER: techandes_api
- DB_PASSWORD: contraseña configurada para el usuario de MySQL.
- DB_NAME: techandes

También se debe configurar una clave secreta para Flask mediante `SECRET_KEY`.

## 6. Ejecución del proyecto

Para iniciar el servidor, activar el entorno virtual y ejecutar:

```bash
python app.py
```

Una vez iniciado, abrir el navegador e ingresar a:

http://127.0.0.1:5000

El sistema solicita iniciar sesión antes de acceder a las funcionalidades del portal.

## 7. Usuarios de prueba

El sistema cuenta con ocho usuarios de prueba distribuidos en dos roles:

| Usuario | Rol | Contraseña |
|---|---|---|
| mprieto | ADMIN | Admin2026* |
| hbustos | ADMIN | Admin2026* |
| crobayo | ADMIN | Admin2026* |
| klozada | VENDEDOR | Ventas2026* |
| ytafur | VENDEDOR | Ventas2026* |
| boviedo | VENDEDOR | Ventas2026* |
| lmurcia | VENDEDOR | Ventas2026* |
| fcuellar | VENDEDOR | Ventas2026* |

**Administrador (ADMIN):** dispone de permisos administrativos para gestionar las funcionalidades autorizadas del sistema.

**Vendedor (VENDEDOR):** dispone de acceso a las funcionalidades comerciales según los permisos asignados.

## 8. Módulos del sistema

El portal cuenta con los siguientes módulos:

- **Inicio:** panel principal con información general del sistema.
- **Productos:** permite consultar y gestionar el catálogo de productos.
- **Clientes:** permite registrar, consultar y buscar clientes.
- **Nueva venta:** permite registrar ventas y pedidos.
- **Pedidos:** permite consultar y gestionar los pedidos registrados.
- **Informes:** permite consultar información y reportes de ventas.
- **Autenticación:** controla el inicio de sesión y el acceso según los roles de usuario.

## 9. Estructura del proyecto

El proyecto está organizado de la siguiente manera:

- `app.py`: archivo principal que inicializa la aplicación Flask y registra los módulos.
- `db.py`: administra la conexión con MySQL y las operaciones de consulta y modificación de datos.
- `seguridad.py`: contiene las funciones relacionadas con la seguridad y los permisos.
- `rutas/`: contiene las rutas de los diferentes módulos del sistema.
- `templates/`: contiene las plantillas HTML de las páginas.
- `static/`: almacena los archivos CSS e imágenes.
- `sql/`: contiene los scripts SQL de usuarios y permisos.
- `requirements.txt`: contiene las dependencias necesarias para ejecutar el proyecto.
- `.env.example`: contiene las variables de ejemplo para configurar la aplicación y la conexión con MySQL.
- `.env`: archivo local con la configuración de conexión y seguridad.

## 10. Repositorio

El proyecto se encuentra alojado en GitHub:

https://github.com/xXORLANDOXx726/techandes-portal

## 11. Autor

Proyecto académico desarrollado para el taller de aplicación web con Flask.

**Autor:** Orlando Salcedo