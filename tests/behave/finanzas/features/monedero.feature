Feature: Monedero

  Scenario: GetMonedero sin loguearse
    Given Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Obtengo el monedero con id 1
    Then Obtengo el codigo de estado 401

  Scenario: GetMonedero correcto
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Obtengo el monedero con id 1
    Then Obtengo el codigo de estado 200

  Scenario: GetMonedero que no existe
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Obtengo el monedero con id -1
    Then Obtengo el codigo de estado 404

  Scenario: ListMonedero correcto
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |