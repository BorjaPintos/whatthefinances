$('#add-button').on( "click", function() {
    $("#addTypeNombreX").val('')
    $("#addTypeCantidadInicialX").val('')
    $("#addTypeMessageX").text('')
    $('#add').modal('show')
} );

$('#add-close-button').on( "click", function() {
    $('#add').modal('hide')
} );

$('#add-submit-button').on( "click", function() {
   add_monedero();
});

$('.edit-element').on( "click", function() {

    var id = $(this).attr("data-element")
    var nombre = $.trim($('#nombre-'+id).text())
    var cantidad_inicial = $('#cantidad_inicial-'+id).text()

    $("#editTypeNombreX").val(nombre)
    $("#editTypeCantidadInicialX").val(cantidad_inicial)
    $("#editTypeIdX").val(id)

    $('#edit').modal('show')
});

$('#edit-close-button').on( "click", function() {
    $('#edit').modal('hide')
} );

$('#edit-submit-button').on( "click", function() {
   update_monedero()
});

$('.delete-element').on( "click", function() {
   delete_monedero($(this).attr("data-element"))
});

function add_monedero() {
    var nombre = $.trim($("#addTypeNombreX").val());
    var cantidad_inicial = $("#addTypeCantidadInicialX").val();


    var data = {
        nombre: nombre,
        cantidad_inicial: cantidad_inicial,
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/monedero", true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 201) {
                window.location = '/monederos.html';
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#addTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));

}

function delete_monedero(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/monedero/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/monederos.html';
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

function update_monedero() {
    var id = $.trim($("#editTypeIdX").val())
    var nombre = $.trim($("#editTypeNombreX").val());
    var cantidad_inicial = $("#editTypeCantidadInicialX").val();


    var data = {
        nombre: nombre,
        cantidad_inicial: cantidad_inicial,
    }
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/monedero/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/monederos.html';
            } else if (xhttp.status != 200){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#editTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));
}
