Feature: CategoriaIngreso

  Scenario: GetCategoriaIngreso sin loguearse
    Given Las siguientes cuentas creadas
      | nombre     | cantidad_base | diferencia | ponderacion |
      | CuentaTest | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_base | diferencia |
      | MonederoTest | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Obtengo la categoria_ingreso con id 1
    Then Obtengo el codigo de estado 401

  Scenario: GetCategoriaIngreso correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre     | cantidad_base | diferencia | ponderacion |
      | CuentaTest | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_base | diferencia |
      | MonederoTest | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Obtengo la categoria_ingreso con id 1
    Then Obtengo el codigo de estado 200

  Scenario: GetCategoriaIngreso que no existe
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre     | cantidad_base | diferencia | ponderacion |
      | CuentaTest | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_base | diferencia |
      | MonederoTest | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Obtengo la categoria_ingreso con id -1
    Then Obtengo el codigo de estado 404

  Scenario: ListCategoriaIngreso sin loguearse
    Given Las siguientes cuentas creadas
      | nombre     | cantidad_base | diferencia | ponderacion |
      | CuentaTest | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_base | diferencia |
      | MonederoTest | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Listo las categorias_ingreso
    Then Obtengo el codigo de estado 401

  Scenario: ListCategoriaIngreso de un elemento
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre     | cantidad_base | diferencia | ponderacion |
      | CuentaTest | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_base | diferencia |
      | MonederoTest | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Listo las categorias_ingreso
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto | nombre_cuenta_abono_defecto | nombre_monedero_defecto |
      | Test        | 1                       | 1                   | CuentaTest                  | MonederoTest            |

  Scenario: ListCategoriaIngreso de varios elementos
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre      | cantidad_base | diferencia | ponderacion |
      | CuentaTest1 | 0.0           | 0.0        | 100         |
      | CuentaTest2 | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre        | cantidad_base | diferencia |
      | MonederoTest1 | 0.0           | 0.0        |
      | MonederoTest2 | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
      | B           | 2                       | 2                   |
    When Listo las categorias_ingreso
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto | nombre_cuenta_abono_defecto | nombre_monedero_defecto |
      | A           | 1                       | 1                   | CuentaTest1                 | MonederoTest1           |
      | B           | 2                       | 2                   | CuentaTest2                 | MonederoTest2           |


  Scenario: CreateCategoriaIngreso sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_ingreso
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    Then Obtengo el codigo de estado 401

  Scenario: CreateCategoriaIngreso correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_ingreso
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    Then Obtengo el codigo de estado 201
    When Listo las categorias_ingreso
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |

  Scenario: CreateCategoriaIngreso sin parametro descripcion
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_ingreso
      | id_cuenta_abono_defecto | id_monedero_defecto |
      | 1                       | 1                   |
    Then Obtengo el codigo de estado 400

  Scenario: CreateCategoriaIngreso solo con descripcion
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_ingreso
      | descripcion      |
      | solo-descripcion |
    Then Obtengo el codigo de estado 201
    When Listo las categorias_ingreso
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion      |
      | solo-descripcion |

  Scenario: CreateCategoriaIngreso duplicado
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Creo la siguiente categoria_ingreso
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    Then Obtengo el codigo de estado 409

  Scenario: CreateCategoriaIngreso varios
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    When Creo la siguiente categoria_ingreso
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
    Then Obtengo el codigo de estado 201
    When Creo la siguiente categoria_ingreso
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | B           | 1                       | 1                   |
    Then Obtengo el codigo de estado 201
    When Listo las categorias_ingreso
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
      | B           | 1                       | 1                   |

  Scenario: UpdateCategoriaIngreso sin loguearse
    Given Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Actualizo la categoria_ingreso con id 1
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test1       | 1                       | 1                   |
    Then Obtengo el codigo de estado 401

  Scenario: UpdateCategoriaIngreso correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Listo las categorias_ingreso
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Actualizo la categoria_ingreso con id 1
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test1       | 1                       | 1                   |
    Then Obtengo el codigo de estado 200
    When Listo las categorias_ingreso
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test1       | 1                       | 1                   |

  Scenario: UpdateCategoriaIngreso sin cambiar nada
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    When Actualizo la categoria_ingreso con id 1
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | Test        | 1                       | 1                   |
    Then Obtengo el codigo de estado 200

  Scenario: UpdateCategoriaIngreso con nombre duplicado
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre | cantidad_base | diferencia | ponderacion |
      | Test   | 0.0           | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre | cantidad_base | diferencia |
      | Test   | 0.0           | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
      | B           | 1                       | 1                   |
    When Actualizo la categoria_ingreso con id 2
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | A           | 1                       | 1                   |
    Then Obtengo el codigo de estado 409
