Feature: Cuenta

  Scenario: GetCuenta sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |
    When Obtengo la cuenta con id 1
    Then Obtengo el codigo de estado 401

  Scenario: GetCuenta correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |
    When Obtengo la cuenta con id 1
    Then Obtengo el codigo de estado 200

  Scenario: GetCuenta que no existe
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |
    When Obtengo la cuenta con id -1
    Then Obtengo el codigo de estado 404

  Scenario: ListCuenta sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |
    When Listo las cuentas
    Then Obtengo el codigo de estado 401

  Scenario: ListCuenta de un elemento
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 10.0             | 1.0        | 100         |
    When Listo las cuentas
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | ponderacion | total |
      | Test   | 10.0             | 1.0        | 100         | 11.0  |

  Scenario: ListCuenta de varios elementos
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | A      | 0.0              | 0.0        | 50          |
      | B      | 1.0              | 2.0        | 50          |
    When Listo las cuentas
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | total |
      | A      | 0.0              | 0.0        | 0.0   |
      | B      | 1.0              | 2.0        | 3.0   |


  Scenario: CreateCuenta sin loguearse
    When Creo la siguiente cuenta
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |
    Then Obtengo el codigo de estado 401

  Scenario: CreateCuenta correcto
    Given Una sesion correcta
    When Creo la siguiente cuenta
      | nombre | cantidad_inicial | ponderacion |
      | Test   | 0.0              | 100         |
    Then Obtengo el codigo de estado 201
    When Listo las cuentas
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | ponderacion | total |
      | Test   | 0.0              | 0.0        | 100         | 0.0   |

  Scenario: CreateCuenta sin parametro nombre
    Given Una sesion correcta
    When Creo la siguiente cuenta
      | cantidad_inicial | ponderacion |
      | 0.0              | 100         |
    Then Obtengo el codigo de estado 400

  Scenario: CreateCuenta duplicado
    Given Una sesion correcta
    Given Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |
    When Creo la siguiente cuenta
      | nombre | cantidad_inicial | ponderacion |
      | Test   | 0.0              | 100         |
    Then Obtengo el codigo de estado 409

  Scenario: CreateCuenta varios
    Given Una sesion correcta
    When Creo la siguiente cuenta
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | A      | 0.0              | 0.0        | 50          |
    Then Obtengo el codigo de estado 201
    When Creo la siguiente cuenta
      | nombre | cantidad_inicial | ponderacion |
      | B      | 1.0              | 50          |
    Then Obtengo el codigo de estado 201
    When Listo las cuentas
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | ponderacion | total |
      | A      | 0.0              | 0.0        | 50          | 0.0   |
      | B      | 1.0              | 0.0        | 50          | 1.0   |

  Scenario: UpdateCuenta sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |
    When Actualizo la cuenta con id 1
      | nombre | cantidad_inicial | ponderacion |
      | Test   | 0.0              | 100         |
    Then Obtengo el codigo de estado 401

  Scenario: UpdateCuenta correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |
    When Listo las cuentas
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | ponderacion | total |
      | Test   | 0.0              | 0.0        | 100         | 0.0   |
    When Actualizo la cuenta con id 1
      | nombre | cantidad_inicial | ponderacion |
      | Test1  | 1.0              | 100         |
    Then Obtengo el codigo de estado 200
    When Listo las cuentas
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | ponderacion | total |
      | Test1  | 1.0              | 0.0        | 100         | 1.0   |

  Scenario: UpdateCuenta sin tocar nada
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |
    When Actualizo la cuenta con id 1
      | nombre | cantidad_inicial | ponderacion |
      | Test   | 0.0              | 100         |
    Then Obtengo el codigo de estado 200
    When Listo las cuentas
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0              | 0.0        | 100         |

  Scenario: UpdateCuenta con nombre duplicado
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | A      | 0.0              | 0.0        | 50          |
      | B      | 2.0              | 3.0        | 50          |
    When Listo las cuentas
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre | cantidad_inicial | diferencia | ponderacion | total |
      | A      | 0.0              | 0.0        | 50          | 0.0   |
      | B      | 2.0              | 3.0        | 50          | 5.0   |
    When Actualizo la cuenta con id 2
      | nombre | cantidad_inicial | ponderacion |
      | A      | 2.0              | 50          |
    Then Obtengo el codigo de estado 409
