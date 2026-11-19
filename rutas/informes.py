from flask import Blueprint, render_template

from db import consultar
from seguridad import rol_requerido

bp = Blueprint("informes", __name__, url_prefix="/informes")


@bp.route("/")
@rol_requerido("ADMIN")
def index():
    categorias = consultar(
        """SELECT c.nombre AS categoria,
                  COALESCE(SUM(d.cantidad * d.precio_unitario), 0) AS total
           FROM categorias c
           JOIN productos pr ON pr.id_categoria = c.id_categoria
           JOIN detalle_pedido d ON d.id_producto = pr.id_producto
           JOIN pedidos p ON p.id_pedido = d.id_pedido AND p.estado <> 'Cancelado'
           GROUP BY c.id_categoria, c.nombre
           ORDER BY total DESC"""
    )
    gran_total = sum(float(fila["total"]) for fila in categorias)
    for fila in categorias:
        fila["porcentaje"] = round(float(fila["total"]) / gran_total * 100, 1) if gran_total else 0

    vendedores = consultar(
        """SELECT CONCAT(e.nombres, ' ', e.apellidos) AS vendedor, e.cargo,
                  COUNT(DISTINCT p.id_pedido) AS pedidos,
                  COALESCE(SUM(d.cantidad * d.precio_unitario), 0) AS total,
                  RANK() OVER (
                    ORDER BY COALESCE(SUM(d.cantidad * d.precio_unitario), 0) DESC
                  ) AS puesto
           FROM empleados e
           JOIN pedidos p ON p.id_empleado = e.id_empleado AND p.estado <> 'Cancelado'
           JOIN detalle_pedido d ON d.id_pedido = p.id_pedido
           GROUP BY e.id_empleado, e.nombres, e.apellidos, e.cargo
           ORDER BY total DESC"""
    )
    productos = consultar(
        """SELECT pr.nombre,
                  SUM(d.cantidad) AS unidades,
                  SUM(d.cantidad * d.precio_unitario) AS total
           FROM detalle_pedido d
           JOIN productos pr ON pr.id_producto = d.id_producto
           JOIN pedidos p ON p.id_pedido = d.id_pedido AND p.estado <> 'Cancelado'
           GROUP BY pr.id_producto, pr.nombre
           ORDER BY unidades DESC, total DESC
           LIMIT 5"""
    )
    sin_compras = consultar(
        """SELECT c.id_cliente, c.documento, c.ciudad, c.email,
                  CONCAT(c.nombres, ' ', c.apellidos) AS cliente
           FROM clientes c
           WHERE NOT EXISTS (
             SELECT 1 FROM pedidos p WHERE p.id_cliente = c.id_cliente
           )
           ORDER BY c.apellidos, c.nombres"""
    )
    return render_template(
        "informes/index.html",
        categorias=categorias,
        vendedores=vendedores,
        productos=productos,
        sin_compras=sin_compras,
    )
