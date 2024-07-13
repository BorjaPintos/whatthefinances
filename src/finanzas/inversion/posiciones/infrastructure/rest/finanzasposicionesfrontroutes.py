from src.finanzas.inversion.bolsa.infrastructure.rest import finanzasbolsacontroller
from src.finanzas.inversion.broker.infrastructure.rest import finanzasbrokercontroller
from src.finanzas.inversion.producto.infrastructure.rest import finanzasproductocontroller

from flask import request, render_template
from flask_login import login_required


def import_routes(rootpath, app):

    @app.route(rootpath + "posiciones.html", methods=['GET'])
    @login_required
    def posiciones():
        user = request.user
        lista_brokers, code = finanzasbrokercontroller.list_brokers({})
        lista_bolsas, code = finanzasbolsacontroller.list_bolsas({})
        lista_productos, code = finanzasproductocontroller.list_productos({})
        lista_headers = ["Fecha", "Nombre", "Bolsa", "Broker",
                         "Precio por Participación", "Número de Participaciones",
                         "Total Compra",
                         "Valor actual", "Total Actual", "Ganacia SC", "Ganacia CC",
                         "Dividendos Acumulados", "Ganancia CC y Dividendos"]

        return render_template('/posiciones.html', username=user.get_name(),
                               title="Posiciones",
                               lista_headers=lista_headers,
                               lista_brokers=lista_brokers,
                               lista_bolsas=lista_bolsas,
                               lista_productos=lista_productos
                               )
