Feature: Monedero

  Scenario: GetMonedero sin loguearse
    Given Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0              | 0.0        |
    When Obtengo el monedero con id 1
    Then Obtengo el codigo de estado 401

  Scenario: GetMonedero correcto
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0              | 0.0        |
    When Obtengo el monedero con id 1
    Then Obtengo el codigo de estado 200

  Scenario: GetMonedero que no existe
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0              | 0.0        |
    When Obtengo el monedero con id -1
    Then Obtengo el codigo de estado 404

  Scenario: ListMonedero sin loguearse
    Given Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0              | 0.0        |
    When Listo los monederos
    Then Obtengo el codigo de estado 401

  Scenario: ListMonedero de un elemento
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 10.0             | 1.0        |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | total |
      | Test   | 10.0             | 1.0        | 11.0  |

  Scenario: ListMonedero de varios elementos
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | A      | 0.0              | 0.0        |
      | B      | 1.0              | 2.0        |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | total |
      | A      | 0.0              | 0.0        | 0.0   |
      | B      | 1.0              | 2.0        | 3.0   |


  Scenario: CreateMonedero sin loguearse
    When Creo el siguiente monedero
      | nombre | cantidad_inicial |
      | Test   | 0.0              |
    Then Obtengo el codigo de estado 401

  Scenario: CreateMonedero correcto
    Given Una sesion correcta
    When Creo el siguiente monedero
      | nombre | cantidad_inicial |
      | Test   | 0.0              |
    Then Obtengo el codigo de estado 201
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | total |
      | Test   | 0.0              | 0.0        | 0.0   |

  Scenario: CreateMonedero sin parametro nombre
    Given Una sesion correcta
    When Creo el siguiente monedero
      | cantidad_inicial | diferencia |
      | 0.0              | 0.0        |
    Then Obtengo el codigo de estado 400

  Scenario: CreateMonedero duplicado
    Given Una sesion correcta
    Given Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0              | 0.0        |
    When Creo el siguiente monedero
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0              | 0.0        |
    Then Obtengo el codigo de estado 409

  Scenario: CreateMonedero varios
    Given Una sesion correcta
    When Creo el siguiente monedero
      | nombre | cantidad_inicial |
      | A      | 0.0              |
    Then Obtengo el codigo de estado 201
    When Creo el siguiente monedero
      | nombre | cantidad_inicial |
      | B      | 1.0              |
    Then Obtengo el codigo de estado 201
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | total |
      | A      | 0.0              | 0.0        | 0.0   |
      | B      | 1.0              | 0.0        | 1.0   |

  Scenario: UpdateMonedero sin loguearse
    Given Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0              | 0.0        |
    When Actualizo el monedero con id 1
      | nombre | cantidad_inicial |
      | Test   | 0.0              |
    Then Obtengo el codigo de estado 401

  Scenario: UpdateMonedero correcto
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0              | 3.0
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | total |
      | Test   | 0.0              | 3.0        | 3.0   |
    When Actualizo el monedero con id 1
      | nombre | cantidad_inicial |
      | Test1  | 1.0              |
    Then Obtengo el codigo de estado 200
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | total |
      | Test1  | 1.0              | 3.0        | 4.0   |

  Scenario: UpdateMonedero sin tocar nada
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0              | 0.0        |
    When Actualizo el monedero con id 1
      | nombre | cantidad_inicial |
      | Test   | 0.0              |
    Then Obtengo el codigo de estado 200

  Scenario: UpdateMonedero con nombre duplicado
    Given Una sesion correcta
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | A      | 0.0              | 0.0        |
      | B      | 2.0              | 3.0        |
    When Actualizo el monedero con id 2
      | nombre | cantidad_inicial |
      | A      | 2.0              |
    Then Obtengo el codigo de estado 409
