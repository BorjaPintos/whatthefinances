$(document).ready(function() {
    get_tabla_cuentas();
});

function get_tabla_cuentas(){

    $.get("finanzas/cuenta?order_property=id&order_type=asc", function( data_cuentas ) {
        create_tabla_cosas_concreta(data_cuentas, "cuentas-total", "total", "cuentas", "id_cuenta");
        create_tabla_cosas_concreta(data_cuentas, "cuentas-ingreso", "ingreso", "cuentas", "id_cuenta");
        create_tabla_cosas_concreta(data_cuentas, "cuentas-gasto", "gasto", "cuentas", "id_cuenta");
    });
}
