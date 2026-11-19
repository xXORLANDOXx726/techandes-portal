import re

import pymysql
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from db import consultar, ejecutar, mensaje_error
from seguridad import login_requerido

bp = Blueprint("clientes", __name__, url_prefix="/clientes")

CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CIUDADES_BASE = (
    "Armenia",
    "Barranquilla",
    "Bogotá",
    "Bucaramanga",
    "Cali",
    "Cartagena",
    "Cúcuta",
    "Ibagué",
    "Manizales",
    "Medellín",
    "Neiva",
    "Pasto",
    "Pereira",
    "Santa Marta",
    "Villavicencio",
)


def ciudades():
    filas = consultar("SELECT DISTINCT ciudad FROM clientes ORDER BY ciudad")
    encontradas = [fila["ciudad"] for fila in filas if fila["ciudad"]]
    return sorted(set(CIUDADES_BASE).union(encontradas), key=str.casefold)


def leer_formulario(opciones):
    datos = {
        "documento": request.form.get("documento", "").strip(),
        "nombre": request.form.get("nombre", "").strip(),
        "apellidos": request.form.get("apellidos", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "telefono": request.form.get("telefono", "").strip(),
        "ciudad": request.form.get("ciudad", "").strip(),
    }
    errores = []
    if not datos["documento"].isdigit() or len(datos["documento"]) > 15:
        errores.append("El documento debe ser numérico y tener máximo 15 dígitos.")
    if not datos["nombre"] or len(datos["nombre"]) > 60:
        errores.append("El nombre es obligatorio y no puede superar 60 caracteres.")
    if not datos["apellidos"] or len(datos["apellidos"]) > 60:
        errores.append("Los apellidos son obligatorios y no pueden superar 60 caracteres.")
    if not CORREO.fullmatch(datos["email"]) or len(datos["email"]) > 100:
        errores.append("Escriba un correo válido.")
    if datos["telefono"] and (len(datos["telefono"]) > 15 or not datos["telefono"].isdigit()):
        errores.append("El teléfono debe ser numérico y tener máximo 15 dígitos.")
    if datos["ciudad"] not in opciones:
        errores.append("Seleccione una ciudad de la lista.")
    return datos, errores


@bp.route("/")
@login_requerido
def lista():
    buscar = request.args.get("buscar", "").strip()
    ciudad = request.args.get("ciudad", "").strip()
    sql = """SELECT c.id_cliente, c.documento, c.nombres AS nombre, c.apellidos, c.email,
                    c.telefono, c.ciudad, COUNT(p.id_pedido) AS pedidos
             FROM clientes c
             LEFT JOIN pedidos p ON p.id_cliente = c.id_cliente
             WHERE 1 = 1"""
    parametros = []
    if buscar:
        sql += " AND (c.nombres LIKE %s OR c.apellidos LIKE %s OR c.documento LIKE %s)"
        comodin = f"%{buscar}%"
        parametros.extend((comodin, comodin, comodin))
    if ciudad:
        sql += " AND c.ciudad = %s"
        parametros.append(ciudad)
    sql += """ GROUP BY c.id_cliente, c.documento, c.nombres, c.apellidos, c.email,
                        c.telefono, c.ciudad
               ORDER BY c.apellidos, c.nombres"""
    return render_template(
        "clientes/lista.html",
        clientes=consultar(sql, parametros),
        ciudades=ciudades(),
        buscar=buscar,
        ciudad=ciudad,
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():
    opciones = ciudades()
    datos = {
        "documento": "",
        "nombre": "",
        "apellidos": "",
        "email": "",
        "telefono": "",
        "ciudad": "",
    }
    if request.method == "POST":
        datos, errores = leer_formulario(opciones)
        if not errores:
            try:
                _, _filas = ejecutar(
                    """INSERT INTO clientes
                       (documento, nombres, apellidos, email, telefono, ciudad)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (
                        datos["documento"],
                        datos["nombre"],
                        datos["apellidos"],
                        datos["email"],
                        datos["telefono"] or None,
                        datos["ciudad"],
                    ),
                )
                flash(f"Cliente {datos['nombre']} {datos['apellidos']} registrado.", "exito")
                return redirect(url_for("clientes.lista"))
            except pymysql.MySQLError as error:
                if error.args and error.args[0] == 1062:
                    errores.append("Ya existe un cliente con ese documento o correo.")
                else:
                    errores.append(mensaje_error(error))
        for error in errores:
            flash(error, "error")
    return render_template("clientes/formulario.html", datos=datos, ciudades=opciones)


@bp.route("/<int:id_cliente>")
@login_requerido
def detalle(id_cliente):
    cliente = consultar(
    """SELECT id_cliente, documento, nombres AS nombre, apellidos,
              email, telefono, ciudad, fecha_registro
       FROM clientes
       WHERE id_cliente = %s""",
    (id_cliente,),
    uno=True,
)
    if cliente is None:
        abort(404)
    resumen = consultar(
        """SELECT COALESCE(SUM(d.cantidad * d.precio_unitario), 0) AS total
           FROM pedidos p
           JOIN detalle_pedido d ON d.id_pedido = p.id_pedido
           WHERE p.id_cliente = %s AND p.estado <> 'Cancelado'""",
        (id_cliente,),
        uno=True,
    )
    pedidos = consultar(
        """SELECT p.id_pedido, p.fecha_pedido, p.estado,
                  COALESCE(SUM(d.cantidad * d.precio_unitario), 0) AS total
           FROM pedidos p
           LEFT JOIN detalle_pedido d ON d.id_pedido = p.id_pedido
           WHERE p.id_cliente = %s
           GROUP BY p.id_pedido, p.fecha_pedido, p.estado
           ORDER BY p.fecha_pedido DESC""",
        (id_cliente,),
    )
    return render_template(
        "clientes/detalle.html",
        cliente=cliente,
        total=resumen["total"],
        pedidos=pedidos,
    )
