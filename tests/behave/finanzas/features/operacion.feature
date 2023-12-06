Feature: Operacion


  Scenario: CreateOperacion sin loguearse
    Given Las siguientes cuentas creadas
      | nombre     | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest | 0.0              | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_inicial | diferencia |
      | MonederoTest | 0.0              | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | GastoTest   | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_cuenta_abono | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 10       | 1               | 1                 | 1                    |
    Then Obtengo el codigo de estado 401

  Scenario: CreateOperacion Ingreso correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre     | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest | 0.0              | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_inicial | diferencia |
      | MonederoTest | 0.0              | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | GastoTest   | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_cuenta_abono | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 10.0     | 1               | 1                 | 1                    |
    Then Obtengo el codigo de estado 201
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | fecha      | descripcion   | cantidad | id_cuenta_abono | id_monedero_abono | id_categoria_ingreso | nombre_cuenta_abono | nombre_monedero_abono | descripcion_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 10.0     | 1               | 1                 | 1                    | CuentaTest          | MonederoTest          | IngresoTest                   |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre     | diferencia | total |
      | CuentaTest | 10.0       | 10.0  |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre       | diferencia | total |
      | MonederoTest | 10.0       | 10.0  |

  Scenario: CreateOperacion Gasto correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre     | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest | 10.0             | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_inicial | diferencia |
      | MonederoTest | 0.0              | 10.0       |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | GastoTest   | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_cuenta_cargo | id_monedero_cargo | id_categoria_gasto |
      | 04/12/2023 | OperacionTest | 5.0      | 1               | 1                 | 1                  |
    Then Obtengo el codigo de estado 201
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | fecha      | descripcion   | cantidad | id_cuenta_cargo | id_monedero_cargo | id_categoria_gasto | nombre_cuenta_cargo | nombre_monedero_cargo | descripcion_categoria_gasto |
      | 04/12/2023 | OperacionTest | 5.0      | 1               | 1                 | 1                  | CuentaTest          | MonederoTest          | GastoTest                   |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre     | diferencia | total |
      | CuentaTest | -5.0       | 5.0   |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre       | diferencia | total |
      | MonederoTest | 5.0        | 5.0   |


  Scenario: CreateOperacion Transferencia correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre     | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest | 10.0             | 0.0        | 100         |
    And Los siguientes monederos creados
      | nombre       | cantidad_inicial | diferencia |
      | MonederoTest | 0.0              | 10.0       |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | GastoTest   | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_cuenta_cargo | id_monedero_cargo | id_categoria_gasto |
      | 04/12/2023 | OperacionTest | 5.0      | 1               | 1                 | 1                  |
    Then Obtengo el codigo de estado 201
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | fecha      | descripcion   | cantidad | id_cuenta_cargo | id_monedero_cargo | id_categoria_gasto | nombre_cuenta_cargo | nombre_monedero_cargo | descripcion_categoria_gasto |
      | 04/12/2023 | OperacionTest | 5.0      | 1               | 1                 | 1                  | CuentaTest          | MonederoTest          | GastoTest                   |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre     | diferencia | total |
      | CuentaTest | -5.0       | 5.0   |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre       | diferencia | total |
      | MonederoTest | 5.0        | 5.0   |

  Scenario: CreateOperacion con Ponderacion correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre      | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest1 | 0.0              | 0.0        | 60          |
      | CuentaTest2 | 0.0              | 0.0        | 40          |
    And Los siguientes monederos creados
      | nombre       | cantidad_inicial | diferencia |
      | MonederoTest | 0.0              | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 1000.0   | 1                 | 1                    |
    Then Obtengo el codigo de estado 201
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso | nombre_cuenta_abono | nombre_monedero_abono | descripcion_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 1000.0   | 1                 | 1                    | None                | MonederoTest          | IngresoTest                   |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre      | diferencia | total |
      | CuentaTest1 | 600.0      | 600.0 |
      | CuentaTest2 | 400.0      | 400.0 |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre       | diferencia | total  |
      | MonederoTest | 1000.0     | 1000.0 |


  Scenario: CreateOperacion con Ponderacion mal
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre      | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest1 | 0.0              | 0.0        | 40          |
      | CuentaTest2 | 0.0              | 0.0        | 40          |
    And Los siguientes monederos creados
      | nombre       | cantidad_inicial | diferencia |
      | MonederoTest | 0.0              | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 1000.0   | 1                 | 1                    |
    Then Obtengo el codigo de estado 400


  Scenario: UpdateOperacion con ponderacion correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre      | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest1 | 0.0              | 0.0        | 60          |
      | CuentaTest2 | 0.0              | 0.0        | 40          |
    And Los siguientes monederos creados
      | nombre       | cantidad_inicial | diferencia |
      | MonederoTest | 0.0              | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 1000.0   | 1                 | 1                    |
    Then Obtengo el codigo de estado 201
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | id | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso | nombre_cuenta_abono | nombre_monedero_abono | descripcion_categoria_ingreso |
      | 1  | 04/12/2023 | OperacionTest | 1000.0   | 1                 | 1                    | None                | MonederoTest          | IngresoTest                   |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre      | diferencia | total |
      | CuentaTest1 | 600.0      | 600.0 |
      | CuentaTest2 | 400.0      | 400.0 |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre       | diferencia | total  |
      | MonederoTest | 1000.0     | 1000.0 |
    When Actualizo la operacion con id 1
      | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 100.0    | 1                 | 1                    |
    Then Obtengo el codigo de estado 200
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | id | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso | nombre_cuenta_abono | nombre_monedero_abono | descripcion_categoria_ingreso |
      | 1  | 04/12/2023 | OperacionTest | 100.0    | 1                 | 1                    | None                | MonederoTest          | IngresoTest                   |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre      | diferencia | total |
      | CuentaTest1 | 60.0       | 60.0  |
      | CuentaTest2 | 40.0       | 40.0  |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre       | diferencia | total |
      | MonederoTest | 100.0      | 100.0 |


  Scenario: UpdateOperacion de cuenta fija a cuentas ponderada y cambio de monedero correcto
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre      | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest1 | 0.0              | 0.0        | 60          |
      | CuentaTest2 | 0.0              | 0.0        | 40          |
    And Los siguientes monederos creados
      | nombre        | cantidad_inicial | diferencia |
      | MonederoTest1 | 0.0              | 0.0        |
      | MonederoTest2 | 0.0              | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_cuenta_abono | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 1000.0   | 1               | 1                 | 1                    |
    Then Obtengo el codigo de estado 201
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | id | fecha      | descripcion   | cantidad | id_monedero_abono | id_monedero_abono | id_categoria_ingreso | nombre_cuenta_abono | nombre_monedero_abono | descripcion_categoria_ingreso |
      | 1  | 04/12/2023 | OperacionTest | 1000.0   | 1                 | 1                 | 1                    | CuentaTest1         | MonederoTest1         | IngresoTest                   |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre      | diferencia | total  |
      | CuentaTest1 | 1000.0     | 1000.0 |
      | CuentaTest2 | 0.0        | 0.0    |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre        | diferencia | total  |
      | MonederoTest1 | 1000.0     | 1000.0 |
      | MonederoTest2 | 0.0        | 0.0    |
    When Actualizo la operacion con id 1
      # id_cuenta_abono = None -> al no ponerlo ya se pone sola
      | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 1000.0   | 2                 | 1                    |
    Then Obtengo el codigo de estado 200
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | id | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso | nombre_cuenta_abono | nombre_monedero_abono | descripcion_categoria_ingreso |
      | 1  | 04/12/2023 | OperacionTest | 1000.0   | 2                 | 1                    | None                | MonederoTest2         | IngresoTest                   |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre      | diferencia | total |
      | CuentaTest1 | 600.0      | 600.0 |
      | CuentaTest2 | 400.0      | 400.0 |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre        | diferencia | total  |
      | MonederoTest1 | 0.0        | 0.0    |
      | MonederoTest2 | 1000.0     | 1000.0 |

  Scenario: CreateOperacion Multiples con paginacion
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre      | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest1 | 30.0             | 0.0        | 60          |
      | CuentaTest2 | 50.0             | 0.0        | 40          |
    And Los siguientes monederos creados
      | nombre        | cantidad_inicial | diferencia |
      | MonederoTest1 | 20.0             | 0.0        |
      | MonederoTest2 | 40.0             | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | GastoTest   | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion    | cantidad | id_cuenta_abono | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest1 | 100.0    | 1               | 2                 | 1                    |
    Then Obtengo el codigo de estado 201
    When Creo la siguiente operacion
      | fecha      | descripcion    | cantidad | id_cuenta_abono | id_monedero_abono | id_categoria_ingreso |
      | 05/12/2023 | OperacionTest2 | 20.0     | 2               | 1                 | 1                    |
    Then Obtengo el codigo de estado 201
    When Creo la siguiente operacion
      | fecha      | descripcion    | cantidad | id_cuenta_cargo | id_monedero_cargo | id_categoria_gasto |
      | 06/12/2023 | OperacionTest3 | 20.0     | 1               | 2                 | 1                  |
    Then Obtengo el codigo de estado 201
    When Creo la siguiente operacion
      | fecha      | descripcion    | cantidad | id_cuenta_cargo | id_monedero_cargo | id_categoria_gasto |
      | 07/12/2023 | OperacionTest4 | 10.0     | 2               | 1                 | 1                  |
    Then Obtengo el codigo de estado 201
    When Listo 3 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | fecha      | descripcion    | cantidad | id_cuenta_abono | id_monedero_abono | id_categoria_ingreso | id_cuenta_cargo | id_monedero_cargo | id_categoria_gasto |
      | 07/12/2023 | OperacionTest4 | 10.0     | None            | None              | None                 | 2               | 1                 | 1                  |
      | 06/12/2023 | OperacionTest3 | 20.0     | None            | None              | None                 | 1               | 2                 | 1                  |
      | 05/12/2023 | OperacionTest2 | 20.0     | 2               | 1                 | 1                    | None            | None              | None               |
    And Hay mas elementos en la lista paginada
    When Listo 3 operaciones desde la pagina 3
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | fecha      | descripcion    | cantidad | id_cuenta_abono | id_monedero_abono | id_categoria_ingreso | id_cuenta_cargo | id_monedero_cargo | id_categoria_gasto |
      | 04/12/2023 | OperacionTest1 | 100.0    | 1               | 2                 | 1                    | None            | None              | None               |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre      | cantidad_inicial | diferencia | total |
      | CuentaTest1 | 30.0             | 80.0       | 110.0 |
      | CuentaTest2 | 50.0             | 10.0       | 60.0  |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre        | cantidad_inicial | diferencia | total |
      | MonederoTest1 | 20.0             | 10.0       | 30.0  |
      | MonederoTest2 | 40.0             | 80.0       | 120.0 |


  Scenario: CreateOperacion Transferencia de monederos correcto con categorias
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre      | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest1 | 30.0             | 0.0        | 60          |
      | CuentaTest2 | 50.0             | 0.0        | 40          |
    And Los siguientes monederos creados
      | nombre        | cantidad_inicial | diferencia |
      | MonederoTest1 | 20.0             | 0.0        |
      | MonederoTest2 | 40.0             | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    And Las siguientes categorias_gasto creadas
      | descripcion | id_cuenta_cargo_defecto | id_monedero_defecto |
      | GastoTest   | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_monedero_abono | id_monedero_cargo | id_categoria_ingreso | id_categoria_gasto |
      | 04/12/2023 | OperacionTest | 10.0     | 2                 | 1                 | 1                    | 1                  |
    Then Obtengo el codigo de estado 201
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | fecha      | descripcion   | cantidad | id_monedero_abono | id_monedero_cargo | nombre_monedero_abono | nombre_monedero_cargo | id_cuenta_abono | id_cuenta_cargo |
      | 04/12/2023 | OperacionTest | 10.0     | 2                 | 1                 | MonederoTest2         | MonederoTest1         | None            | None            |
    And No hay mas elementos en la lista paginada
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre        | cantidad_inicial | diferencia | total |
      | MonederoTest1 | 20.0             | -10.0      | 10.0  |
      | MonederoTest2 | 40.0             | 10.0       | 50.0  |
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre      | cantidad_inicial | diferencia | total |
      | CuentaTest1 | 30.0             | 0.0        | 30.0  |
      | CuentaTest2 | 50.0             | 0.0        | 50.0  |


  Scenario: DeleteOperacion con ponderacion
    Given Una sesion correcta
    And Las siguientes cuentas creadas
      | nombre      | cantidad_inicial | diferencia | ponderacion |
      | CuentaTest1 | 0.0              | 0.0        | 60          |
      | CuentaTest2 | 0.0              | 0.0        | 40          |
    And Los siguientes monederos creados
      | nombre       | cantidad_inicial | diferencia |
      | MonederoTest | 0.0              | 0.0        |
    And Las siguientes categorias_ingreso creadas
      | descripcion | id_cuenta_abono_defecto | id_monedero_defecto |
      | IngresoTest | 1                       | 1                   |
    When Creo la siguiente operacion
      | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso |
      | 04/12/2023 | OperacionTest | 1000.0   | 1                 | 1                    |
    Then Obtengo el codigo de estado 201
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista paginada
      | id | fecha      | descripcion   | cantidad | id_monedero_abono | id_categoria_ingreso | nombre_cuenta_abono | nombre_monedero_abono | descripcion_categoria_ingreso |
      | 1  | 04/12/2023 | OperacionTest | 1000.0   | 1                 | 1                    | None                | MonederoTest          | IngresoTest                   |
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre      | diferencia | total |
      | CuentaTest1 | 600.0      | 600.0 |
      | CuentaTest2 | 400.0      | 400.0 |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre       | diferencia | total  |
      | MonederoTest | 1000.0     | 1000.0 |
    When Borro la operacion con id 1
    Then Obtengo el codigo de estado 200
    When Listo 10 operaciones desde la pagina 0
    Then Obtengo el codigo de estado 200
    And  No obtengo nada paginado
    And No hay mas elementos en la lista paginada
    When Listo las cuentas
    Then  Obtengo la siguiente lista
      | nombre      | diferencia | total |
      | CuentaTest1 | 0.0        | 0.0   |
      | CuentaTest2 | 0.0        | 0.0   |
    When Listo los monederos
    Then Obtengo el codigo de estado 200
    And  Obtengo la siguiente lista
      | nombre       | diferencia | total |
      | MonederoTest | 0.0        | 0.0   |
