function add_dividendo() {
    var fecha = $("#addFechaDataPicker").val()
    var isin = $("#add-isin-select").val();
    var dividendo_por_accion = $("#addTypeDividendoPorAccionX").val();
    var retencion_por_accion = $("#addTypeRetencionPorAccionX").val();

    var data = {
        fecha: fecha,
        isin: isin,
        dividendo_por_accion: parseFloat(dividendo_por_accion).toFixed(2) ? dividendo_por_accion : null,
        retencion_por_accion: parseFloat(retencion_por_accion).toFixed(2) ? retencion_por_accion : null,
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/dividendo", true);
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

function delete_dividendo(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/dividendo/"+id, true);
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

function update_dividendo() {
    var id = $.trim($("#editTypeIdX").val())
    var fecha = $("#editFechaDataPicker").val()
    var isin = $("#edit-isin-select").val();
    var dividendo_por_accion = $("#editTypeDividendoPorAccionX").val();
    var retencion_por_accion = $("#editTypeRetencionPorAccionX").val();

    var data = {
        fecha: fecha,
        isin: isin,
        dividendo_por_accion: parseFloat(dividendo_por_accion).toFixed(2) ? dividendo_por_accion : null,
        retencion_por_accion: parseFloat(retencion_por_accion).toFixed(2) ? retencion_por_accion : null,
    }
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/dividendo/"+id, true);
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

get_daterangepicker_config = function(){
    return {
        singleDatePicker: true,
        timePicker: false,
        autoApply: false,
        autoUpdateInput: true,
        locale: {
          format: "DD/MM/YYYY",
          applyLabel: "Aplicar",
          cancelLabel: "Limpiar",
          weekLabel: "S",
          daysOfWeek: [
                "Do",
                "Lu",
                "Ma",
                "Mi",
                "Ju",
                "Vi",
                "Sa"
            ],
            monthNames: [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Julio",
                "Agosto",
                "Septiembre",
                "Octuber",
                "Noviembre",
                "Diciembre"
            ],
            firstDay: 1
        }
    }
}

get_local_number = function(num){
    return $.fn.dataTable.render.number('', ',', 2).display(num);
}

render_dinero = function (data, type) {
    var number = get_local_number(data);
    if (type === 'display') {
        return '<span class="badge custom-badge flex-grow-1 ms-2">'+number+'</span><span class="badge custom-badge flex-grow-1 ms-2">€</span>'
    }
    return data
}

render_actions = function (data, type) {
    if (type === 'display') {
        edit =  '<a class="edit-element font-18 text-info me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Edit" data-bs-original-title="Edit" data-element="'+data+'"><i class="uil uil-pen"></i></a>'
        del = '<a class="delete-element font-18 text-danger me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Delete" data-bs-original-title="Borrar" data-element="'+data+'"><i class="uil uil-trash"></i></a>'
        return edit + del
    }
    return data
}

render_isin = function (data, type) {
    var new_data = data
    if (data == undefined)
        new_data = "-"
    if (type === 'display'){
        return '<span class="badge custom-badge">'+new_data+'</span>'
    }
    return new_data
}

$(document).ready(function() {

    table = $('#lista_tabla').DataTable({
        ajax: {
            url:'/finanzas/dividendo',
            dataSrc: '',
        },
        columns: [
            {
                data:'fecha',
                type: "string"
            },
            {
                data:'isin',
                type: "string",
                render: render_isin,
            },
            {
                data:'dividendo_por_accion',
                type: "num",
                render: render_dinero,
            },
            {
                data:'retencion_por_accion',
                type: "num",
                render: render_dinero,
            },
            {
                className: 'text-end',
                data:'id',
                render: render_actions,
                type: "num",
                orderSequence:[]
            }
        ],
        order: [[0, 'desc']],
        info: true,
        paging: false,
        searching: false,
        scrollX: false,
        language: {
            info: 'Total _MAX_ Dividendos',
            infoEmpty: 'No hay Dividendos',
            loadingRecords: "Cargando...",
            decimal:",",
        }
    });

    table.on( 'draw', function () {
        activar_elements();
        $('.edit-element').on( "click", function() {
            var data = table.row($(this).parents('tr')).data()
            var id = data.id
            var isin = data.isin
            var fecha = data.fecha
            var dividendo_por_accion = get_local_number(data.dividendo_por_accion)
            var retencion_por_accion = get_local_number(data.retencion_por_accion)

            $("#editTypeIdX").val(id)
            $('#editFechaDataPicker').val(fecha);
            $("#edit-isin-select").val(isin)
            $("#editTypeDividendoPorAccionX").val(dividendo_por_accion)
            $("#editTypeRetencionPorAccionX").val(retencion_por_accion)
            $("#editTypeMessageX").text('')
            $('#edit').modal('show')
        });

        $('.delete-element').on( "click", function() {
           delete_broker($(this).attr("data-element"))
        });
    } );


    $('#addFechaDataPicker').daterangepicker(get_daterangepicker_config());

    $('#add-button').on( "click", function() {
        $('#addFechaDataPicker').val(moment().format("DD/MM/YYYY"));
        $("#add-isin-select").val('')
        $("#addTypeDividendopPorAccionX").val('')
        $("#addTypeRetencionPorAccionX").val('')
        $("#addTypeMessageX").text('')
        $('#add').modal('show')
    } );

    $('#add-close-button').on( "click", function() {
        $('#add').modal('hide')
    });

    $('#add-submit-button').on( "click", function() {
       add_dividendo();
    });

    $('#edit-close-button').on( "click", function() {
        $('#edit').modal('hide')
    } );

    $('#edit-submit-button').on( "click", function() {
       update_dividendo()
    });


});


