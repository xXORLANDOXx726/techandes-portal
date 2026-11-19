"""Genera la guía en PDF para explicar el portal. No forma parte de la aplicación."""

from fpdf import FPDF

SALIDA = r"C:\Users\orlan\techandes-portal\Guia_Portal_TechAndes.pdf"
AZUL = (11, 42, 74)
AZUL_MED = (22, 115, 184)
CIAN = (54, 194, 224)
TEXTO = (20, 50, 77)
GRIS = (77, 109, 134)
FONDO = (244, 249, 253)
AMBAR = (255, 244, 214)
VERDE = (222, 246, 232)


class Guia(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*AZUL)
        self.rect(0, 0, 210, 14, "F")
        self.set_fill_color(*CIAN)
        self.rect(0, 14, 210, 1.2, "F")
        self.set_xy(12, 4)
        self.set_font("Arial", "", 9)
        self.set_text_color(255, 255, 255)
        self.cell(0, 6, "Portal TechAndes   ·   Guía para explicar el proyecto", align="L")
        self.ln(16)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(213, 230, 242)
        self.line(14, self.get_y(), 196, self.get_y())
        self.set_font("Arial", "", 8)
        self.set_text_color(*GRIS)
        self.cell(0, 8, f"Uso académico  ·  página {self.page_no()}", align="C")

    def espacio(self, alto=4):
        self.ln(alto)

    def asegurar(self, alto):
        if self.get_y() + alto > 272:
            self.add_page()

    def titulo(self, texto):
        self.asegurar(16)
        self.set_font("Arial", "B", 15)
        self.set_text_color(*AZUL)
        self.multi_cell(0, 8, texto)
        self.set_draw_color(*AZUL_MED)
        y = self.get_y()
        self.set_line_width(0.6)
        self.line(14, y, 70, y)
        self.set_line_width(0.2)
        self.ln(4)

    def subtitulo(self, texto):
        self.asegurar(12)
        self.espacio(2)
        self.set_font("Arial", "B", 12)
        self.set_text_color(*AZUL_MED)
        self.multi_cell(0, 7, texto)
        self.ln(1)

    def parrafo(self, texto):
        self.set_font("Arial", "", 11)
        self.set_text_color(*TEXTO)
        self.multi_cell(0, 6, texto)
        self.ln(1.5)

    def viñeta(self, texto):
        self.set_text_color(*TEXTO)
        x = self.get_x()
        self.set_font("Arial", "B", 11)
        self.set_text_color(*AZUL_MED)
        self.cell(6, 6, "·")
        self.set_font("Arial", "", 11)
        self.set_text_color(*TEXTO)
        self.multi_cell(0, 6, texto)
        self.set_x(x)

    def caja(self, texto, fondo=FONDO):
        self.set_font("Arial", "", 10.5)
        ancho = 182
        alto = self.get_string_width  # placeholder to keep linters calm
        del alto
        lineas = self.multi_cell(ancho - 8, 5.6, texto, dry_run=True, output="LINES")
        alto_caja = 8 + len(lineas) * 5.6
        self.asegurar(alto_caja + 2)
        y = self.get_y()
        self.set_fill_color(*fondo)
        self.set_draw_color(190, 214, 230)
        self.rect(14, y, ancho, alto_caja, "FD")
        self.set_xy(18, y + 3)
        self.set_text_color(*TEXTO)
        self.multi_cell(ancho - 8, 5.6, texto)
        self.set_y(y + alto_caja + 3)

    def codigo(self, texto):
        self.set_font("Consolas", "", 9.5)
        ancho = 182
        lineas = texto.split("\n")
        alto = 8 + len(lineas) * 5
        self.asegurar(alto + 2)
        y = self.get_y()
        self.set_fill_color(232, 242, 248)
        self.rect(14, y, ancho, alto, "F")
        self.set_xy(18, y + 3)
        self.set_text_color(11, 42, 74)
        for linea in lineas:
            self.cell(0, 5, linea)
            self.ln(5)
            self.set_x(18)
        self.set_y(y + alto + 3)

    def tabla(self, encabezados, filas, anchos):
        alto_fila = 7
        self.asegurar(alto_fila * (len(filas) + 2))
        self.set_font("Arial", "B", 9)
        self.set_fill_color(*AZUL)
        self.set_text_color(255, 255, 255)
        for texto, ancho in zip(encabezados, anchos):
            self.cell(ancho, alto_fila, texto, border=0, fill=True)
        self.ln()
        self.set_font("Arial", "", 9)
        self.set_text_color(*TEXTO)
        for i, fila in enumerate(filas):
            self.set_fill_color(255, 255, 255) if i % 2 else self.set_fill_color(236, 246, 252)
            for texto, ancho in zip(fila, anchos):
                self.cell(ancho, alto_fila, texto, border=0, fill=True)
            self.ln()
        self.ln(3)


def construir():
    pdf = Guia(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(14, 22, 14)
    pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
    pdf.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf")
    pdf.add_font("Arial", "I", r"C:\Windows\Fonts\ariali.ttf")
    pdf.add_font("Consolas", "", r"C:\Windows\Fonts\consola.ttf")

    pdf.add_page()
    pdf.set_fill_color(*AZUL)
    pdf.rect(0, 0, 210, 78, "F")
    pdf.set_fill_color(*CIAN)
    pdf.rect(0, 78, 210, 3, "F")
    pdf.set_xy(14, 22)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(182, 231, 248)
    pdf.cell(0, 7, "TALLER DE PYTHON  ·  FLASK Y MYSQL")
    pdf.set_xy(14, 34)
    pdf.set_font("Arial", "B", 26)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(180, 12, "Portal TechAndes")
    pdf.set_font("Arial", "", 13)
    pdf.set_text_color(214, 236, 248)
    pdf.set_x(14)
    pdf.multi_cell(170, 7, "Guía corta para ponerlo a funcionar\ny para explicarlo en clase.")
    pdf.set_y(92)

    pdf.titulo("El paso que sigue")
    pdf.parrafo(
        "El programa ya está escrito. Python, el entorno virtual y las librerías también. "
        "Lo que falta es conectar el portal con MySQL. Hoy el usuario techandes_api todavía "
        "no existe: al intentar entrar, MySQL responde «Access denied»."
    )
    pdf.subtitulo("Haz esto en orden")
    pasos = [
        "Abre MySQL Workbench con la conexión «Local instance MySQL80» (usuario root).",
        "Comprueba que la base techandes tenga datos. En una pestaña SQL ejecuta: SELECT COUNT(*) FROM empleados; Si el resultado es 0, primero importa el script completo de la clase (el de los registros). El archivo «Base de datos_ clase (1).sql» solo crea tablas vacías.",
        "Abre y ejecuta el archivo sql/02_permisos.sql. Crea el usuario techandes_api con clave TechAndes2026* y le da permiso de consultar y modificar la base.",
        "Abre y ejecuta sql/01_usuarios.sql. Crea la tabla usuarios y las 8 cuentas de prueba, ligadas a los empleados 1 a 8. Si esos empleados no existen, el INSERT falla.",
        "En PowerShell, entra a la carpeta del proyecto, activa el entorno y arranca el portal.",
        "En el navegador abre http://127.0.0.1:5000 e inicia sesión.",
    ]
    for i, paso in enumerate(pasos, 1):
        pdf.asegurar(16)
        y = pdf.get_y()
        pdf.set_fill_color(*AZUL_MED)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 11)
        pdf.rect(14, y, 8, 8, "F")
        pdf.set_xy(14, y + 1.2)
        pdf.cell(8, 6, str(i), align="C")
        pdf.set_xy(25, y)
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(*TEXTO)
        pdf.multi_cell(171, 6, paso)
        pdf.ln(2)

    pdf.subtitulo("Comandos para arrancar")
    pdf.codigo(
        "cd C:\\Users\\orlan\\techandes-portal\n"
        ".venv\\Scripts\\activate\n"
        "python app.py"
    )
    pdf.parrafo(
        "La terminal debe decir Running on http://127.0.0.1:5000. "
        "Para detener el servidor: Ctrl + C. Si el puerto 5000 está ocupado, cierra la otra terminal."
    )

    pdf.add_page()
    pdf.titulo("Con qué usuario entrar")
    pdf.parrafo(
        "La contraseña no se guarda en texto. En la tabla queda un hash scrypt: Flask lo vuelve "
        "a calcular y lo compara. Del hash no se puede recuperar la clave. En este script, "
        "los tres ADMIN comparten el hash de Admin2026* y los cinco vendedores el de Ventas2026*."
    )
    pdf.tabla(
        ["Usuario", "Rol", "Contraseña", "Para qué mostrarlo"],
        [
            ["mprieto", "ADMIN", "Admin2026*", "Gerente: ve Informes y edita productos"],
            ["hbustos", "ADMIN", "Admin2026*", "Supervisor de ventas"],
            ["crobayo", "ADMIN", "Admin2026*", "Supervisor de ventas"],
            ["klozada", "VENDEDOR", "Ventas2026*", "Asesor: Kevin Lozada"],
            ["ytafur", "VENDEDOR", "Ventas2026*", "Asesor comercial"],
            ["boviedo", "VENDEDOR", "Ventas2026*", "Asesor comercial"],
            ["lmurcia", "VENDEDOR", "Ventas2026*", "Asesor comercial"],
            ["fcuellar", "VENDEDOR", "Ventas2026*", "Asesor comercial"],
        ],
        [32, 28, 38, 84],
    )
    pdf.caja(
        "Orden útil en la sustentación: primero klozada (vendedor) y después mprieto (admin). "
        "Así se ve que el menú Informes y los botones Editar / Eliminar aparecen solo para el administrador.",
        FONDO,
    )

    pdf.titulo("Cómo contarlo en un minuto")
    pdf.parrafo(
        "TechAndes es el portal interno de ventas. Un empleado entra con su usuario, "
        "el sistema sabe si es vendedor o administrador, y desde ahí consulta el catálogo, "
        "registra clientes, hace pedidos y, si es admin, mira informes. "
        "Todo el HTML lo arma el servidor: no hay JavaScript de la aplicación."
    )
    pdf.parrafo("La frase que ordena el proyecto es esta:")
    pdf.caja(
        "El navegador pide una ruta. Flask busca la función de esa ruta. "
        "La función consulta MySQL con db.py. Jinja2 mete los resultados en una plantilla HTML. "
        "La plantilla hereda el banner, la bienvenida y el menú de base.html.",
        VERDE,
    )

    pdf.asegurar(78)
    pdf.titulo("De qué archivo hablar")
    pdf.tabla(
        ["Archivo", "Qué decir"],
        [
            ["app.py", "Crea la aplicación, registra los módulos y da formato a pesos y fechas."],
            ["db.py", "Abre una conexión por petición y obliga a usar parámetros %s."],
            ["seguridad.py", "login_requerido y rol_requerido protegen las páginas."],
            ["rutas/", "Un archivo por sección del menú: login, inicio, productos, clientes..."],
            ["templates/", "HTML. base.html es el marco; cada página solo llena el contenido."],
            ["static/", "estilos.css y el banner.svg. El diseño vive aquí, no en Python."],
            [".env", "Clave de sesión y datos de MySQL. No se sube a GitHub."],
            ["sql/", "02 crea el usuario de la base. 01 crea la tabla usuarios."],
        ],
        [32, 150],
    )

    pdf.titulo("Recorrido de las pantallas")
    pdf.tabla(
        ["Menú", "Quién entra", "Qué hace"],
        [
            ["Inicio", "Los dos roles", "Totales, mis ventas, últimos pedidos y stock bajo."],
            ["Productos", "Los dos leen", "Búsqueda. Solo ADMIN crea, edita y elimina."],
            ["Clientes", "Los dos", "Busca, registra y abre el historial de compras."],
            ["Nueva venta", "Los dos", "Pedido a nombre de quien está conectado."],
            ["Pedidos", "Los dos", "Cambia el estado. Cancelar devuelve el stock."],
            ["Informes", "Solo ADMIN", "Categorías, ranking, top 5 y clientes sin compras."],
        ],
        [32, 36, 114],
    )
    pdf.parrafo(
        "Ocultar Informes en el menú no basta. Un vendedor puede escribir /informes/ a mano. "
        "La ruta también está decorada con @rol_requerido(\"ADMIN\") y responde 403."
    )

    pdf.titulo("Inicio de sesión, para explicarlo")
    pdf.viñeta("La página /login no usa el marco del portal: todavía no hay un nombre que mostrar.")
    pdf.viñeta("Se busca el usuario en MySQL, unido al empleado, para mostrar nombre y cargo.")
    pdf.viñeta("Si el usuario no existe o la clave no coincide, el mensaje es el mismo. Así no se revela qué cuentas son reales.")
    pdf.viñeta("Si coincide, se limpia la sesión y se guardan id, rol, nombre y cargo. Nunca la contraseña ni el hash.")
    pdf.viñeta("Se actualiza ultimo_acceso y el navegador vuelve a la página que había pedido.")
    pdf.viñeta("«Cerrar sesión» borra la cookie firmada. Si alguien la modifica a mano, Flask la descarta.")
    pdf.espacio(2)
    pdf.caja(
        "HTTP no recuerda al usuario entre una página y otra. La sesión de Flask es una cookie "
        "firmada con SECRET_KEY. Es el equivalente de $_SESSION en el ejemplo del videoclub.",
        FONDO,
    )

    pdf.asegurar(52)
    pdf.titulo("Por qué las consultas usan %s")
    pdf.parrafo(
        "Si se arma el SQL pegando lo que escribió el usuario, alguien puede cambiar la consulta. "
        "PyMySQL recibe el SQL y los valores por separado. El marcador es %s, y una tupla de un solo "
        "valor lleva coma: (usuario,)."
    )
    pdf.codigo(
        "consultar(\"SELECT * FROM usuarios WHERE usuario = %s\", (usuario,), uno=True)"
    )

    pdf.titulo("La venta: todo o nada")
    pdf.parrafo(
        "Registrar un pedido toca tres tablas: pedidos, detalle_pedido y productos. "
        "Si el stock no alcanza en la segunda línea, no debe quedar un pedido a medias "
        "ni un descuento del primer producto. Por eso ventas.py abre una transacción."
    )
    pdf.viñeta("begin() empieza la transacción aunque la conexión tenga autocommit.")
    pdf.viñeta("Se inserta el pedido en estado Pendiente, a nombre del empleado de la sesión.")
    pdf.viñeta("Cada producto se lee con FOR UPDATE: si dos asesores venden la última unidad, el segundo espera.")
    pdf.viñeta("El precio sale de la base en ese momento. El formulario solo envía el id y la cantidad.")
    pdf.viñeta("Si el mismo producto está en dos filas, las cantidades se suman. La llave de detalle_pedido no permite repetirlo.")
    pdf.viñeta("Si todo sale bien, commit(). Si hay un error de negocio o de MySQL, rollback() deshace todo.")
    pdf.espacio(2)
    pdf.caja(
        "Prueba que lo deja claro: vende 1 memoria que sí hay y 50 portátiles que no hay. "
        "El mensaje dice «Stock insuficiente» y en Workbench no aparece el pedido ni baja el stock de la memoria.",
        AMBAR,
    )

    pdf.titulo("Cancelar un pedido")
    pdf.parrafo(
        "Cambiar el estado también va en una transacción. El estado actual se lee con FOR UPDATE "
        "para que dos personas no devuelvan el inventario dos veces."
    )
    pdf.viñeta("Si el estado nuevo es el mismo, se avisa y no se escribe nada.")
    pdf.viñeta("Un pedido Cancelado ya no se puede pasar a Enviado ni a Entregado.")
    pdf.viñeta("Al cancelar, cada línea suma de nuevo su cantidad al stock y después se guarda el estado.")
    pdf.espacio(1)
    pdf.parrafo(
        "Los estados de esta base son Pendiente, Enviado, Entregado y Cancelado. "
        "Los métodos de pago son Efectivo, Tarjeta, Transferencia y PSE. "
        "Van en ese formato porque así está el CHECK de la tabla pedidos del script de la clase."
    )

    pdf.titulo("Productos y el error 1451")
    pdf.parrafo(
        "Cualquier empleado consulta el catálogo. Crear, editar y eliminar exigen rol ADMIN. "
        "Eliminar va en un formulario POST, no en un enlace: un enlace es un GET y un navegador "
        "podría abrirlo solo."
    )
    pdf.parrafo(
        "Si el producto ya está en un detalle de pedido, MySQL responde 1451 (la llave foránea "
        "impide borrarlo). El portal lo traduce: no se elimina; se desmarca Activo para retirarlo del catálogo. "
        "El ejemplo de clase es el mouse Logitech."
    )
    pdf.parrafo(
        "El formulario se valida en Python aunque el HTML tenga required. Esas reglas del navegador "
        "se pueden saltar. La base, con sus CHECK, es la última línea."
    )

    pdf.titulo("Informes, solo el administrador")
    pdf.viñeta("Ventas por categoría: el porcentaje se calcula en Python y la barra es un div con ese ancho. No hay librería de gráficas.")
    pdf.viñeta("Ranking de vendedores: RANK() OVER ordena por el total vendido, sin pedidos cancelados.")
    pdf.viñeta("Top 5: los productos con más unidades.")
    pdf.viñeta("Clientes sin compras: NOT EXISTS, clientes que no tienen ninguna fila en pedidos.")
    pdf.espacio(2)
    pdf.parrafo(
        "Con los 200 registros originales del taller, Inicio debe mostrar cerca de $ 66.538.300 en ventas efectivas, "
        "2 pedidos pendientes, 40 clientes y 8 productos con stock bajo. "
        "Esas cifras solo aparecen si se importó esa base completa. Con las tablas vacías, los indicadores quedan en cero."
    )

    pdf.titulo("Guion corto para la sustentación")
    pdf.tabla(
        ["#", "Quién", "Qué hacer", "Qué debe verse"],
        [
            ["1", "Nadie", "Abrir /productos/", "Pide iniciar sesión"],
            ["2", "klozada", "Clave mal escrita", "Usuario o contraseña incorrectos"],
            ["3", "klozada", "Ventas2026*", "Entra y no ve Informes"],
            ["4", "klozada", "Escribir /informes/", "Error 403"],
            ["5", "klozada", "Registrar una venta", "Pedido nuevo y stock menor"],
            ["6", "klozada", "Vender de más", "Stock insuficiente; no se crea pedido"],
            ["7", "klozada", "Cancelar el pedido", "El stock vuelve"],
            ["8", "klozada", "Cerrar sesión", "Al recargar pide login otra vez"],
            ["9", "mprieto", "Admin2026*", "Ve Informes y puede crear un producto"],
            ["10", "mprieto", "Borrar un producto vendido", "Mensaje del error 1451"],
        ],
        [10, 24, 52, 96],
    )

    pdf.titulo("Si algo falla")
    pdf.tabla(
        ["Lo que aparece", "Qué revisar"],
        [
            ["Access denied techandes_api", "Ejecutar sql/02_permisos.sql como root."],
            ["Table usuarios doesn't exist", "Ejecutar sql/01_usuarios.sql."],
            ["Cannot add or update a child row", "No hay empleados 1 a 8. Importa los datos de la clase."],
            ["Usuario o contraseña incorrectos", "ADMIN usa Admin2026* y VENDEDOR usa Ventas2026*."],
            ["Can't connect", "El servicio MySQL80 debe estar en ejecución."],
            ["Address already in use", "Ya hay un python app.py abierto. Ciérralo."],
        ],
        [68, 114],
    )
    pdf.caja(
        "Detalle del esquema: el PDF del taller escribe empleados.nombres y estados en mayúscula "
        "(PENDIENTE, CANCELADO). El script de esta carpeta usa empleados.nombre y estados "
        "Pendiente, Enviado, Entregado y Cancelado. El portal sigue el script de la carpeta. "
        "Si en Workbench la columna se llama nombres, hay que decirlo antes de sustentar: las consultas no coincidirían.",
        AMBAR,
    )

    pdf.titulo("Qué no subir a GitHub")
    pdf.parrafo(
        "La carpeta .venv y el archivo .env se quedan en el computador. "
        "En el repositorio van el código, requirements.txt, .env.example y los scripts de sql/. "
        ".env.example solo enseña los nombres de las variables. "
        "En este taller, la clave de techandes_api es la que trae la guía de clase."
    )
    pdf.titulo("Cómo cerrar la explicación")
    pdf.parrafo("Si te piden el cierre en tres frases, puedes decir:")
    pdf.viñeta("El portal identifica al empleado, no solo un usuario suelto: cada cuenta es un empleado.")
    pdf.viñeta("Vender y cancelar no son dos consultas sueltas: o se guarda todo, o no se guarda nada.")
    pdf.viñeta("El menú esconde Informes, y la ruta también lo prohíbe. Las dos cosas hacen falta.")

    pdf.output(SALIDA)


if __name__ == "__main__":
    construir()
    print(SALIDA)
