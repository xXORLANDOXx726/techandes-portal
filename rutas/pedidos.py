from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from db import consultar, obtener_conexion
from seguridad import login_requerido

bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")

ESTADOS = ("Pendiente", "Enviado", "Entregado", "Cancelado")


def cambiar_estado(id_pedido, nuevo):
    conexion = obtener_conexion()
    conexion.begin()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT estado FROM pedidos WHERE id_pedido = %s FOR UPDATE",
                (id_pedido,),
            )
            fila = cursor.fetchone()
            if fila is None:
                conexion.rollback()
                return "no_existe"
            actual = fila["estado"]
            if actual == nuevo:
                conexion.rollback()
                return "igual"
            if actual == "Cancelado":
                conexion.rollback()
                return "cerrado"
            if nuevo == "Cancelado":
                cursor.execute(
                    "SELECT id_producto, cantidad FROM detalle_pedido WHERE id_pedido = %s",
                    (id_pedido,),
                )
                for linea in cursor.fetchall():
                    cursor.execute(
                        "UPDATE productos SET stock = stock + %s WHERE id_producto = %s",
                        (linea["cantidad"], linea["id_producto"]),
                    )
            cursor.execute(
                "UPDATE pedidos SET estado = %s WHERE id_pedido = %s",
                (nuevo, id_pedido),
            )
        conexion.commit()
        return "ok" if nuevo != "Cancelado" else "devuelto"
    except Exception:
        conexion.rollback()
        raise


@bp.route("/")
@login_requerido
def lista():
    estado = request.args.get("estado", "").strip()
    sql = """SELECT p.id_pedido, p.fecha_pedido, p.estado, p.metodo_pago,
                    CONCAT(c.nombres, ' ', c.apellidos) AS cliente,
                    CONCAT(e.nombres, ' ', e.apellidos) AS vendedor,
                    COALESCE(SUM(d.cantidad * d.precio_unitario), 0) AS total
             FROM pedidos p
             JOIN clientes c ON c.id_cliente = p.id_cliente
             JOIN empleados e ON e.id_empleado = p.id_empleado
             LEFT JOIN detalle_pedido d ON d.id_pedido = p.id_pedido
             WHERE 1 = 1"""
    parametros = []
    if estado in ESTADOS:
        sql += " AND p.estado = %s"
        parametros.append(estado)
    else:
        estado = ""
    sql += """ GROUP BY p.id_pedido, p.fecha_pedido, p.estado, p.metodo_pago,
                        c.nombres, c.apellidos, e.nombres, e.apellidos
               ORDER BY p.fecha_pedido DESC"""
    return render_template(
        "pedidos/lista.html",
        pedidos=consultar(sql, parametros),
        estados=ESTADOS,
        estado=estado,
    )


@bp.route("/<int:id_pedido>")
@login_requerido
def detalle(id_pedido):
    pedido = consultar(
        """SELECT p.id_pedido, p.fecha_pedido, p.estado, p.metodo_pago,
                  CONCAT(c.nombres, ' ', c.apellidos) AS cliente, c.documento, c.ciudad,
                  CONCAT(e.nombres, ' ', e.apellidos) AS vendedor
           FROM pedidos p
           JOIN clientes c ON c.id_cliente = p.id_cliente
           JOIN empleados e ON e.id_empleado = p.id_empleado
           WHERE p.id_pedido = %s""",
        (id_pedido,),
        uno=True,
    )
    if pedido is None:
        abort(404)
    lineas = consultar(
        """SELECT d.id_producto, pr.nombre, d.cantidad, d.precio_unitario,
                  d.cantidad * d.precio_unitario AS subtotal
           FROM detalle_pedido d
           JOIN productos pr ON pr.id_producto = d.id_producto
           WHERE d.id_pedido = %s
           ORDER BY pr.nombre""",
        (id_pedido,),
    )
    total = sum(linea["subtotal"] for linea in lineas)
    return render_template(
        "pedidos/detalle.html",
        pedido=pedido,
        lineas=lineas,
        total=total,
        estados=ESTADOS,
    )


@bp.route("/<int:id_pedido>/estado", methods=["POST"])
@login_requerido
def estado(id_pedido):
    nuevo = request.form.get("estado", "")
    if nuevo not in ESTADOS:
        flash("Seleccione un estado válido.", "error")
        return redirect(url_for("pedidos.detalle", id_pedido=id_pedido))

    resultado = cambiar_estado(id_pedido, nuevo)
    if resultado == "no_existe":
        abort(404)
    elif resultado == "igual":
        flash("El pedido ya tiene ese estado.", "aviso")
    elif resultado == "cerrado":
        flash("Un pedido cancelado no se puede modificar.", "error")
    elif resultado == "devuelto":
        flash("Pedido cancelado. Las unidades volvieron al inventario.", "exito")
    else:
        flash(f"El pedido quedó en estado {nuevo}.", "exito")
    return redirect(url_for("pedidos.detalle", id_pedido=id_pedido))
