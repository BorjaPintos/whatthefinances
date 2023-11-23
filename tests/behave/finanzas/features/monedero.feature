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

  Scenario: ListMonedero sin loguearse
    Given Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Listo los monederos
    Then Obtengo el codigo de estado 401

  Scenario: ListMonedero de un elemento
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |

  Scenario: ListMonedero de varios elementos
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | A      | 0.0           | 0.0        |
      | B      | 1.0           | 2.0        |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_base | diferencia |
      | A      | 0.0           | 0.0        |
      | B      | 1.0           | 2.0        |


  Scenario: CreateMonedero sin loguearse
    When Creo el siguiente monedero
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    Then Obtengo el codigo de estado 401

  Scenario: CreateMonedero correcto
    Given Una sesion correcta
    When Creo el siguiente monedero
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    Then Obtengo el codigo de estado 201
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |

  Scenario: CreateMonedero sin parametro nombre
    Given Una sesion correcta
    When Creo el siguiente monedero
      | cantidad_base | diferencia |
      | 0.0           | 0.0        |
    Then Obtengo el codigo de estado 400

  Scenario: CreateMonedero duplicado
    Given Una sesion correcta
    Given Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo el siguiente monedero
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    Then Obtengo el codigo de estado 409

  Scenario: CreateMonedero varios
    Given Una sesion correcta
    When Creo el siguiente monedero
      | nombre | cantidad_base | diferencia |
      | A      | 0.0           | 0.0        |
    Then Obtengo el codigo de estado 201
    When Creo el siguiente monedero
      | nombre | cantidad_base | diferencia |
      | B      | 1.0           | 2.0        |
    Then Obtengo el codigo de estado 201
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_base | diferencia |
      | A      | 0.0           | 0.0        |
      | B      | 1.0           | 2.0        |

  Scenario: UpdateMonedero sin loguearse
    Given Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Actualizo el monedero con id 1
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    Then Obtengo el codigo de estado 401

  Scenario: UpdateMonedero correcto
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Actualizo el monedero con id 1
      | nombre | cantidad_base | diferencia |
      | Test1  | 0.0           | 0.0        |
    Then Obtengo el codigo de estado 200
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_base | diferencia |
      | Test1  | 0.0           | 0.0        |

  Scenario: UpdateMonedero sin tocar nada
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Actualizo el monedero con id 1
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    Then Obtengo el codigo de estado 200

  Scenario: UpdateMonedero con nombre duplicado
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | A      | 0.0           | 0.0        |
      | B      | 2.0           | 3.0        |
    When Actualizo el monedero con id 2
      | nombre | cantidad_base | diferencia |
      | A      | 2.0           | 3.0        |
    Then Obtengo el codigo de estado 409
