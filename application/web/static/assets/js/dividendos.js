function add_dividendo() {
    var fecha = $("#addFechaDataPicker").val()
    var isin = $("#add-isin-select").val();
    var dividendo_por_participacion = $("#addTypeDividendoPorParticipacionX").val();
    var retencion_por_participacion = $("#addTypeRetencionPorParticipacionX").val();

    var data = {
        fecha: fecha,
        isin: isin,
        dividendo_por_participacion: parseFloat(dividendo_por_participacion).toFixed(2) ? dividendo_por_participacion : null,
        retencion_por_participacion: parseFloat(retencion_por_participacion).toFixed(2) ? retencion_por_participacion : null,
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
    var dividendo_por_participacion = $("#editTypeDividendoPorParticipacionX").val();
    var retencion_por_participacion = $("#editTypeRetencionPorParticipacionX").val();

    var data = {
        fecha: fecha,
        isin: isin,
        dividendo_por_participacion: parseFloat(dividendo_por_participacion).toFixed(2) ? dividendo_por_participacion : null,
        retencion_por_participacion: parseFloat(retencion_por_participacion).toFixed(2) ? retencion_por_participacion : null,
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

render_nombre = function(data, type, row){

    if (type == 'display'){
        var isin = row["isin"]
        if (data.length>45)
            return '<span class="badge custom-badge" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="'+data+ ' - '+ isin +'">'+  (data.substring(0, 45) + "...") +'</span>'
        else
            return '<span class="badge custom-badge" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="'+data+ ' - '+ isin +'">'+  data +'</span>'

    }
    return data
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
                data:'nombre',
                type: "string",
                render: render_nombre,
            },
            {
                data:'dividendo_por_participacion',
                type: "num",
                render: render_dinero,
            },
            {
                data:'retencion_por_participacion',
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
            var dividendo_por_participacion = get_local_number(data.dividendo_por_participacion)
            var retencion_por_participacion = get_local_number(data.retencion_por_participacion)

            $("#editTypeIdX").val(id)
            $('#editFechaDataPicker').val(fecha);
            $("#edit-isin-select").val(isin)
            $("#editTypeDividendoPorParticipacionX").val(dividendo_por_participacion)
            $("#editTypeRetencionPorParticipacionX").val(retencion_por_participacion)
            $("#editTypeMessageX").text('')
            $('#edit').modal('show')
        });

        $('.delete-element').on( "click", function() {
           delete_dividendo($(this).attr("data-element"))
        });
    } );


    $('#addFechaDataPicker').daterangepicker(get_daterangepicker_config());
    $('#editFechaDataPicker').daterangepicker(get_daterangepicker_config());

    $('#add-button').on( "click", function() {
        $('#addFechaDataPicker').val(moment().format("DD/MM/YYYY"));
        $("#add-isin-select").val('')
        $("#addTypeDividendopPorParticipacionX").val('')
        $("#addTypeRetencionPorParticipacionX").val('')
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


