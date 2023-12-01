Feature: CategoriaGasto

  Scenario: GetCategoriaGasto sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Obtengo la categoria_gasto con id 1
    Then Obtengo el codigo de estado 401

  Scenario: GetCategoriaGasto correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Obtengo la categoria_gasto con id 1
    Then Obtengo el codigo de estado 200

  Scenario: GetCategoriaGasto que no existe
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Obtengo la categoria_gasto con id -1
    Then Obtengo el codigo de estado 404

  Scenario: ListCategoriaGasto sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Listo las categorias_gasto
    Then Obtengo el codigo de estado 401

  Scenario: ListCategoriaGasto de un elemento
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre     | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_inicial | diferencia |
      | MonederoTest | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Listo las categorias_gasto
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto | nombre_cuenta_cargo_defecto | nombre_monedero_defecto |
      | Test        | 1                       | 1                   | CuentaTest                  | MonederoTest            |

  Scenario: ListCategoriaGasto de varios elementos
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre      | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest1 | 0.0           | 0.0        | 100         |
      | CuentaTest2 | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre        | cantidad_inicial | diferencia |
      | MonederoTest1 | 0.0           | 0.0        |
      | MonederoTest2 | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
      | B           | 2                       | 2                   |
    When Listo las categorias_gasto
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto | nombre_cuenta_cargo_defecto | nombre_monedero_defecto |
      | A           | 1                       | 1                   | CuentaTest1                 | MonederoTest1           |
      | B           | 2                       | 2                   | CuentaTest2                 | MonederoTest2           |


  Scenario: CreateCategoriaGasto sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_gasto
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    Then Obtengo el codigo de estado 401

  Scenario: CreateCategoriaGasto correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_gasto
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    Then Obtengo el codigo de estado 201
    When Listo las categorias_gasto
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |

  Scenario: CreateCategoriaGasto sin parametro descripcion
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_gasto
      | id_cuenta_cargo_defecto | id_monedero_defecto |
      | 1                       | 1                   |
    Then Obtengo el codigo de estado 400


  Scenario: CreateCategoriaGasto solo descripcion
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_gasto
      | descripcion |
      | Test        |
    Then Obtengo el codigo de estado 201
    When Listo las categorias_gasto
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion |
      | Test        |

  Scenario: CreateCategoriaGasto duplicado
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Creo la siguiente categoria_gasto
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    Then Obtengo el codigo de estado 409

  Scenario: CreateCategoriaGasto varios
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_gasto
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
    Then Obtengo el codigo de estado 201
    When Creo la siguiente categoria_gasto
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | B           | 1                       | 1                   |
    Then Obtengo el codigo de estado 201
    When Listo las categorias_gasto
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
      | B           | 1                       | 1                   |

  Scenario: UpdateCategoriaGasto sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Actualizo la categoria_gasto con id 1
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test1       | 1                       | 1                   |
    Then Obtengo el codigo de estado 401

  Scenario: UpdateCategoriaGasto correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Listo las categorias_gasto
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Actualizo la categoria_gasto con id 1
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test1       | 1                       | 1                   |
    Then Obtengo el codigo de estado 200
    When Listo las categorias_gasto
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test1       | 1                       | 1                   |

  Scenario: UpdateCategoriaGasto sin cambiar nada
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Actualizo la categoria_gasto con id 1
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    Then Obtengo el codigo de estado 200

  Scenario: UpdateCategoriaGasto con nombre duplicado
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_inicial | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_inicial | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
      | B           | 1                       | 1                   |
    When Actualizo la categoria_gasto con id 2
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
    Then Obtengo el codigo de estado 409
