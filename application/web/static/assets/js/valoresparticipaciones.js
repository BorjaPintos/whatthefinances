function add_valor_participacion() {
    var fecha = $("#addFechaDataPicker").val()
    var isin = $("#add-isin-select").val();
    var valor_participacion = $("#addTypeValorParticipacionX").val();

    var data = {
        fecha: fecha,
        isin: isin,
        valor: parseFloat(valor_participacion).toFixed(4) ? valor_participacion : null,
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/valorparticipacion", true);
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

function delete_valor_participacion(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/valorparticipacion/"+id, true);
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

function create_tabla_valores_participaciones_meses(data_productos, callback){

    var today = new Date()
    var año_antes_today = new Date(today)
    año_antes_today.setFullYear(año_antes_today.getFullYear()-1)
    var end_date = today.getDate()+"/"+ (today.getMonth()+1) + "/" + today.getFullYear()
    var begin_date = "1/"+ (año_antes_today.getMonth()+1) + "/" + año_antes_today.getFullYear()

    $.get("finanzas/resumen/valores_participaciones_meses?begin_fecha="+begin_date+"&end_fecha="+end_date, function(resultado) {
        var valores_participaciones={}
        var labels = []
        var fecha_iterada = new Date(año_antes_today)

        for (var i=1;i<=13;i++){
            label = (fecha_iterada.getMonth()+1) + "/" + fecha_iterada.getFullYear()
            labels.push(label)
            for (var j in data_productos){
                valores_participaciones[data_productos[j].isin] = {}
                valores_participaciones[data_productos[j].isin]["nombre"] = data_productos[j].nombre + ' - ' + data_productos[j].isin
                valores_participaciones[data_productos[j].isin][label] = 0
            }
            fecha_iterada.setMonth(fecha_iterada.getMonth()+1)
        }

        for (var i in resultado){
            label = resultado[i].mes+"/"+resultado[i].año
            try {
                valores_participaciones[resultado[i].isin][label] = resultado[i].ultimo_valor
            } catch (error) {
                valores_participaciones[resultado[i].isin] = {}
                valores_participaciones[resultado[i].isin][label] = resultado[i].ultimo_valor
            }
        }


        var tr = $("#resumen-valores-participaciones thead tr")
        tr.append($('<th></th>').text("valores-participaciones"))
        for (var i in labels){
            tr.append($('<th></th>').text(labels[i]))
        }

        var tbody = $("#resumen-valores-participaciones tbody")
        for (var valor_participacion in valores_participaciones){
            var row = $('<tr></tr>')
            row.append($('<td></td>').text(valores_participaciones[valor_participacion].nombre))
            for (var j in labels){
                var value = "-"
                if (valores_participaciones[valor_participacion][labels[j]] != undefined){
                    value = parseFloat(valores_participaciones[valor_participacion][labels[j]]).toFixed(2)
                }
                row.append($('<td></td>').text(value))
            }
            tbody.append(row)
        }

        callback(labels)
    });

}

create_table = function(labels){

    render_nombre = function(data, type, row){

        if (type == 'display'){
            if (data.length>15)
                return '<span class="badge custom-badge" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="'+data+'">'+  (data.substring(0, 15) + "...") +'</span>'
            else
                return '<span class="badge custom-badge" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="'+data+'">'+  data +'</span>'
        }
        return data
    }

    var columns = [
            {
                data:'nombre',
                type: "string",
                render: render_nombre
            }]

        render_valor_participacion = function (data, type, row, meta) {
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
                    render: render_valor_participacion
                }
            )
        }


        table = $("#resumen-valores-participaciones")
            .on('init.dt', function () {
                activar_elements();
            }).DataTable({
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
    var thead= $("#resumen-valores-participaciones thead")
    thead.empty()
    thead.append($('<tr></tr>'))

    tbody= $("#resumen-valores-participaciones tbody").empty()

    $.get("finanzas/producto", function( data_isin ) {
        create_tabla_valores_participaciones_meses(data_isin, function(labels) {
            create_table(labels);
        });
    });
}

$(document).ready(function() {

    $.get("finanzas/producto", function( data_productos ) {
        create_tabla_valores_participaciones_meses(data_productos, create_table);
    });

    $('#addFechaDataPicker').daterangepicker(get_daterangepicker_config());

    $('#add-button').on( "click", function() {
        $('#addFechaDataPicker').val(moment().format("DD/MM/YYYY HH:mm"));
        $("#add-isin-select").val('')
        $("#addTypeValorParticipacionX").val('')
        $("#addTypeMessageX").text('')
        $('#add').modal('show')
    } );

    $('#add-close-button').on( "click", function() {
        $('#add').modal('hide')
    });

    $('#add-submit-button').on( "click", function() {
       add_valor_participacion();
    });

    $('#auto-add-button').on( "click", function() {
        var xhttp = new XMLHttpRequest();

        xhttp.open("POST", "/finanzas/valorparticipacion/auto", true);
        xhttp.setRequestHeader("Content-Type", "application/json");

        xhttp.onreadystatechange = function () {
            if (xhttp.readyState === 4)
                if (xhttp.status === 200) {
                    reload_table();
                }
        };
        xhttp.send();
        } );
});


