from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.domain.operacion import Operacion
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


def update_cantidad_cuentas(cuenta_repository: CuentaRepository, params: dict):
    if params["id_cuenta_abono"]is not None:
        cuenta = cuenta_repository.get(params["id_cuenta_abono"])
        cuenta.set_diferencia(cuenta.get_diferencia() + params["cantidad"])
        cuenta_repository.update(cuenta)
    if params["id_cuenta_cargo"]is not None:
        cuenta = cuenta_repository.get(params["id_cuenta_cargo"])
        cuenta.set_diferencia(cuenta.get_diferencia() - params["cantidad"])
        cuenta_repository.update(cuenta)
    # Aquí empieza lo chungo.
    """Si es ingreso o gasto e id_cuenta es None, entonces se usa la ponderación, "
     "pero si ambas categorías no son none, entonces es una simple transferencia y no se usa ponderación"""
    if params["id_categoria_ingreso"] is not None and params["id_categoria_gasto"] is not None:
        pass
    else:
        if params["id_cuenta_abono"] is None and params["id_categoria_ingreso"] is not None:
            do_ponderacion(cuenta_repository, params["cantidad"], True)
        if params["id_cuenta_cargo"] is None and params["id_categoria_gasto"] is not None:
            do_ponderacion(cuenta_repository, params["cantidad"], False)


def update_cantidad_monederos(monedero_repository: MonederoRepository, params: dict):
    if params["id_monedero_abono"] is not None:
        monedero = monedero_repository.get(params["id_monedero_abono"])
        monedero.set_diferencia(monedero.get_diferencia() + params["cantidad"])
        monedero_repository.update(monedero)
    if params["id_monedero_cargo"]is not None:
        monedero = monedero_repository.get(params["id_monedero_cargo"])
        monedero.set_diferencia(monedero.get_diferencia() - params["cantidad"])
        monedero_repository.update(monedero)


def do_ponderacion(cuenta_repository: CuentaRepository, cantidad: float, add: bool):
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
        cantidad_ponderada = cantidad * (cuenta.get_ponderacion() / 100)
        if add:
            cuenta.set_diferencia(cuenta.get_diferencia() + cantidad_ponderada)
        else:
            cuenta.set_diferencia(cuenta.get_diferencia() - cantidad_ponderada)
        cuenta_repository.update(cuenta)


def revert_cantidad_cuentas(cuenta_repository: CuentaRepository, operacion_original: Operacion):
    if operacion_original.get_id_cuenta_abono() is not None:
        cuenta = cuenta_repository.get(operacion_original.get_id_cuenta_abono())
        cuenta.set_diferencia(cuenta.get_diferencia() - operacion_original.get_cantidad())
        cuenta_repository.update(cuenta)
    if operacion_original.get_id_cuenta_cargo() is not None:
        cuenta = cuenta_repository.get(operacion_original.get_id_cuenta_cargo())
        cuenta.set_diferencia(cuenta.get_diferencia() + operacion_original.get_cantidad())
        cuenta_repository.update(cuenta)
    # Aquí empieza lo chungo.
    """Si es ingreso o gasto e id_cuenta es None, entonces se usa la ponderación, "
     "pero si ambas categorías no son none, entonces es una simple transferencia y no se usa ponderación"""
    if operacion_original.get_id_categoria_ingreso() is not None and operacion_original.get_id_categoria_gasto() is not None:
        pass
    else:
        if operacion_original.get_id_cuenta_abono() is None and operacion_original.get_id_categoria_ingreso() is not None:
            do_ponderacion(cuenta_repository, operacion_original.get_cantidad(), False)
        if operacion_original.get_id_cuenta_cargo() is None and operacion_original.get_id_categoria_gasto() is not None:
            do_ponderacion(cuenta_repository, operacion_original.get_cantidad(), True)


def revert_cantidad_monederos(monedero_repository: MonederoRepository, operacion_original: Operacion):
    if operacion_original.get_id_monedero_abono() is not None:
        monedero = monedero_repository.get(operacion_original.get_id_monedero_abono())
        monedero.set_diferencia(monedero.get_diferencia() - operacion_original.get_cantidad())
        monedero_repository.update(monedero)
    if operacion_original.get_id_monedero_cargo() is not None:
        monedero = monedero_repository.get(operacion_original.get_id_monedero_cargo())
        monedero.set_diferencia(monedero.get_diferencia() + operacion_original.get_cantidad())
        monedero_repository.update(monedero)


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
