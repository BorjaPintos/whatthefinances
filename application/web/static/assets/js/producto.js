function add_producto() {
    var nombre = $.trim($("#addTypeNombreX").val());
    var isin = $.trim($("#addTypeIsinX").val());
    var id_plataforma = $("#add-plataforma-select").val();
    var url = $.trim($("#addTypeURLX").val());

    var data = {
        nombre: nombre,
        isin: isin,
        id_plataforma: parseInt(id_plataforma) ? id_plataforma : null,
        url: url
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

function check_producto(isin) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/autovalorparticipacion/"+isin, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                alert("Producto encontrado en la plataforma")
            } else if (xhttp.status != 200){
                alert("Error al obtener el producto en la plataforma")
            }
    };
    xhttp.send();
}

function update_producto() {
    var id = $.trim($("#editTypeIdX").val())
    var nombre = $.trim($("#editTypeNombreX").val());
    var isin = $.trim($("#editTypeIsinX").val());
    var id_plataforma = $("#edit-plataforma-select").val();
    var url = $.trim($("#editTypeURLX").val());

    var data = {
        nombre: nombre,
        isin: isin,
        id_plataforma: parseInt(id_plataforma) ? id_plataforma : null,
        url: url
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

render_actions = function (data, type, row) {
    if (type === 'display') {
        edit =  '<a class="edit-element font-18 text-info me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Editar" data-bs-original-title="Editar" data-element="'+data+'"><i class="uil uil-pen"></i></a>'
        del = '<a class="delete-element font-18 text-danger me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Delete" data-bs-original-title="Borrar" data-element="'+data+'"><i class="uil uil-trash"></i></a>'

        check_enable = row.plataforma != undefined & row.url != undefined & row.url != ''
        check = ''
        if (check_enable) {
            check = '<a class="check-element font-18 text-danger me-2 disabled" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Check" data-bs-original-title="Comprobar conexión con la plataforma" data-element="'+row.isin+'"><i class="uil uil-sync-exclamation"></i></a>'
        }

        return check + edit + del
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
                data:'plataforma',
                type: "string"
            },
            {
                data:'url',
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
            var id_plataforma = data.id_plataforma
            var url = data.url

            $("#editTypeNombreX").val(nombre);
            $("#editTypeIsinX").val(isin);
            $("#editTypeIdX").val(id);
            $("#editTypeURLX").val(url);
            $("#edit-plataforma-select").val(id_plataforma).change()
            $('#edit').modal('show')
        });

        $('.delete-element').on("click", function() {
           delete_producto($(this).attr("data-element"))
        });

        $('.check-element').on("click", function() {
           check_producto($(this).attr("data-element"))
        });
    } );


    $('#add-button').on( "click", function() {
        $("#addTypeNombreX").val('')
        $("#addTypeIsinX").val('')
        $("#addTypeURLX").val('')
        $("#add-plataforma-select").val('')
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
