

function add_posicion_accion() {
    var fecha_compra = $("#addFechaCompraDataPicker").val()
    var isin = $("#addTypeISINX").val();
    var id_bolsa = $("#add-bolsa-select").val();
    var id_broker = $("#add-broker-select").val();
    var precio_accion = $("#addTypePrecioAccionX").val();
    var numero_acciones = $("#addTypeNumeroAccionesX").val();
    var comisiones_compra = $("#addTypeComisionesCompraX").val();
    var otras_comisiones = $("#addTypeOtrasComisionesX").val();


    var data = {
        fecha_compra: fecha_compra,
        isin: isin,
        id_bolsa: id_bolsa,
        id_broker: id_broker,
        precio_accion_sin_comision: parseFloat(precio_accion).toFixed(4) ? precio_accion : null,
        numero_acciones: parseInt(numero_acciones) ? numero_acciones : null,
        comision_compra: parseFloat(comisiones_compra).toFixed(4) ? comisiones_compra : 0,
        otras_comisiones: parseFloat(otras_comisiones).toFixed(4) ? otras_comisiones : 0.0
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/posicionaccion", true);
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

function delete_posicion_accion(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/posicionaccion/"+id, true);
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

function update_posicion_accion() {
    var id = $.trim($("#editTypeIdX").val())

    var fecha_compra = $("#editFechaCompraDataPicker").val()
    var isin = $("#editTypeISINX").val();
    var id_bolsa = $("#edit-bolsa-select").val();
    var id_broker = $("#edit-broker-select").val();
    var precio_accion = $("#editTypePrecioAccionX").val();
    var numero_acciones = $("#editTypeNumeroAccionesX").val();
    var comisiones_compra = $("#editTypeComisionesCompraX").val();
    var otras_comisiones = $("#editTypeOtrasComisionesX").val();


    var data = {
        fecha_compra: fecha_compra,
        isin: isin,
        id_bolsa: id_bolsa,
        id_broker: id_broker,
        precio_accion_sin_comision: parseFloat(precio_accion).toFixed(4) ? precio_accion : 0.0,
        numero_acciones: parseInt(numero_acciones) ? numero_acciones : 0,
        comision_compra: parseFloat(comisiones_compra).toFixed(4) ? comisiones_compra : 0.0,
        otras_comisiones: parseFloat(otras_comisiones).toFixed(4) ? otras_comisiones : 0.0
    }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/posicionaccion/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                $('#edit').modal('hide')
                table.ajax.reload( null, false );
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#editTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));
}

get_local_number = function(num){
    return $.fn.dataTable.render.number('', ',', 2).display(num);
}

get_local_integer = function(num){
    return $.fn.dataTable.render.number('').display(num);
}

render_dinero = function (data, type) {
    var number = get_local_number(data);
    if (type === 'display') {
        return '<span class="badge custom-badge flex-grow-1 ms-2">'+number+'</span><span class="badge custom-badge flex-grow-1 ms-2">€</span>'
    }
    return data
}

render_total_dinero = function (data, type, row) {
    var number = get_local_number(data);
    if (type === 'display') {
        explicacion = '( numero_acciones * precio_accion_sin_comision ) + comision_compra + otras_comisiones'
        if (! row['abierta']){
            explicacion += '+ comision_venta'
        }
        explicacion += ' = (' + row['numero_acciones'] + ' * ' +  row['precio_accion_sin_comision'] + ') + ' + row['comision_compra'] + ' + ' + row['otras_comisiones']
        if (! row['abierta']){
            explicacion += ' + ' + row['comision_venta']
        }
        explicacion += ' = ' + number
        return '<span class="badge custom-badge flex-grow-1 ms-2" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="'+explicacion+'">'+number+'</span><span class="badge custom-badge flex-grow-1 ms-2">€</span>'
    }
    return data
}

render_actions = function (data, type) {
    if (type === 'display') {
        cerrar_posicion =  '<a class="cerrar-posicion-element font-18 text-info me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Cerrar Posición" data-bs-original-title="Cerrar Posición" data-element="'+data+'"><i class="uil uil-sign-out-alt"></i></a>'
        edit =  '<a class="edit-element font-18 text-info me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Editar" data-bs-original-title="Editar" data-element="'+data+'"><i class="uil uil-pen"></i></a>'
        del = '<a class="delete-element font-18 text-danger me-2" data-bs-toggle="tooltip" data-bs-placement="top" aria-label="Borrar" data-bs-original-title="Borrar" data-element="'+data+'"><i class="uil uil-trash"></i></a>'
        return cerrar_posicion + edit + del
    }
    return data
}

render_nombre = function(data, type, row){

    if (type == 'display'){
        var isin = row["isin"]
        if (data.length>15)
            return '<span class="badge custom-badge" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="'+data+ ' - '+ isin +'">'+  (data.substring(0, 15) + "...") +'</span>'
        else
            return '<span class="badge custom-badge" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="'+data+ ' - '+ isin +'">'+  data +'</span>'

    }
    return data
}

render_texto = function(data, type){

    if (type == 'display'){
        if (data.length>15)
            return '<span class="badge custom-badge" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="'+data+'">'+  (data.substring(0, 15) + "...") +'</span>'
        else
          return '<span class="badge custom-badge">'+ data +'</span>'

    }
    return data
}

get_datapicker_conf = function(){
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



$(document).ready(function() {


    $('#addFechaCompraDataPicker').daterangepicker(get_datapicker_conf());

    $('#editFechaCompraDataPicker').daterangepicker(get_datapicker_conf());

    $('#search-fecha-compra-begin-datapicker').daterangepicker(get_datapicker_conf());
    $('#search-fecha-compra-begin-datapicker').val('')
    $('#search-fecha-compra-end-datapicker').daterangepicker(get_datapicker_conf());
    $('#search-fecha-compra-end-datapicker').val('')

    $('#search-fecha-compra-begin-datapicker').on('cancel.daterangepicker', function(ev, picker) {
        $('#search-fecha-compra-begin-datapicker').val('');
    });
    $('#search-fecha-compra-end-datapicker').on('cancel.daterangepicker', function(ev, picker) {
        $('#search-fecha-compra-end-datapicker').val('');
    });

    table = $('#lista_tabla')
         .on('preXhr.dt', function ( e, settings, data ) {
               data.count = data.length
               data.offset = data.start
               data.order_property = data.columns[data.order[0].column].data
               data.order_type = data.order[0].dir
         })
         .on('xhr.dt', function ( e, settings, json, xhr ) {
            for (var i=0; i<json.elements.length; i++) {
                if ( json.elements[i].ganacia_con_comosiones_y_dividendos > 0)
                    json.elements[i].DT_RowClass = "ingreso"
                else if (json.elements[i].ganacia_con_comosiones_y_dividendos < 0)
                    json.elements[i].DT_RowClass = "gasto"
                else
                    json.elements[i].DT_RowClass = "transferencia"
            }
            json.recordsTotal = json.total_elements
            json.recordsFiltered = json.total_elements
         })
        .DataTable({
        dom: '<flrt<"#table_fotter"ip>',
        serverSide:true,
        ajax: {
            url:'/finanzas/posicionaccion',
            data: function (d) {
                var begin_fecha_compra = $('#search-fecha-compra-begin-datapicker').val()
                var end_fecha_compra = $('#search-fecha-compra-end-datapicker').val()

                if (begin_fecha_compra != '')
                    d.begin_fecha_compra = begin_fecha_compra
                if (end_fecha_compra != '')
                    d.end_fecha_compra = end_fecha_compra
            },
            dataSrc: 'elements',
        },
        columns: [
            {
                data:'fecha_compra',
                type: "string",
                render: render_texto,
                width: "5%"
            },
            {
                data:'nombre',
                type: "string",
                render: render_nombre,
                width: "10%"
            },
            {
                data:'nombre_bolsa',
                type: "string",
                render: render_texto,
                width: "10%"
            },
            {
                data:'nombre_broker',
                type: "string",
                render: render_texto,
                width: "7%"
            },{
                data:'precio_accion_sin_comision',
                type: "num",
                render: render_dinero,
                width: "10%"
            },
            {
                data:'numero_acciones',
                type: "num",
                render: render_texto,
                width: "5%"
            },
            {
                data:'total',
                type: "num",
                render: render_total_dinero,
                width: "10%"
            },
            {
                data:'valor_accion',
                type: "num",
                render: render_dinero,
                width: "10%"
            },
            {
                data:'valor_actual',
                type: "num",
                render: render_dinero,
                width: "10%"
            },
            {
                data:'ganacia_sin_comosiones',
                type: "num",
                render: render_dinero,
                width: "10%"
            },
            {
                data:'ganacia_con_comosiones',
                type: "num",
                render: render_dinero,
                width: "10%"
            },
            {
                data:'dividendos_total',
                type: "num",
                render: render_dinero,
                width: "10%"
            },
            {
                data:'ganacia_con_comosiones_y_dividendos',
                type: "num",
                render: render_dinero,
                width: "10%"
            },
            {
                className: 'text-end',
                data:'id',
                render: render_actions,
                type: "num",
                orderSequence:[],
                width: "12%"
            }
        ],
        order: [[0, 'asc']],
        info: true,
        lengthChange: false,
        paging: true,
        pageLength: 30,
        searching: false,
        scrollX: false,
        responsive: true,
        language: {
            info: 'Total _MAX_ Posiciones de Acciones',
            infoEmpty: 'No hay Posiciones de Acciones',
            zeroRecords: "No hay Posiciones de Acciones",
            loadingRecords: "Cargando...",
            decimal:",",
        }
    });


    table.on('draw', function () {
        activar_elements();

        $('.edit-element').on( "click", function() {

            var posicion_accion = table.row($(this).parents('tr')).data()
            var id = posicion_accion.id
            var fecha_compra = posicion_accion.fecha_compra
            var isin = posicion_accion.isin;
            var id_bolsa = posicion_accion.id_bolsa;
            var id_broker = posicion_accion.id_broker;
            var numero_acciones = get_local_integer(posicion_accion.numero_acciones);
            var precio_accion = get_local_number(posicion_accion.precio_accion_sin_comision);
            var comision_compra = get_local_number(posicion_accion.comision_compra)
            var otras_comisiones = get_local_number(posicion_accion.otras_comisiones)


            $("#editTypeIdX").val(id)
            $('#editFechaCompraDataPicker').val(fecha_compra);
            $("#editTypeISINX").val(isin)
            $("#edit-bolsa-select").val(id_bolsa).change();
            $("#edit-broker-select").val(id_broker).change();
            $("#editTypePrecioAccionX").val(precio_accion)
            $("#editTypeNumeroAccionesX").val(numero_acciones)
            $("#editTypeComisionesCompraX").val(comision_compra)
            $("#editTypeOtrasComisionesX").val(otras_comisiones)

           $('#edit').modal('show')

        });
        $('.delete-element').on( "click", function() {
           delete_posicion_accion($(this).attr("data-element"))
        });


    });

    $('#search-button').on( "click", function() {
        table.ajax.reload(null, false);
    } );


    $('#add-button').on( "click", function() {
        $("#addFechaCompraDataPicker").val(moment().format("DD/MM/YYYY"));
        $("#addTypeISINX").val('');
        $("#add-bolsa-select").val('')
        $("#add-broker-select").val('')
        $("#addTypePrecioAccionX").val('');
        $("#addTypeNumeroAccionesX").val('');
        $("#addTypeComisionesCompraX").val('');
        $("#addTypeOtrasComisionesX").val('');

        $('#add').modal('show')
    } );

    $('#add-close-button').on( "click", function() {
        $('#add').modal('hide')
    });

    $('#add-submit-button').on( "click", function() {
       add_posicion_accion();
    });

    $('#edit-close-button').on( "click", function() {
        $('#edit').modal('hide')
    } );

    $('#edit-submit-button').on( "click", function() {
       update_posicion_accion()
    });

});

