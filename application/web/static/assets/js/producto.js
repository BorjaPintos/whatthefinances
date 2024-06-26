function add_producto() {
    var nombre = $.trim($("#addTypeNombreX").val());
    var isin = $.trim($("#addTypeIsinX").val());

    var data = {
        nombre: nombre,
        isin: isin
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/producto", true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 201) {
                $('#add').modal('hide')
                table.ajax.reload( null, false );
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#addTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));

}

function delete_producto(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/producto/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                table.ajax.reload( null, false );
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

function update_producto() {
    var id = $.trim($("#editTypeIdX").val())
    var nombre = $.trim($("#editTypeNombreX").val());
    var isin = $.trim($("#editTypeIsinX").val());

    var data = {
        nombre: nombre,
        isin: isin
    }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/producto/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                $('#edit').modal('hide')
                table.ajax.reload( null, false );
            } else if (xhttp.status != 200){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#editTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));
}

render_actions = function (data, type) {
    if (type === 'display') {
        edit =  '<a class="edit-element font-18 text-info me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Editar" data-bs-original-title="Editar" data-element="'+data+'"><i class="uil uil-pen"></i></a>'
        del = '<a class="delete-element font-18 text-danger me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Delete" data-bs-original-title="Borrar" data-element="'+data+'"><i class="uil uil-trash"></i></a>'
        return edit + del
    }
    return data
}


$( document).ready(function() {

    table = $('#lista_tabla').DataTable({
        ajax: {
            url:'/finanzas/producto',
            dataSrc: '',
        },
        columns: [
            {
                data:'nombre',
                type: "string"
            },
            {
                data:'isin',
                type: "string"
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
            info: 'Total _MAX_ Productos',
            infoEmpty: 'No hay Productos',
            loadingRecords: "Cargando...",
            decimal:",",
        }
    });

    table.on( 'draw', function () {
        activar_elements();
        $('.edit-element').on( "click", function() {
            var data = table.row($(this).parents('tr')).data()
            var id = data.id
            var nombre = data.nombre
            var isin = data.isin

            $("#editTypeNombreX").val(nombre);
            $("#editTypeIsinX").val(isin);
            $("#editTypeIdX").val(id);
            $('#edit').modal('show')
        });

        $('.delete-element').on( "click", function() {
           delete_bolsa($(this).attr("data-element"))
        });
    } );



    $('#add-button').on( "click", function() {
        $("#addTypeNombreX").val('')
        $("#addTypeIsinX").val('')
        $("#addTypeMessageX").text('')
        $('#add').modal('show')
    } );

    $('#add-close-button').on( "click", function() {
        $('#add').modal('hide')
    } );

    $('#add-submit-button').on( "click", function() {
       add_producto();
    });


    $('#edit-close-button').on( "click", function() {
        $('#edit').modal('hide')
    } );

    $('#edit-submit-button').on( "click", function() {
       update_producto()
    });


});
