from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.domain.movimientocuentarepository import MovimientoCuentaRepository
from src.finanzas.domain.movimientomonederorepository import MovimientoMonederoRepository
from src.finanzas.domain.operacion import Operacion
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


def update_cantidad_cuentas(cuenta_repository: CuentaRepository,
                            movimiento_cuenta_repository: MovimientoCuentaRepository,
                            params: dict):
    if params["id_cuenta_abono"] is not None:
        cuenta = cuenta_repository.get(params["id_cuenta_abono"])
        cuenta.set_diferencia(cuenta.get_diferencia() + params["cantidad"])
        cuenta_repository.update(cuenta)

        movimiento = {
            "id_operacion": params["id_operacion"],
            "id_cuenta": cuenta.get_id(),
            "cantidad": params["cantidad"]
        }
        movimiento_cuenta_repository.new(movimiento)

    if params["id_cuenta_cargo"] is not None:
        cuenta = cuenta_repository.get(params["id_cuenta_cargo"])
        cuenta.set_diferencia(cuenta.get_diferencia() - params["cantidad"])
        cuenta_repository.update(cuenta)

        movimiento = {
            "id_operacion": params["id_operacion"],
            "id_cuenta": cuenta.get_id(),
            "cantidad": -params["cantidad"]  # aquí si mantenemos la parte negativa
        }
        movimiento_cuenta_repository.new(movimiento)

    # Aquí empieza lo chungo.
    """Si es ingreso o gasto e id_cuenta es None, entonces se usa la ponderación, "
     "pero si ambas categorías no son none, entonces es una simple transferencia y no se usa ponderación"""
    if params["id_categoria_ingreso"] is not None and params["id_categoria_gasto"] is not None:
        pass
    else:
        if params["id_cuenta_abono"] is None and params["id_categoria_ingreso"] is not None:
            do_ponderacion(cuenta_repository, movimiento_cuenta_repository, params, True)
        if params["id_cuenta_cargo"] is None and params["id_categoria_gasto"] is not None:
            do_ponderacion(cuenta_repository, movimiento_cuenta_repository, params, False)


def update_cantidad_monederos(monedero_repository: MonederoRepository,
                              movimiento_monedero_repository: MovimientoMonederoRepository, params: dict):
    if params["id_monedero_abono"] is not None:
        monedero = monedero_repository.get(params["id_monedero_abono"])
        monedero.set_diferencia(monedero.get_diferencia() + params["cantidad"])
        monedero_repository.update(monedero)
        movimiento = {
            "id_operacion": params["id_operacion"],
            "id_monedero": monedero.get_id(),
            "cantidad": params["cantidad"]
        }
        movimiento_monedero_repository.new(movimiento)
    if params["id_monedero_cargo"] is not None:
        monedero = monedero_repository.get(params["id_monedero_cargo"])
        monedero.set_diferencia(monedero.get_diferencia() - params["cantidad"])
        monedero_repository.update(monedero)
        movimiento = {
            "id_operacion": params["id_operacion"],
            "id_monedero": monedero.get_id(),
            "cantidad": -params["cantidad"]  # aquí si mantenemos la parte negativa
        }
        movimiento_monedero_repository.new(movimiento)


def do_ponderacion(cuenta_repository: CuentaRepository,
                   movimiento_cuenta_repository: MovimientoCuentaRepository,
                   params: dict, add: bool):
    ponderacion_positiva = SimpleFilter("ponderacion", WhereOperator.GREATER, 0.0)
    list_cuentas = cuenta_repository.list(Criteria(filter=ponderacion_positiva))
    # hacemos un check previo para cercinarnos que la suma es 100 y no hay problemas
    sum_ponderacion = 0
    for cuenta in list_cuentas:
        sum_ponderacion += cuenta.get_ponderacion()
    if sum_ponderacion != 100:
        raise InvalidParamError(
            "No se puede llevar a cabo esta acción porque la ponderación de las cuentas no es 100, es: {}. "
            "Por favor, corrige esto para que los cálculos queden correctos".format(sum_ponderacion))
    for cuenta in list_cuentas:
        cantidad_ponderada = params["cantidad"] * (cuenta.get_ponderacion() / 100)
        if add:
            cuenta.set_diferencia(cuenta.get_diferencia() + cantidad_ponderada)
        else:
            cuenta.set_diferencia(cuenta.get_diferencia() - cantidad_ponderada)
        cuenta_repository.update(cuenta)

        movimiento = {
            "id_operacion": params["id_operacion"],
            "id_cuenta": cuenta.get_id(),
            "cantidad": cantidad_ponderada if add else -cantidad_ponderada
        }
        movimiento_cuenta_repository.new(movimiento)


def revert_cantidad_cuentas(cuenta_repository: CuentaRepository,
                            movimiento_cuenta_repository: MovimientoCuentaRepository, operacion_original: Operacion):
    lista_movimientos = movimiento_cuenta_repository.get_by_id_operacion(operacion_original.get_id())
    for movimiento in lista_movimientos:
        cuenta = cuenta_repository.get(movimiento.get_id_cuenta())
        cuenta.set_diferencia(
            cuenta.get_diferencia() - movimiento.get_cantidad())  # al estar el movimeinto con +/- entonces solo hay que hace la resta.
        cuenta_repository.update(cuenta)
        movimiento_cuenta_repository.delete(movimiento.get_id())


def revert_cantidad_monederos(monedero_repository: MonederoRepository,
                              movimiento_monedero_repository: MovimientoMonederoRepository,
                              operacion_original: Operacion):
    lista_movimientos = movimiento_monedero_repository.get_by_id_operacion(operacion_original.get_id())
    for movimiento in lista_movimientos:
        monedero = monedero_repository.get(movimiento.get_id_monedero())
        monedero.set_diferencia(
            monedero.get_diferencia() - movimiento.get_cantidad())  # al estar el movimeinto con +/- entonces solo hay que hace la resta.
        monedero_repository.update(monedero)
        movimiento_monedero_repository.delete(movimiento.get_id())


def validate_params(params: dict):
    if "descripcion" not in params or params["descripcion"] is None:
        raise InvalidParamError("campo descripcion obligatorio")

    if "fecha" not in params or params["fecha"] is None:
        raise InvalidParamError("campo fecha obligatorio")

    if "cantidad" not in params or params["cantidad"] is None:
        raise InvalidParamError("campo cantidad obligatorio")
    elif params["cantidad"] <= 0:
        raise InvalidParamError(
            "Cantidad debe ser un número positivo (>0) (ya se ocupará la categoría de sumar o restar")

    if ("id_categoria_gasto" not in params or params["id_categoria_gasto"] is None) \
            and ("id_categoria_ingreso" not in params or params["id_categoria_ingreso"] is None):
        raise InvalidParamError("campo id_categoria_gasto o id_categoria_ingreso obligatorio (o ambos)")
