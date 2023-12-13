function add_cuenta() {
    var nombre = $.trim($("#addTypeNombreX").val());
    var cantidad_inicial = $("#addTypeCantidadInicialX").val();
    var ponderacion = $("#addTypePonderacionX").val();


    var data = {
        nombre: nombre,
        cantidad_inicial: cantidad_inicial,
        ponderacion:ponderacion
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/cuenta", true);
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

function delete_cuenta(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/cuenta/"+id, true);
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

function update_cuenta() {
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
    xhttp.open("POST", "/finanzas/cuenta/"+id, true);
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

get_local_number = function(num){
    return $.fn.dataTable.render.number('', ',', 2).display(num);
}

render_dinero = function (data, type) {
    var number = get_local_number(data);
    var add_class = ""
    if (type === 'display') {
        if (data > 0)
            add_class = "text-success "
        else if (data < 0)
            add_class = "text-danger "
        return "<span class='ms-2 font-weight-bold "+add_class+"'>"+number+"</span><span class='ms-2 font-weight-bold "+add_class+"'>€</span>"
    }
    return data
}

render_actions = function (data, type) {
    if (type === 'display') {
        if (data != 0) {
            edit =  '<a class="edit-element font-18 text-info me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Edit" data-bs-original-title="Edit" data-element="'+data+'"><i class="uil uil-pen"></i></a>'
            del = '<a class="delete-element font-18 text-danger me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Delete" data-bs-original-title="Borrar" data-element="'+data+'"><i class="uil uil-trash"></i></a>'
            return edit + del
        }
        return ""
    }
    return data
}

$( document ).ready(function() {

    table = $('#lista_tabla')
        .on('xhr.dt', function ( e, settings, json, xhr ) {
            var ponderacion = 0;
            var total_inicial = 0
            var total_diferencia = 0
            var total = 0
            for (var i=0; i<json.length; i++) {
                ponderacion+=json[i].ponderacion
                total_inicial+=json[i].cantidad_inicial
                total_diferencia+=json[i].diferencia
                json[i]["tipo_row"] = "Cuentas"
            }
            total = total_inicial+total_diferencia;
            if (ponderacion != 100){
                $("#ponderacion-label").text("La ponderación no suma 100, esto puede traer problemas con las operaciones que involucren todas las cuentas")
            } else
                $("#ponderacion-label").text("")
            json.push({
            "id":0,
            "nombre":"Total",
            "ponderacion":ponderacion,
            "cantidad_inicial":total_inicial,
            "diferencia":total_diferencia,
            "total": total,
            "DT_RowClass" : "resumen-total",
            "tipo_row" : "Resumen"
            })
         })
        .DataTable({
        ajax: {
            url:'/finanzas/cuenta',
            dataSrc: '',
        },
        columns: [
            {
                data:'tipo_row',
                type: "string",
                visible: false
            },
            {
                data:'nombre',
                type: "string"
            },
            {
                data:'ponderacion',
                type: "num"
            },
            {
                data:'cantidad_inicial',
                render: render_dinero,
                type: "num"
            },
            {
                data:'diferencia',
                render: render_dinero,
                type: "num"
            },
            {
                data:'total',
                render: render_dinero,
                type: "num"
            },
            {
                className: 'text-end',
                data:'id',
                render: render_actions,
                type: "num",
                orderSequence:[]
            }
        ],
        rowGroup: {
            dataSrc: "tipo_row"
        },
        orderFixed: [0, 'asc'],
        order: [[1, 'asc']],
        info: true,
        paging: false,
        searching: false,
        scrollX: false,
        language: {
            info: 'Total _MAX_ cuentas',
            infoEmpty: 'No hay cuentas',
            loadingRecords: "Cargando...",
            decimal:",",
        }
    });

    table.on( 'draw', function () {
        $('.dtrg-group').remove();
        activar_elements();
        $('.edit-element').on( "click", function() {
            var data = table.row($(this).parents('tr')).data()
            var id = data.id
            var nombre = data.nombre
            var cantidad_inicial = get_local_number(data.cantidad_inicial)
            var ponderacion = get_local_number(data.ponderacion)

            $("#editTypeNombreX").val(nombre)
            $("#editTypeCantidadInicialX").val(cantidad_inicial)
            $("#editTypePonderacionX").val(ponderacion)
            $("#editTypeIdX").val(id)

            $('#edit').modal('show')
        });
        $('.delete-element').on( "click", function() {
           delete_cuenta($(this).attr("data-element"))
        });
    });


    $('#add-button').on("click", function() {
        $("#addTypeNombreX").val('')
        $("#addTypeCantidadInicialX").val('')
        $("#addTypePonderacionX").val('')
        $("#addTypeMessageX").text('')
        $('#add').modal('show')
    });

    $('#add-close-button').on( "click", function() {
        $('#add').modal('hide')
    } );

    $('#add-submit-button').on( "click", function() {
       add_cuenta();
    });


    $('#edit-close-button').on( "click", function() {
        $('#edit').modal('hide')
    } );

    $('#edit-submit-button').on( "click", function() {
       update_cuenta()
    });

});


