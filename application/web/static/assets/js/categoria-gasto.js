function add_categoria_gasto() {
    var descripcion = $.trim($("#addTypeDescripcionX").val());
    var cuenta_id = $("#add-cuenta-select").val();
    var monedero_id = $("#add-monedero-select").val();

    var data = {
        descripcion: descripcion,
        id_cuenta_cargo_defecto: cuenta_id ? cuenta_id : null,
        id_monedero_defecto:monedero_id ? monedero_id : null
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/categoria_gasto", true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 201) {
                window.location = '/categorias-gasto.html';
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#addTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));

}

function delete_categoria_gasto(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/categoria_gasto/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/categorias-gasto.html';
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

function update_categoria_gasto() {
    var id = $.trim($("#editTypeIdX").val())
    var descripcion = $.trim($("#editTypeDescripcionX").val());
    var cuenta_id = $("#edit-cuenta-select").val();
    var monedero_id = $("#edit-monedero-select").val();

    var data = {
        descripcion: descripcion,
        id_cuenta_cargo_defecto: cuenta_id ? cuenta_id : null,
        id_monedero_defecto:monedero_id ? monedero_id : null
    }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/categoria_gasto/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/categorias-gasto.html';
            } else if (xhttp.status != 200){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#editTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));
}

render_actions = function (data, type) {
    if (type === 'display') {
        edit =  '<a class="edit-element font-18 text-info me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Edit" data-bs-original-title="Edit" data-element="'+data+'"><i class="uil uil-pen"></i></a>'
        del = '<a class="delete-element font-18 text-danger me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Delete" data-bs-original-title="Borrar" data-element="'+data+'"><i class="uil uil-trash"></i></a>'
        return edit + del
    }
    return data
}

render_nombre_cuenta = function (data, type) {
    new_data = data
    if (data == undefined)
        new_data = "Todas"
    if (type === 'display'){
        return '<span class="badge badge-danger-lighten">'+new_data+'</span>'
    }
    return new_data
}

render_nombre_monedero = function (data, type) {
    new_data = data
    if (data == undefined)
        new_data = "Ninguno"
    if (type === 'display'){
        return '<span class="badge badge-danger-lighten">'+new_data+'</span>'
    }
    return new_data
}

$( document).ready(function() {

    table = $('#lista_tabla').DataTable({
        ajax: {
            url:'/finanzas/categoria_gasto',
            dataSrc: '',
        },
        columns: [
            {
                data:'descripcion',
                type: "string"
            },
            {
                data:'nombre_cuenta_cargo_defecto',
                type: "string",
                render: render_nombre_cuenta
            },
            {
                data:'nombre_monedero_defecto',
                type: "string",
                render: render_nombre_monedero
            },
            {
                className: 'text-end',
                data:'id',
                render: render_actions,
                type: "num",
                orderSequence:[]
            }
        ],
        order: [[0, 'asc']],
        info: true,
        paging: false,
        searching: false,
        scrollX: false,
        language: {
            info: 'Total _MAX_ Categorías gasto',
            infoEmpty: 'No hay Categorías gasto',
            loadingRecords: "Cargando...",
            decimal:",",
        }
    });

    table.on( 'draw', function () {
        activar_tooltip();
        $('.edit-element').on( "click", function() {
            var data = table.row($(this).parents('tr')).data()
            var id = data.id
            var descripcion = data.descripcion
            var cuenta = data.id_cuenta_cargo_defecto
            var monedero = data.id_monedero_defecto

            $("#editTypeDescripcionX").val(descripcion);
            $("#edit-cuenta-select").val(cuenta).change();
            $("#edit-monedero-select").val(monedero).change();
            $("#editTypeIdX").val(id);

            $('#edit').modal('show')
        });






        $('.delete-element').on( "click", function() {
           delete_categoria_gasto($(this).attr("data-element"))
        });
    } );



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
       add_categoria_gasto();
    });


    $('#edit-close-button').on( "click", function() {
        $('#edit').modal('hide')
    } );

    $('#edit-submit-button').on( "click", function() {
       update_categoria_gasto()
    });





});
