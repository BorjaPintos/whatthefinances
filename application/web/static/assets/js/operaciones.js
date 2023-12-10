function add_operacion() {
    var fecha = $("#addFechaDataPicker").val()
    var descripcion = $("#addTypeDescripcionX").val();
    var cantidad = $("#addTypeCantidadX").val();

    tipo_opcion = $('#add-seleccion_tipo input:radio[name=add_tipo]:checked').attr('id')
   if (tipo_opcion == "add-tipo-gasto"){
    var id_categoria_ingreso = undefined;
    var id_cuenta_abono = undefined;
    var id_monedero_abono = undefined;
    var id_categoria_gasto = $("#add-gasto-categoria-gasto-select").val();
    var id_cuenta_cargo = $("#add-gasto-cuenta-cargo-select").val();
    var id_monedero_cargo = $("#add-gasto-monedero-cargo-select").val();
   }
   else if (tipo_opcion == "add-tipo-ingreso"){
    var id_categoria_ingreso = $("#add-ingreso-categoria-ingreso-select").val();
    var id_cuenta_abono = $("#add-ingreso-cuenta-abono-select").val();
    var id_monedero_abono = $("#add-ingreso-monedero-abono-select").val();
    var id_categoria_gasto = undefined;
    var id_cuenta_cargo = undefined;
    var id_monedero_cargo = undefined;
   }
   else if (tipo_opcion == "add-tipo-transferencia"){
    var id_categoria_ingreso = $("#add-transferencia-categoria-ingreso-select").val();
    var id_cuenta_abono = $("#add-transferencia-cuenta-abono-select").val();
    var id_monedero_abono = $("#add-transferencia-monedero-abono-select").val();
    var id_categoria_gasto = $("#add-transferencia-categoria-gasto-select").val();
    var id_cuenta_cargo = $("#add-transferencia-cuenta-cargo-select").val();
    var id_monedero_cargo = $("#add-transferencia-monedero-cargo-select").val();
   }

    var data = {
        fecha: fecha,
        descripcion: descripcion,
        cantidad: cantidad ? cantidad : null,
        id_categoria_gasto: parseInt(id_categoria_gasto) ? id_categoria_gasto : null,
        id_monedero_cargo: parseInt(id_monedero_cargo) ? id_monedero_cargo : null,
        id_cuenta_cargo: parseInt(id_cuenta_cargo) ? id_cuenta_cargo : null,
        id_categoria_ingreso: parseInt(id_categoria_ingreso) ? id_categoria_ingreso : null,
        id_monedero_abono: parseInt(id_monedero_abono) ? id_monedero_abono : null,
        id_cuenta_abono: parseInt(id_cuenta_abono) ? id_cuenta_abono : null
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/operacion", true);
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

function delete_operacion(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/operacion/"+id, true);
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

function update_operacion() {
    var id = $.trim($("#editTypeIdX").val())
    var fecha = $("#editFechaDataPicker").val()
    var descripcion = $("#editTypeDescripcionX").val();
    var cantidad = $("#editTypeCantidadX").val();

    tipo_opcion = $('#edit-seleccion_tipo input:radio[name=edit_tipo]:checked').attr('id')
   if (tipo_opcion == "edit-tipo-gasto"){
    var id_categoria_ingreso = undefined;
    var id_cuenta_abono = undefined;
    var id_monedero_abono = undefined;
    var id_categoria_gasto = $("#edit-gasto-categoria-gasto-select").val();
    var id_cuenta_cargo = $("#edit-gasto-cuenta-cargo-select").val();
    var id_monedero_cargo = $("#edit-gasto-monedero-cargo-select").val();
   }
   else if (tipo_opcion == "edit-tipo-ingreso"){
    var id_categoria_ingreso = $("#edit-ingreso-categoria-ingreso-select").val();
    var id_cuenta_abono = $("#edit-ingreso-cuenta-abono-select").val();
    var id_monedero_abono = $("#edit-ingreso-monedero-abono-select").val();
    var id_categoria_gasto = undefined;
    var id_cuenta_cargo = undefined;
    var id_monedero_cargo = undefined;
   }
   else if (tipo_opcion == "edit-tipo-transferencia"){
    var id_categoria_ingreso = $("#edit-transferencia-categoria-ingreso-select").val();
    var id_cuenta_abono = $("#edit-transferencia-cuenta-abono-select").val();
    var id_monedero_abono = $("#edit-transferencia-monedero-abono-select").val();
    var id_categoria_gasto = $("#edit-transferencia-categoria-gasto-select").val();
    var id_cuenta_cargo = $("#edit-transferencia-cuenta-cargo-select").val();
    var id_monedero_cargo = $("#edit-transferencia-monedero-cargo-select").val();
   }

   var data = {
        fecha: fecha,
        descripcion: descripcion,
        cantidad: cantidad ? cantidad : null,
        id_categoria_gasto: parseInt(id_categoria_gasto) ? id_categoria_gasto : null,
        id_monedero_cargo: parseInt(id_monedero_cargo) ? id_monedero_cargo : null,
        id_cuenta_cargo: parseInt(id_cuenta_cargo) ? id_cuenta_cargo : null,
        id_categoria_ingreso: parseInt(id_categoria_ingreso) ? id_categoria_ingreso : null,
        id_monedero_abono: parseInt(id_monedero_abono) ? id_monedero_abono : null,
        id_cuenta_abono: parseInt(id_cuenta_abono) ? id_cuenta_abono : null
   }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/operacion/"+id, true);
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

render_nombre_cuenta_abono = function (data, type, row) {
    var new_data = data
    if (data == undefined)
        if ((row.id_categoria_ingreso != undefined) &&  (row.id_categoria_gasto==undefined))
            new_data = "Todas"
        else
            new_data = "-"
    if (type === 'display'){
        return '<span class="badge custom-badge">'+new_data+'</span>'
    }
    return new_data
}

render_nombre_cuenta_cargo = function (data, type, row) {
    var new_data = data
    if (data == undefined)
        if ((row.id_categoria_gasto != undefined) &&  (row.id_categoria_ingreso==undefined))
            new_data = "Todas"
        else
            new_data = "-"
    if (type === 'display'){
        return '<span class="badge custom-badge">'+new_data+'</span>'
    }
    return new_data
}

render_nombre = function (data, type) {
    var new_data = data
    if (data == undefined)
        new_data = "-"
    if (type === 'display'){
        return '<span class="badge custom-badge">'+new_data+'</span>'
    }
    return new_data
}

render_texto = function(data, type){

    if (type == 'display'){
        if (data.length>75)
            return '<span class="badge custom-badge" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="'+data+'">'+  (data.substring(0, 75) + "...") +'</span>'
        else
          return '<span class="badge custom-badge">'+ data +'</span>'

    }
    return data
}

$(document).ready(function() {
    $('#addFechaDataPicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'es-ES'
    });
    $('#editFechaDataPicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'es-ES'
    });
     $('#search-fecha-begin-datapicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'es-ES'
    });
    $('#search-fecha-end-datapicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'es-ES'
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
                if (json.elements[i].id_categoria_ingreso != undefined && json.elements[i].id_categoria_gasto != undefined)
                    json.elements[i].DT_RowClass = "transferencia"
                else if (json.elements[i].id_categoria_ingreso != undefined)
                    json.elements[i].DT_RowClass = "ingreso"
                else
                    json.elements[i].DT_RowClass = "gasto"
            }
            json.recordsTotal = json.total_elements
            json.recordsFiltered = json.total_elements
         })
        .DataTable({
        dom: '<flrt<"#table_fotter"ip>',
        serverSide:true,
        ajax: {
            url:'/finanzas/operacion',
            data: function (d) {
                var begin_fecha = $('#search-fecha-begin-datapicker').val()
                var end_fecha = $('#search-fecha-end-datapicker').val()
                var id_categoria_ingreso = $("#search-categoria-ingreso-select").val();
                var id_categoria_gasto = $("#search-categoria-gasto-select").val();
                var id_cuenta_cargo = $("#search-cuenta-cargo-select").val();
                var id_monedero_cargo = $("#search-monedero-cargo-select").val();
                var id_cuenta_abono = $("#search-cuenta-abono-select").val();
                var id_monedero_abono = $("#search-monedero-abono-select").val();

                if (begin_fecha != '')
                    d.begin_fecha = begin_fecha
                if (end_fecha != '')
                    d.end_fecha = end_fecha
                if (id_categoria_gasto != '')
                    d.id_categoria_gasto = id_categoria_gasto
                if (id_categoria_ingreso != '')
                    d.id_categoria_ingreso = id_categoria_ingreso
                if (id_cuenta_cargo != '')
                    d.id_cuenta_cargo = id_cuenta_cargo
                if (id_monedero_cargo != '')
                    d.id_monedero_cargo = id_monedero_cargo
                if (id_cuenta_abono != '')
                    d.id_cuenta_abono = id_cuenta_abono
                if (id_monedero_abono != '')
                    d.id_monedero_abono = id_monedero_abono

            },
            dataSrc: 'elements',
        },
        columns: [
            {
                data:'fecha',
                type: "string",
                render: render_texto,
                width: "5%"
            },
            {
                data:'cantidad',
                type: "num",
                render: render_dinero,
                width: "12%"
            },
            {
                data:'descripcion',
                type: "string",
                render: render_texto,
                orderSequence:[],
                width: "13%"
            },
            {
                data:'descripcion_categoria_gasto',
                render: render_nombre,
                type: "string",
                orderSequence:[],
                width: "10%"
            },
            {
                data:'descripcion_categoria_ingreso',
                render: render_nombre,
                type: "string",
                orderSequence:[],
                width: "10%"
            },
            {
                data:'nombre_cuenta_cargo',
                render: render_nombre_cuenta_cargo,
                type: "string",
                orderSequence:[],
                width: "10%"
            },
            {
                data:'nombre_cuenta_abono',
                render: render_nombre_cuenta_abono,
                type: "string",
                orderSequence:[],
                width: "10%"
            },
            {
                data:'nombre_monedero_cargo',
                render: render_nombre,
                type: "string",
                orderSequence:[],
                width: "10%"
            },
            {
                data:'nombre_monedero_abono',
                render: render_nombre,
                type: "string",
                orderSequence:[],
                width: "10%"
            },
            {
                className: 'text-end',
                data:'id',
                render: render_actions,
                type: "num",
                orderSequence:[],
                width: "10%"
            }
        ],
        order: [[0, 'desc']],
        info: true,
        lengthChange: false,
        paging: true,
        pageLength: 30,
        searching: false,
        scrollX: false,
        language: {
            info: 'Total _MAX_ Operaciones',
            infoEmpty: 'No hay Operaciones',
            zeroRecords: "No hay Operaciones",
            loadingRecords: "Cargando...",
            decimal:",",
        }
    });


    table.on('draw', function () {
        activar_elements();

        $('.edit-element').on( "click", function() {

            var operacion = table.row($(this).parents('tr')).data()
            var id = operacion.id
            var fecha = operacion.fecha
            var descripcion = operacion.descripcion;
            var cantidad = get_local_number(operacion.cantidad)

            var id_cuenta_cargo=operacion.id_cuenta_cargo
            var id_monedero_cargo= operacion.id_monedero_cargo
            var id_categoria_gasto=operacion.id_categoria_gasto
            var id_cuenta_abono= operacion.id_cuenta_abono
            var id_monedero_abono=operacion.id_monedero_abono
            var id_categoria_ingreso= operacion.id_categoria_ingreso


            $("#editTypeIdX").val(id)
            $('#editFechaDataPicker').datepicker('update',  fecha);
            $("#editTypeDescripcionX").val(descripcion)
            $("#editTypeCantidadX").val(cantidad)


           var div_gasto = $("#edit-div-gasto")
           var div_ingreso = $("#edit-div-ingreso")
           var div_transferencia = $("#edit-div-transferencia")
           var radio_transferencia = $("#edit-tipo-transferencia")
           var radio_gasto = $("#edit-tipo-gasto")
           var radio_ingreso = $("#edit-tipo-ingreso")

           div_gasto.collapse('hide');
           div_ingreso.collapse('hide');
           div_transferencia.collapse('hide');
           radio_transferencia.prop("checked", false)
           radio_gasto.prop("checked", false)
           radio_ingreso.prop("checked", false)


           if ((id_categoria_gasto) && (id_categoria_ingreso)){
                $("#edit-transferencia-categoria-ingreso-select").val(id_categoria_ingreso).change();
                $("#edit-transferencia-cuenta-abono-select").val(id_cuenta_abono).change();
                $("#edit-transferencia-monedero-abono-select").val(id_monedero_abono).change();
                $("#edit-transferencia-categoria-gasto-select").val(id_categoria_gasto).change();
                $("#edit-transferencia-cuenta-cargo-select").val(id_cuenta_cargo).change();
                $("#edit-transferencia-monedero-cargo-select").val(id_monedero_cargo).change();
                radio_transferencia.prop("checked", true)
                div_transferencia.collapse('show');

           } else if (id_categoria_gasto){
                $("#edit-gasto-categoria-gasto-select").val(id_categoria_gasto).change();
                $("#edit-gasto-cuenta-cargo-select").val(id_cuenta_cargo).change();
                $("#edit-gasto-monedero-cargo-select").val(id_monedero_cargo).change();
                radio_gasto.prop("checked", true)
                div_gasto.collapse('show');

           } else if(id_categoria_ingreso){
                $("#edit-ingreso-categoria-ingreso-select").val(id_categoria_ingreso).change();
                $("#edit-ingreso-cuenta-abono-select").val(id_cuenta_abono).change();
                $("#edit-ingreso-monedero-abono-select").val(id_monedero_abono).change();
                radio_ingreso.prop("checked", true)
                div_ingreso.collapse('show');

           }

           $('#edit').modal('show')

        });
        $('.delete-element').on( "click", function() {
           delete_operacion($(this).attr("data-element"))
        });


    });

    $('#search-button').on( "click", function() {
        table.ajax.reload(null, false);
    } );


    $('#add-button').on( "click", function() {
        $("#addTypeNombreX").val('')
        $("#addTypeCantidadInicialX").val('')
        $("#addTypePonderacionX").val('')
        $("#addTypeMessageX").text('')
        $('#addFechaDataPicker').datepicker('update',  new Date());
        $("#add-div-gasto").collapse('show');
        $("#add-div-ingreso").collapse('hide');
        $("#add-div-transferencia").collapse('hide');
        $('#add').modal('show')
    } );

    $('#add-close-button').on( "click", function() {
        $('#add').modal('hide')
    });

    $('#add-submit-button').on( "click", function() {
       add_operacion();
    });

    $('#edit-close-button').on( "click", function() {
        $('#edit').modal('hide')
    } );

    $('#edit-submit-button').on( "click", function() {
       update_operacion()
    });


    $('#add-ingreso-categoria-ingreso-select').on("change", function() {
       var option = $('#add-ingreso-categoria-ingreso-select option:selected')
       var id_cuenta = option.attr("data-id-cuenta-defecto")
       var id_monedero = option.attr("data-id-monedero-defecto")

       $("#add-ingreso-cuenta-abono-select").val(id_cuenta).change();
       $("#add-ingreso-monedero-abono-select").val(id_monedero).change();
    });

    $('#add-gasto-categoria-gasto-select').on("change", function() {
       var option = $('#add-gasto-categoria-gasto-select option:selected')
       var id_cuenta = option.attr("data-id-cuenta-defecto")

       var id_monedero = option.attr("data-id-monedero-defecto")
       $("#add-gasto-cuenta-cargo-select").val(id_cuenta).change();
       $("#add-gasto-monedero-cargo-select").val(id_monedero).change();
    });

    $('#add-transferencia-categoria-ingreso-select').on("change", function() {
       var option = $('#add-transferencia-categoria-ingreso-select option:selected')
       var id_cuenta = option.attr("data-id-cuenta-defecto")
       var id_monedero = option.attr("data-id-monedero-defecto")

       $("#add-transferencia-cuenta-abono-select").val(id_cuenta).change();
       $("#add-transferencia-monedero-abono-select").val(id_monedero).change();
    });

    $('#add-transferencia-categoria-gasto-select').on("change", function() {
       var option = $('#add-transferencia-categoria-gasto-select option:selected')
       var id_cuenta = option.attr("data-id-cuenta-defecto")

       id_monedero = option.attr("data-id-monedero-defecto")
       $("#add-transferencia-cuenta-cargo-select").val(id_cuenta).change();
       $("#add-transferencia-monedero-cargo-select").val(id_monedero).change();
    });

    $('#edit-ingreso-categoria-ingreso-select').on("change", function() {
       var option = $('#edit-ingreso-categoria-ingreso-select option:selected')
       var id_cuenta = option.attr("data-id-cuenta-defecto")
       var id_monedero = option.attr("data-id-monedero-defecto")

       $("#edit-ingreso-cuenta-abono-select").val(id_cuenta).change();
       $("#edit-ingreso-monedero-abono-select").val(id_monedero).change();
    });

    $('#edit-gasto-categoria-gasto-select').on("change", function() {
       var option = $('#edit-gasto-categoria-gasto-select option:selected')
       var id_cuenta = option.attr("data-id-cuenta-defecto")

       var id_monedero = option.attr("data-id-monedero-defecto")
       $("#edit-gasto-cuenta-cargo-select").val(id_cuenta).change();
       $("#edit-gasto-monedero-cargo-select").val(id_monedero).change();
    });

    $('#edit-transferencia-categoria-ingreso-select').on("change", function() {
       var option = $('#edit-transferencia-categoria-ingreso-select option:selected')
       var id_cuenta = option.attr("data-id-cuenta-defecto")
       var id_monedero = option.attr("data-id-monedero-defecto")

       $("#edit-transferencia-cuenta-abono-select").val(id_cuenta).change();
       $("#edit-transferencia-monedero-abono-select").val(id_monedero).change();
    });

    $('#edit-transferencia-categoria-gasto-select').on("change", function() {
       var option = $('#edit-transferencia-categoria-gasto-select option:selected')
       var id_cuenta = option.attr("data-id-cuenta-defecto")

       id_monedero = option.attr("data-id-monedero-defecto")
       $("#edit-transferencia-cuenta-cargo-select").val(id_cuenta).change();
       $("#edit-transferencia-monedero-cargo-select").val(id_monedero).change();
    });

    $('#add-seleccion_tipo input:radio[name=add_tipo]').on('change', function() {
       var tipo_opcion = $('#add-seleccion_tipo input:radio[name=add_tipo]:checked').attr('id')
       var div_gasto = $("#add-div-gasto")
       var div_ingreso = $("#add-div-ingreso")
       var div_transferencia = $("#add-div-transferencia")
       if (tipo_opcion == "add-tipo-gasto"){
            div_gasto.collapse('show');
            div_ingreso.collapse('hide');
            div_transferencia.collapse('hide');
       }
       else if (tipo_opcion == "add-tipo-ingreso"){
            div_gasto.collapse('hide');
            div_ingreso.collapse('show');
            div_transferencia.collapse('hide');
       }
       else if (tipo_opcion == "add-tipo-transferencia"){
            div_gasto.collapse('hide');
            div_ingreso.collapse('hide');
            div_transferencia.collapse('show');
       }
    });

    $('#edit-seleccion_tipo input:radio[name=edit_tipo]').on('change', function() {
       var tipo_opcion = $('#edit-seleccion_tipo input:radio[name=edit_tipo]:checked').attr('id')
       var div_gasto = $("#edit-div-gasto")
       var div_ingreso=$("#edit-div-ingreso")
       var div_transferencia=$("#edit-div-transferencia")
       if (tipo_opcion == "edit-tipo-gasto"){
            div_gasto.collapse('show');
            div_ingreso.collapse('hide');
            div_transferencia.collapse('hide');
       }
       else if (tipo_opcion == "edit-tipo-ingreso"){
            div_gasto.collapse('hide');
            div_ingreso.collapse('show');
            div_transferencia.collapse('hide');
       }
       else if (tipo_opcion == "edit-tipo-transferencia"){
            div_gasto.collapse('hide');
            div_ingreso.collapse('hide');
            div_transferencia.collapse('show');
       }
    });
});

