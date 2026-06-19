Feature: Posicion

  Scenario: ListPosicion sin loguearse
    Given Los siguientes productos creados
      | nombre | isin         |
      | Apple  | US0378331005 |
    And Los siguientes brokers creados
      | nombre  | extranjero |
      | Ninguno | false      |
    And Las siguientes bolsas creadas
      | nombre |
      | MEV    |
    And Las siguientes posiciones creadas
      | isin         | fecha_compra | numero_participaciones | id_bolsa | id_broker | precio_compra_sin_comision | comision_compra | otras_comisiones | abierta |
      | US0378331005 | 15/01/2024   | 100                    | 1        | 1         | 10.0                       | 1.0             | 0.0              | true    |
    When Listo las posiciones
    Then Obtengo el codigo de estado 401

  Scenario: ListPosicion solo abiertas por defecto
    Given Una sesion correcta
    And Los siguientes productos creados
      | nombre | isin         |
      | Apple  | US0378331001 |
      | Apple2 | US0378331002 |
    And Los siguientes brokers creados
      | nombre  | extranjero |
      | Ninguno | false      |
    And Las siguientes bolsas creadas
      | nombre |
      | MEV    |
    And Las siguientes posiciones creadas
      | isin         | fecha_compra | numero_participaciones | id_bolsa | id_broker | precio_compra_sin_comision | comision_compra | otras_comisiones | abierta |
      | US0378331001 | 2025-01-15   | 100                    | 1        | 1         | 10.0                       | 1.0             | 0.0              | true    |
      | US0378331002 | 2024-03-20   | 50                     | 1        | 1         | 12.0                       | 1.0             | 0.0              | false   |
    When Listo las posiciones
    Then Obtengo el codigo de estado 200
    And Obtengo la siguiente lista paginada
      | isin         |
      | US0378331001 |

  Scenario: ListPosicion muestra cerradas con filtro
    Given Una sesion correcta
    And Los siguientes productos creados
      | nombre | isin         |
      | Apple  | US0378331001 |
      | Apple2 | US0378331002 |
    And Los siguientes brokers creados
      | nombre  | extranjero |
      | Ninguno | false      |
    And Las siguientes bolsas creadas
      | nombre |
      | MEV    |
    And Las siguientes posiciones creadas
      | isin         | fecha_compra | numero_participaciones | id_bolsa | id_broker | precio_compra_sin_comision | comision_compra | otras_comisiones | abierta |
      | US0378331001 | 2025-01-15   | 100                    | 1        | 1         | 10.0                       | 1.0             | 0.0              | true    |
      | US0378331002 | 2024-03-20   | 50                     | 1        | 1         | 12.0                       | 1.0             | 0.0              | false   |
    When Listo las posiciones con filtro abierta false
    Then Obtengo el codigo de estado 200
    And Obtengo la siguiente lista paginada
      | isin         |
      | US0378331001 |
      | US0378331002 |

  Scenario: CerrarPosicion sin loguearse
    Given Los siguientes productos creados
      | nombre | isin         |
      | Apple  | US0378331005 |
    And Los siguientes brokers creados
      | nombre  | extranjero |
      | Ninguno | false      |
    And Las siguientes bolsas creadas
      | nombre |
      | MEV    |
    And Las siguientes posiciones creadas
      | isin         | fecha_compra | numero_participaciones | id_bolsa | id_broker | precio_compra_sin_comision | comision_compra | otras_comisiones | abierta |
      | US0378331005 | 2024-01-15   | 100                    | 1        | 1         | 10.0                       | 1.0             | 0.0              | true    |
    When Cierro la posicion con id 1
      | fecha_venta | comision_venta | precio_venta_sin_comision |
      | 06/01/2026  | 2.0            | 10                        |
    Then Obtengo el codigo de estado 401

  Scenario: CerrarPosicion correcta con broker Ninguno
    Given Una sesion correcta
    And Los siguientes productos creados
      | nombre | isin         |
      | Apple  | US0378331005 |
    And Los siguientes brokers creados
      | nombre  | extranjero |
      | Ninguno | false      |
    And Las siguientes bolsas creadas
      | nombre |
      | MEV    |
    And Las siguientes posiciones creadas
      | isin         | fecha_compra | numero_participaciones | id_bolsa | id_broker | precio_compra_sin_comision | comision_compra | otras_comisiones | abierta |
      | US0378331005 | 2024-01-15   | 100                    | 1        | 1         | 10.0                       | 1.0             | 0.0              | true    |
    When Cierro la posicion con id 1
      | fecha_venta | comision_venta | precio_venta_sin_comision |
      | 06/01/2026  | 2.0            | 10                        |
    Then Obtengo el codigo de estado 200
    When Listo las posiciones con filtro abierta false
    Then Obtengo el codigo de estado 200
    And Obtengo la siguiente lista paginada
      | isin         |
      | US0378331005 |

  Scenario: CerrarPosicion correcta siendo la mas antigua
    Given Una sesion correcta
    And Los siguientes productos creados
      | nombre | isin         |
      | Apple  | US0378331005 |
    And Los siguientes brokers creados
      | nombre  | extranjero |
      | Ninguno | false      |
      | IBKR    | true       |
    And Las siguientes bolsas creadas
      | nombre |
      | MEV    |
    And Las siguientes posiciones creadas
      | isin         | fecha_compra | numero_participaciones | id_bolsa | id_broker | precio_compra_sin_comision | comision_compra | otras_comisiones | abierta |
      | US0378331005 | 2024-01-15   | 100                    | 1        | 2         | 10.0                       | 1.0             | 0.0              | true    |
      | US0378331005 | 2024-03-15   | 50                     | 1        | 2         | 12.0                       | 1.0             | 0.0              | true    |
    When Cierro la posicion con id 1
      | fecha_venta | comision_venta | precio_venta_sin_comision |
      | 06/01/2026  | 2.0            | 10                        |
    Then Obtengo el codigo de estado 200

  Scenario: CerrarPosicion rechazada por no ser la mas antigua
    Given Una sesion correcta
    And Los siguientes productos creados
      | nombre | isin         |
      | Apple  | US0378331005 |
    And Los siguientes brokers creados
      | nombre  | extranjero |
      | Ninguno | false      |
      | IBKR    | true       |
    And Las siguientes bolsas creadas
      | nombre |
      | MEV    |
    And Las siguientes posiciones creadas
      | isin         | fecha_compra | numero_participaciones | id_bolsa | id_broker | precio_compra_sin_comision | comision_compra | otras_comisiones | abierta |
      | US0378331005 | 2024-01-15   | 100                    | 1        | 2         | 10.0                       | 1.0             | 0.0              | true    |
      | US0378331005 | 2024-03-15   | 50                     | 1        | 2         | 12.0                       | 1.0             | 0.0              | true    |
    When Cierro la posicion con id 2
      | fecha_venta | comision_venta | precio_venta_sin_comision |
      | 06/01/2026  | 2.0            | 10                        |
    Then Obtengo el codigo de estado 400

  Scenario: CerrarPosicion sin fecha_venta
    Given Una sesion correcta
    And Los siguientes productos creados
      | nombre | isin         |
      | Apple  | US0378331005 |
    And Los siguientes brokers creados
      | nombre  | extranjero |
      | Ninguno | false      |
      | IBKR    | true       |
    And Las siguientes bolsas creadas
      | nombre |
      | MEV    |
    And Las siguientes posiciones creadas
      | isin         | fecha_compra | numero_participaciones | id_bolsa | id_broker | precio_compra_sin_comision | comision_compra | otras_comisiones | abierta |
      | US0378331005 | 2024-01-15   | 100                    | 1        | 2         | 10.0                       | 1.0             | 0.0              | true    |
    When Cierro la posicion con id 1
      | comision_venta |
      | 2.0            |
    Then Obtengo el codigo de estado 400

  Scenario: DeshacerCerrarPosicion correcto
    Given Una sesion correcta
    And Los siguientes productos creados
      | nombre | isin         |
      | Apple  | US0378331005 |
    And Los siguientes brokers creados
      | nombre  | extranjero |
      | Ninguno | false      |
      | IBKR    | true       |
    And Las siguientes bolsas creadas
      | nombre |
      | MEV    |
    And Las siguientes posiciones creadas
      | isin         | fecha_compra | numero_participaciones | id_bolsa | id_broker | precio_compra_sin_comision | comision_compra | otras_comisiones | abierta |
      | US0378331005 | 2024-01-15   | 100                    | 1        | 2         | 10.0                       | 1.0             | 0.0              | false   |
    When Deshago el cierre de la posicion con id 1
    Then Obtengo el codigo de estado 200
    When Listo las posiciones
    Then Obtengo el codigo de estado 200
    And Obtengo la siguiente lista paginada
      | isin         |
      | US0378331005 |
