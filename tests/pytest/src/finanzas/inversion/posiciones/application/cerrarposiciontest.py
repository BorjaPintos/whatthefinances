from datetime import date
from tests.pytest.shared.environmentpytest import *
import unittest
from unittest.mock import Mock

from src.finanzas.inversion.posiciones.application.cerrarposicion import CerrarPosicion
from src.finanzas.inversion.posiciones.domain.posicion import Posicion
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


def _make_posicion(id=1, isin="ES0000000001", id_broker=1, abierta=True,
                   fecha_compra=date(2024, 1, 15)):
    return Posicion({
        "id": id,
        "isin": isin,
        "id_broker": id_broker,
        "id_bolsa": 1,
        "abierta": abierta,
        "fecha_compra": fecha_compra,
        "numero_participaciones": 100,
        "precio_compra_sin_comision": 10.0,
        "comision_compra": 1.0,
        "otras_comisiones": 0.0,
        "comision_venta": 0.0,
    })


class CerrarPosicionTest(unittest.TestCase):

    def test_cerrar_posicion_broker_ninguno(self):
        posicion = _make_posicion(id_broker=1)
        repo = Mock()
        repo.get = Mock(return_value=posicion)
        repo.update = Mock(return_value=True)
        use_case = CerrarPosicion(posicion_repository=repo)

        result = use_case.execute({
            "id": 1,
            "fecha_venta": date(2024, 6, 1),
            "comision_venta": 2.0,
            "precio_venta_sin_comision" : 10.0
        })

        self.assertIsNotNone(result)
        self.assertEqual(result.is_abierta(), False)
        self.assertEqual(result.get_fecha_venta(), date(2024, 6, 1))
        self.assertEqual(result.get_comision_venta(), 2.0)
        repo.update.assert_called_once_with(posicion)

    def test_cerrar_posicion_broker_antigua(self):
        posicion = _make_posicion(id=2, id_broker=2, fecha_compra=date(2024, 1, 10))
        oldest = _make_posicion(id=2, id_broker=2, fecha_compra=date(2024, 1, 10))
        repo = Mock()
        repo.get = Mock(return_value=posicion)
        repo.get_oldest_open_by_isin_and_broker = Mock(return_value=oldest)
        repo.update = Mock(return_value=True)
        use_case = CerrarPosicion(posicion_repository=repo)

        result = use_case.execute({
            "id": 2,
            "fecha_venta": date(2024, 6, 1),
            "comision_venta": 2.0,
            "precio_venta_sin_comision": 10.0
        })

        self.assertIsNotNone(result)
        self.assertEqual(result.is_abierta(), False)

    def test_cerrar_posicion_broker_no_antigua(self):
        posicion = _make_posicion(id=3, id_broker=2, fecha_compra=date(2024, 3, 10))
        oldest = _make_posicion(id=2, id_broker=2, fecha_compra=date(2024, 1, 10))
        repo = Mock()
        repo.get = Mock(return_value=posicion)
        repo.get_oldest_open_by_isin_and_broker = Mock(return_value=oldest)
        use_case = CerrarPosicion(posicion_repository=repo)

        with self.assertRaises(InvalidParamError) as ctx:
            use_case.execute({
                "id": 3,
                "fecha_venta": date(2024, 6, 1),
                "comision_venta": 2.0,
                "precio_venta_sin_comision": 10.0
            })
        self.assertIn("más antigua", str(ctx.exception))

    def test_cerrar_posicion_ya_cerrada(self):
        posicion = _make_posicion(abierta=False)
        repo = Mock()
        repo.get = Mock(return_value=posicion)
        use_case = CerrarPosicion(posicion_repository=repo)

        with self.assertRaises(InvalidParamError) as ctx:
            use_case.execute({
                "id": 1,
                "fecha_venta": date(2024, 6, 1),
                "comision_venta": 2.0,
                "precio_venta_sin_comision": 10.0
            })
        self.assertIn("ya está cerrada", str(ctx.exception))

    def test_cerrar_posicion_sin_fecha_venta(self):
        repo = Mock()
        use_case = CerrarPosicion(posicion_repository=repo)

        with self.assertRaises(InvalidParamError) as ctx:
            use_case.execute({
                "id": 1,
                "comision_venta": 2.0,
                "precio_venta_sin_comision": 10.0
            })
        self.assertIn("fecha_venta", str(ctx.exception))

    def test_cerrar_posicion_sin_comision_venta(self):
        repo = Mock()
        use_case = CerrarPosicion(posicion_repository=repo)

        with self.assertRaises(InvalidParamError) as ctx:
            use_case.execute({
                "id": 1,
                "fecha_venta": date(2024, 6, 1),
                "precio_venta_sin_comision": 10.0
            })
        self.assertIn("comision_venta", str(ctx.exception))

    def test_cerrar_posicion_sin_precio_venta_sin_comision(self):
        repo = Mock()
        use_case = CerrarPosicion(posicion_repository=repo)

        with self.assertRaises(InvalidParamError) as ctx:
            use_case.execute({
                "id": 1,
                "fecha_venta": date(2024, 6, 1),
                "comision_venta": 2.0,
            })
        self.assertIn("precio_venta_sin_comision", str(ctx.exception))