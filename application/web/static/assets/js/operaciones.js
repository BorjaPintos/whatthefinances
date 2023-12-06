$( document ).ready(function() {
    $('#addFechaDataPicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'es-ES'
    });
    $('#editFechaDataPicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'es-ES'
    });
});


$('#add-button').on( "click", function() {
    $("#addTypeNombreX").val('')
    $("#addTypeCantidadInicialX").val('')
    $("#addTypePonderacionX").val('')
    $("#addTypeMessageX").text('')
    $('#addFechaDataPicker').datepicker('update',  new Date());
    $('#add').modal('show')
} );

$('#add-close-button').on( "click", function() {
    $('#add').modal('hide')
});

$('#add-submit-button').on( "click", function() {
   add_operacion();
});

$('.edit-element').on( "click", function() {

    var id = $(this).attr("data-element")
    var descripcion = $.trim($('#descripcion-'+id).text())
    var fecha = $.trim($('#fecha-'+id).text())

    $("#editTypeDescripcionX").val(descripcion)
    $('#editFechaDataPicker').datepicker('update',  fecha);

    $('#edit').modal('show')
});

$('#edit-close-button').on( "click", function() {
    $('#edit').modal('hide')
} );

$('#edit-submit-button').on( "click", function() {
   update_operacion()
});

$('.delete-element').on( "click", function() {
   delete_operacion($(this).attr("data-element"))
});

function add_operacion() {
    var fecha = $("#addFechaDataPicker").val()
    var descripcion = $("#addTypeDescripcionX").val();


    var data = {
        fecha: fecha,
        descripcion: descripcion,
        cantidad: 10,

        id_categoria_gasto:1,
        id_monedero_cargo:1,
        id_cuenta_cargo:1
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/operacion", true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 201) {
                window.location = '/operaciones.html';
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#addTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));

}

function delete_operacion(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/operacion/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/operaciones.html';
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

function update_operacion() {
    var id = $.trim($("#editTypeIdX").val())
    var nombre = $.trim($("#editTypeNombreX").val());
    var cantidad_inicial = $("#editTypeCantidadInicialX").val();
    var ponderacion = $("#editTypePonderacionX").val();


    var data = {
        nombre: nombre,
        cantidad_inicial: cantidad_inicial,
        ponderacion:ponderacion
    }
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/operacion/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/operaciones.html';
            } else if (xhttp.status != 200){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#editTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));
}
