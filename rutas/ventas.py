from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from db import consultar, mensaje_error, obtener_conexion
from seguridad import login_requerido

bp = Blueprint("ventas", __name__, url_prefix="/ventas")

METODOS = ("Efectivo", "Tarjeta", "Transferencia", "PSE")
FILAS = 5


class ErrorVenta(Exception):
    """Error de negocio: aborta la transacción con un mensaje claro."""


def catalogo():
    return consultar(
        """SELECT id_producto, nombre, precio, stock
           FROM productos
           WHERE activo = 1
           ORDER BY nombre"""
    )


def clientes_activos():
    return consultar(
        """SELECT id_cliente, documento, CONCAT(nombres, ' ', apellidos) AS nombre
           FROM clientes
           ORDER BY apellidos, nombres"""
    )


def leer_lineas():
    """Suma cantidades si el mismo producto aparece en más de una fila."""
    items = {}
    lineas = []
    errores = []
    for numero in range(1, FILAS + 1):
        id_producto = request.form.get(f"producto_{numero}", "").strip()
        cantidad = request.form.get(f"cantidad_{numero}", "").strip()
        lineas.append({"producto": id_producto, "cantidad": cantidad})
        if not id_producto and not cantidad:
            continue
        if not id_producto.isdigit():
            errores.append(f"Fila {numero}: seleccione un producto.")
            continue
        if not cantidad.isdigit() or int(cantidad) <= 0:
            errores.append(f"Fila {numero}: la cantidad debe ser un entero mayor que 0.")
            continue
        clave = int(id_producto)
        items[clave] = items.get(clave, 0) + int(cantidad)
    if not items and not errores:
        errores.append("Agregue al menos un producto.")
    return items, lineas, errores


def registrar_pedido(id_cliente, metodo_pago, items):
    """Inserta pedido + detalle y descuenta stock. Todo o nada."""
    conexion = obtener_conexion()
    conexion.begin()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """INSERT INTO pedidos (id_cliente, id_empleado, estado, metodo_pago)
                   VALUES (%s, %s, 'Pendiente', %s)""",
                (id_cliente, session["usuario"]["id_empleado"], metodo_pago),
            )
            id_pedido = cursor.lastrowid
            for id_producto, cantidad in items.items():
                cursor.execute(
                    """SELECT nombre, precio, stock, activo
                       FROM productos
                       WHERE id_producto = %s
                       FOR UPDATE""",
                    (id_producto,),
                )
                producto = cursor.fetchone()
                if producto is None or not producto["activo"]:
                    raise ErrorVenta(f"El producto {id_producto} no está disponible.")
                if int(producto["stock"]) < cantidad:
                    raise ErrorVenta(
                        f"Stock insuficiente de {producto['nombre']}: "
                        f"hay {producto['stock']}, se piden {cantidad}."
                    )
                cursor.execute(
                    """INSERT INTO detalle_pedido
                       (id_pedido, id_producto, cantidad, precio_unitario)
                       VALUES (%s, %s, %s, %s)""",
                    (id_pedido, id_producto, cantidad, producto["precio"]),
                )
                cursor.execute(
                    "UPDATE productos SET stock = stock - %s WHERE id_producto = %s",
                    (cantidad, id_producto),
                )
        conexion.commit()
        return id_pedido
    except Exception:
        conexion.rollback()
        raise


@bp.route("/nueva", methods=["GET", "POST"])
@login_requerido
def nueva():
    datos = {"id_cliente": "", "metodo_pago": ""}
    lineas = [{"producto": "", "cantidad": ""} for _ in range(FILAS)]
    if request.method == "POST":
        datos = {
            "id_cliente": request.form.get("id_cliente", "").strip(),
            "metodo_pago": request.form.get("metodo_pago", "").strip(),
        }
        items, lineas, errores = leer_lineas()
        if not datos["id_cliente"].isdigit():
            errores.append("Seleccione un cliente.")
        if datos["metodo_pago"] not in METODOS:
            errores.append("Seleccione un método de pago.")
        if not errores:
            try:
                id_pedido = registrar_pedido(datos["id_cliente"], datos["metodo_pago"], items)
                flash(f"Venta registrada: pedido #{id_pedido}.", "exito")
                return redirect(url_for("pedidos.detalle", id_pedido=id_pedido))
            except ErrorVenta as error:
                errores.append(str(error))
            except Exception as error:
                if getattr(error, "args", None):
                    errores.append(mensaje_error(error))
                else:
                    errores.append("No se pudo registrar la venta.")
        for error in errores:
            flash(error, "error")
    return render_template(
        "ventas/nueva.html",
        datos=datos,
        lineas=lineas,
        clientes=clientes_activos(),
        productos=catalogo(),
        metodos=METODOS,
    )
