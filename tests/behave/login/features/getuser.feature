Feature: GetUser

  Scenario: GetUser Sin loguearse
    When Obtengo el usuario con id 1
    Then Obtengo el codigo de estado 401

  Scenario: GetUser correcto
    Given Una sesion correcta
    When Obtengo el usuario con id 1
    Then Obtengo el codigo de estado 200

  Scenario: GetUser de un usuario que no existe
    Given Una sesion correcta
    When Obtengo el usuario con id -1
    Then Obtengo el codigo de estado 404