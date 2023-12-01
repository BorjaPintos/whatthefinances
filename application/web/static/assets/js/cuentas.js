$('#add-button').on( "click", function() {
    $("#addTypeNombreX").val('')
    $("#addTypeTotalX").val('')
    $("#addTypePonderacionX").val('')
    $("#addTypeMessageX").text('')
    $('#add').modal('show')
} );

$('#add-close-button').on( "click", function() {
    $('#add').modal('hide')
} );

$('#add-submit-button').on( "click", function() {
   add_cuenta();
});

$('.edit-element').on( "click", function() {

    var id = $(this).attr("data-element")
    var nombre = $.trim($('#nombre-'+id).text())
    var total = $('#total-'+id).text()
    var ponderacion = $('#ponderacion-'+id).text()

    $("#editTypeNombreX").val(nombre)
    $("#editTypeTotalX").val(total)
    $("#editTypePonderacionX").val(ponderacion)
    $("#editTypeIdX").val(id)

    $('#edit').modal('show')
});

$('#edit-close-button').on( "click", function() {
    $('#edit').modal('hide')
} );

$('#edit-submit-button').on( "click", function() {
   update_cuenta()
});

$('.delete-element').on( "click", function() {
   delete_cuenta($(this).attr("data-element"))
});

function add_cuenta() {
    var nombre = $.trim($("#addTypeNombreX").val());
    var total = $("#addTypeTotalX").val();
    var ponderacion = $("#addTypePonderacionX").val();


    var data = {
        nombre: nombre,
        total: total,
        ponderacion:ponderacion
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/cuenta", true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 201) {
                window.location = '/cuentas.html';
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#addTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));

}

function delete_cuenta(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/cuenta/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/cuentas.html';
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

function update_cuenta() {
    var id = $.trim($("#editTypeIdX").val())
    var nombre = $.trim($("#editTypeNombreX").val());
    var total = $("#editTypeTotalX").val();
    var ponderacion = $("#editTypePonderacionX").val();


    var data = {
        nombre: nombre,
        total: total,
        ponderacion:ponderacion
    }
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/cuenta/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/cuentas.html';
            } else if (xhttp.status != 200){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#editTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));
}
