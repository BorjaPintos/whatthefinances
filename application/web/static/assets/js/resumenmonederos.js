$(document).ready(function() {
    get_tabla_monederos();

    $('#show-eliminados-resumen').on("change", function() {
        get_tabla_monederos();
    });
});

function get_tabla_monederos(){
    var eliminado = $('#show-eliminados-resumen').is(':checked');
    $.get("finanzas/monedero?order_property=id&order_type=asc&eliminado=" + eliminado, function( data_monederos ) {
        create_tabla_cosas_concreta(data_monederos, "monederos-total", "total", "monederos", "id_monedero");
        create_tabla_cosas_concreta(data_monederos, "monederos-ingreso", "ingreso", "monederos", "id_monedero");
        create_tabla_cosas_concreta(data_monederos, "monederos-gasto","gasto", "monederos", "id_monedero");
    });
}
