Feature: Login

  Scenario: Login correcto
    Given Los siguientes usuarios creados
      | name  | password                                                                                                                         |
      | admin | addd55c9db8c0d868e7a826df9c58c364dda0bbd25e151f9acfaf993e73c5fb1276d119d3a11c2931aeb72fc3131a71c61edfa291cf261347e8377108fa61c22 |
    When Me logueo como el usuario admin y contraseña test
    Then Obtengo el token
    And Obtengo el codigo de estado 200

  Scenario: Login incorrecto
    Given Los siguientes usuarios creados
      | name  | password                                                                                                                         |
      | admin | addd55c9db8c0d868e7a826df9c58c364dda0bbd25e151f9acfaf993e73c5fb1276d119d3a11c2931aeb72fc3131a71c61edfa291cf261347e8377108fa61c22 |
    When Me logueo como el usuario admin y contraseña invalid
    Then Obtengo el codigo de estado 401

  Scenario: Login usuario no existente
    Given Los siguientes usuarios creados
      | name  | password                                                                                                                         |
      | admin | addd55c9db8c0d868e7a826df9c58c364dda0bbd25e151f9acfaf993e73c5fb1276d119d3a11c2931aeb72fc3131a71c61edfa291cf261347e8377108fa61c22 |
    When Me logueo como el usuario noexistente y contraseña test
    Then Obtengo el codigo de estado 401