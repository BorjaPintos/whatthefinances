Feature: Cuenta

  Scenario: GetCuenta sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    When Obtengo la cuenta con id 1
    Then Obtengo el codigo de estado 401

  Scenario: GetCuenta correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    When Obtengo la cuenta con id 1
    Then Obtengo el codigo de estado 200

  Scenario: GetCuenta que no existe
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    When Obtengo la cuenta con id -1
    Then Obtengo el codigo de estado 404