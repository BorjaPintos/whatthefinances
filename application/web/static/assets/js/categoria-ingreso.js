$('#add-button').on( "click", function() {
    $("#addTypeDescripcionX").val('')
    $("#cuenta-select").val('')
    $("#monedero-select").val('')
    $("#addTypeMessageX").text('')
    $('#add').modal('show')
} );

$('#add-close-button').on( "click", function() {
    $('#add').modal('hide')
} );

$('#add-submit-button').on( "click", function() {
   add_categoria_ingreso();
});

$('.edit-element').on( "click", function() {

    var id = $(this).attr("data-element")
    var descripcion = $.trim($('#descripcion-'+id).text())
    var cuenta = $('#id-cuenta-defecto-'+id).val()
    var monedero = $('#id-monedero-defecto-'+id).val()

    $("#editTypeDescripcionX").val(descripcion);
    $("#edit-cuenta-select").val(cuenta).change();
    $("#edit-monedero-select").val(monedero).change();
    $("#editTypeIdX").val(id);

    $('#edit').modal('show')

});

$('#edit-close-button').on( "click", function() {
    $('#edit').modal('hide')
} );

$('#edit-submit-button').on( "click", function() {
   update_categoria_ingreso()
});

$('.delete-element').on( "click", function() {
   delete_categoria_ingreso($(this).attr("data-element"))
});

function add_categoria_ingreso() {
    var descripcion = $.trim($("#addTypeDescripcionX").val());
    var cuenta_id = $("#add-cuenta-select").val();
    var monedero_id = $("#add-monedero-select").val();

    var data = {
        descripcion: descripcion,
        id_cuenta_abono_defecto: cuenta_id ? cuenta_id : null,
        id_monedero_defecto:monedero_id ? monedero_id : null
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/categoria_ingreso", true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 201) {
                window.location = '/categorias-ingreso.html';
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#addTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));

}

function delete_categoria_ingreso(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/categoria_ingreso/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/categorias-ingreso.html';
            } else if (xhttp.status != 200){
                try {
                    var respuesta = JSON.parse(xhttp.responseText).message;
                } catch (error){
                    respuesta = "Error inesperado";
                }
                $("#errorTypeMessageX").text(respuesta)
                $("#error-modal").modal("show");
            }
    };
    xhttp.send();
}

function update_categoria_ingreso() {
    var id = $.trim($("#editTypeIdX").val())
    var descripcion = $.trim($("#editTypeDescripcionX").val());
    var cuenta_id = $("#edit-cuenta-select").val();
    var monedero_id = $("#edit-monedero-select").val();

    var data = {
        descripcion: descripcion,
        id_cuenta_abono_defecto: cuenta_id ? cuenta_id : null,
        id_monedero_defecto:monedero_id ? monedero_id : null
    }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/categoria_ingreso/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/categorias-ingreso.html';
            } else if (xhttp.status != 200){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#editTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));
}
