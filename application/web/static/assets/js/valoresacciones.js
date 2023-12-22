function add_valor_accion() {
    var fecha = $("#addFechaDataPicker").val()
    var isin = $("#add-isin-select").val();
    var valor_accion = $("#addTypeValorAccionX").val();

    var data = {
        fecha: fecha,
        isin: isin,
        valor: parseFloat(valor_accion).toFixed(4) ? valor_accion : null,
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/valoraccion", true);
    xhttp.setRequestHeader("Content-Type", "application/json");

    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 201) {
                $('#add').modal('hide')
                reload_table();
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#addTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));

}

function delete_valor_accion(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/valoraccion/"+id, true);
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

get_daterangepicker_config = function(){
    return {
        timePicker: true,
        timePicker24Hour: true,
        singleDatePicker: true,
        autoApply: true,
        startDate: moment(),
        locale: {
          format: "DD/MM/YYYY HH:mm",
          applyLabel: "Aplicar",
          cancelLabel: "Cancelar",
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

function create_tabla_valores_acciones_meses(isins, callback){

    var today = new Date()
    var año_antes_today = new Date(today)
    año_antes_today.setFullYear(año_antes_today.getFullYear()-1)
    var end_date = today.getDate()+"/"+ (today.getMonth()+1) + "/" + today.getFullYear()
    var begin_date = "1/"+ (año_antes_today.getMonth()+1) + "/" + año_antes_today.getFullYear()

    $.get("finanzas/resumen/valores_acciones_meses?begin_fecha="+begin_date+"&end_fecha="+end_date, function(resultado) {
        var valores_acciones={}
        var labels = []
        var fecha_iterada = new Date(año_antes_today)

        for (var i=1;i<=13;i++){
            label = (fecha_iterada.getMonth()+1) + "/" + fecha_iterada.getFullYear()
            labels.push(label)
            for (var j in isins){
                valores_acciones[isins[j]] = {}
                valores_acciones[isins[j]][label] = 0
            }
            fecha_iterada.setMonth(fecha_iterada.getMonth()+1)
        }

        for (var i in resultado){
            label = resultado[i].mes+"/"+resultado[i].año
            try {
                valores_acciones[resultado[i].isin][label] = resultado[i].ultimo_valor
            } catch (error) {
                valores_acciones[resultado[i].isin] = {}
                valores_acciones[resultado[i].isin][label] = resultado[i].ultimo_valor
            }
        }


        var tr = $("#resumen-valores-acciones thead tr")
        tr.append($('<th></th>').text("valores-acciones"))
        for (var i in labels){
            tr.append($('<th></th>').text(labels[i]))
        }

        var tbody = $("#resumen-valores-acciones tbody")
        for (var isin in valores_acciones){
            var row = $('<tr></tr>')
            row.append($('<td></td>').text(isin))
            for (var j in labels){
                var value = "-"
                if (valores_acciones[isin][labels[j]] != undefined){
                    value = parseFloat(valores_acciones[isin][labels[j]]).toFixed(2)
                }
                row.append($('<td></td>').text(value))
            }
            tbody.append(row)
        }

        callback(labels)
    });

}

create_table = function(labels){
    var columns = [
            {
                data:'isin',
                type: "string"
            }]

        render_valor_accion = function (data, type, row, meta) {
            var number = get_local_number(data);
            var add_class = ""
            if (type === 'display') {
                if (meta.col > 0) {
                    before_colum_number = row[columns[meta.col-1].data]
                    if (data != "-" && before_colum_number != "-"){
                        data_float = parseFloat(data)
                        before_colum_number_float = parseFloat(before_colum_number)
                        if (data_float > before_colum_number_float){
                            add_class = "text-success "
                        } else if (data_float < before_colum_number_float){
                            add_class = "text-danger "
                        }
                    }
                }
                return "<span class='ms-2 font-weight-bold texto-resumen "+add_class+"'>"+number+"</span><span class='ms-2 font-weight-bold texto-resumen "+add_class+"'>€</span>"
            }
            return data
        }

        for (var i in labels){
            columns.push({
                    data: labels[i],
                    type: "num",
                    render: render_valor_accion
                }
            )
        }


        table = $("#resumen-valores-acciones").DataTable({
            columns: columns,
            order: [[0, 'asc']],
            info: false,
            lengthChange: false,
            paging: false,
            searching: false,
            scrollX: false,
            language: {
                info: 'Total _MAX_ Datos',
                infoEmpty: 'No hay Datos',
                zeroRecords: "No hay Datos",
                loadingRecords: "Cargando...",
                decimal:",",
            },
        });

}



reload_table = function() {

    table.destroy()
    var thead= $("#resumen-valores-acciones thead")
    thead.empty()
    thead.append($('<tr></tr>'))

    tbody= $("#resumen-valores-acciones tbody").empty()

    $.get("finanzas/posicionaccion/isin", function( data_isin ) {
        create_tabla_valores_acciones_meses(data_isin, function(labels) {
            create_table(labels);
        });
    });
}

$(document).ready(function() {

    $.get("finanzas/posicionaccion/isin", function( data_isin ) {
        create_tabla_valores_acciones_meses(data_isin, create_table);
    });

    $('#addFechaDataPicker').daterangepicker(get_daterangepicker_config());

    $('#add-button').on( "click", function() {
        $('#addFechaDataPicker').val(moment().format("DD/MM/YYYY HH:mm"));
        $("#add-isin-select").val('')
        $("#addTypeValorAccionX").val('')
        $("#addTypeMessageX").text('')
        $('#add').modal('show')
    } );

    $('#add-close-button').on( "click", function() {
        $('#add').modal('hide')
    });

    $('#add-submit-button').on( "click", function() {
       add_valor_accion();
    });


});


