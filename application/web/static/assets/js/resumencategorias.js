$(document).ready(function() {
    get_tabla_categorias_gasto();
    get_tabla_categorias_ingreso();
});

function get_tabla_categorias_gasto(){

    $.get("finanzas/categoria_gasto?order_property=id&order_type=asc", function( categorias ) {
        for (i in categorias)
            categorias[i].nombre = categorias[i].descripcion
        create_tabla_cosas_concreta(categorias, "gastos", "gasto", "categorias-gasto", "id_categoria_gasto");
    });
}

function get_tabla_categorias_ingreso(){

    $.get("finanzas/categoria_ingreso?order_property=id&order_type=asc", function( categorias ) {
        for (i in categorias)
            categorias[i].nombre = categorias[i].descripcion
        create_tabla_cosas_concreta(categorias, "ingresos", "ingreso", "categorias-ingreso", "id_categoria_ingreso");
    });
}
