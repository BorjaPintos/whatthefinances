from datetime import date
from tests.pytest.shared.environmentpytest import *
import unittest

from src.finanzas.inversion.posiciones.domain.posicion import Posicion


class PosicionTest(unittest.TestCase):

    def test_es_cerrable_default_true(self):
        p = Posicion({"id": 1, "abierta": True})
        self.assertEqual(p.is_es_cerrable(), True)

    def test_es_cerrable_set_get(self):
        p = Posicion({"id": 1, "abierta": True})
        p.set_es_cerrable(False)
        self.assertEqual(p.is_es_cerrable(), False)
        p.set_es_cerrable(True)
        self.assertEqual(p.is_es_cerrable(), True)

    def test_dto_includes_es_cerrable(self):
        p = Posicion({
            "id": 1,
            "isin": "ES0000000001",
            "abierta": True,
            "fecha_compra": date(2024, 1, 15),
            "numero_participaciones": 100,
            "precio_compra_sin_comision": 10.0,
            "precio_venta_sin_comision": 0.0,
            "comision_compra": 1.0,
            "otras_comisiones": 0.0,
            "comision_venta": 0.0,
        })
        dto = p.get_dto()
        self.assertIn("es_cerrable", dto)
        self.assertEqual(dto["es_cerrable"], True)

    def test_dto_es_cerrable_reflects_value(self):
        p = Posicion({
            "id": 1,
            "isin": "ES0000000001",
            "abierta": True,
            "fecha_compra": date(2024, 1, 15),
            "numero_participaciones": 100,
            "precio_compra_sin_comision": 10.0,
            "precio_venta_sin_comision": 0.0,
            "comision_compra": 1.0,
            "otras_comisiones": 0.0,
            "comision_venta": 0.0,
        })
        p.set_es_cerrable(False)
        dto = p.get_dto()
        self.assertEqual(dto["es_cerrable"], False)

    def test_dto_abierta_field(self):
        p = Posicion({
            "id": 1,
            "abierta": True,
            "fecha_compra": date(2024, 1, 15),
            "numero_participaciones": 10,
            "precio_compra_sin_comision": 5.0,
            "precio_venta_sin_comision": 0.0,
            "comision_compra": 0.0,
            "otras_comisiones": 0.0,
            "comision_venta": 0.0,
        })
        dto = p.get_dto()
        self.assertEqual(dto["abierta"], True)
        p.set_abierta(False)
        dto = p.get_dto()
        self.assertEqual(dto["abierta"], False)
