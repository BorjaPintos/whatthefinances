get_local_number = function(num){
    return $.fn.dataTable.render.number('', ',', 2).display(num);
}

function create_tabla_posiciones_meses(data_productos, callback){

    var today = new Date()
    var año_antes_today = new Date(today)
    año_antes_today.setFullYear(año_antes_today.getFullYear()-1)
    var end_date = today.getDate()+"/"+ (today.getMonth()+1) + "/" + today.getFullYear()
    var begin_date = "1/"+ (año_antes_today.getMonth()+1) + "/" + año_antes_today.getFullYear()

    $.get("finanzas/resumen/posiciones_meses?begin_fecha="+begin_date+"&end_fecha="+end_date, function(resultado) {
        var valores_posiciones={}
        var labels = []
        var fecha_iterada = new Date(año_antes_today)
        var total_month = {}

        for (var i=1;i<=13;i++){
            var label = (fecha_iterada.getMonth()+1) + "/" + fecha_iterada.getFullYear()
            labels.push(label)
            fecha_iterada.setMonth(fecha_iterada.getMonth()+1)
        }
        for (var j in data_productos){
                valores_posiciones[data_productos[j].isin] = {}
                valores_posiciones[data_productos[j].isin]["nombre"] = data_productos[j].nombre + ' - ' + data_productos[j].isin
        }
        for (var i in resultado){
            var label = resultado[i].mes+"/"+resultado[i].año
            try {
                valores_posiciones[resultado[i].isin][label] = resultado[i].valor * resultado[i].suma_participaciones
            } catch (error) {
                valores_posiciones[resultado[i].isin] = {}
                valores_posiciones[resultado[i].isin][label] = resultado[i].valor * resultado[i].suma_participaciones
            }
        }

        var tr = $("#resumen-posiciones thead tr")
        tr.append($('<th></th>').text("Valores de tus posiciones"))
        for (var i in labels){
            tr.append($('<th></th>').text(labels[i]))
            total_month[labels[i]] = 0
        }

        var tbody = $("#resumen-posiciones tbody")

        for (var valores_posicion in valores_posiciones){
            var row = $('<tr></tr>')
            row.append($('<td></td>').text(valores_posiciones[valores_posicion].nombre))
            for (var j in labels){
                var value = "-"
                if (valores_posiciones[valores_posicion][labels[j]] != undefined){
                    value = parseFloat(valores_posiciones[valores_posicion][labels[j]]).toFixed(2)
                    total_month[labels[j]] += valores_posiciones[valores_posicion][labels[j]]
                }
                row.append($('<td></td>').text(value))
            }
            tbody.append(row)
        }

        var row = $('<tr></tr>')
        row.append($('<td></td>').text("Total"))
        for (var j in labels){
            var value = total_month[labels[j]]
            row.append($('<td></td>').text(parseFloat(value).toFixed(2)))
        }
        tbody.append(row)
        callback(labels, "#resumen-posiciones")
    });
}

function create_tabla_posiciones_meses_acumuladas(data_productos, callback){

    var today = new Date()
    var año_antes_today = new Date(today)
    año_antes_today.setFullYear(año_antes_today.getFullYear()-1)

    $.get("finanzas/resumen/posiciones_meses_acumuladas", function(resultado) {
        var valores_posiciones={}
        var labels = []
        var fecha_iterada = new Date(año_antes_today)
        var total_month = {}

        for (var i=1;i<=13;i++){
            var label = (fecha_iterada.getMonth()+1) + "/" + fecha_iterada.getFullYear()
            labels.push(label)
            fecha_iterada.setMonth(fecha_iterada.getMonth()+1)
        }
        for (var j in data_productos){
                valores_posiciones[data_productos[j].isin] = {}
                valores_posiciones[data_productos[j].isin]["nombre"] = data_productos[j].nombre + ' - ' + data_productos[j].isin
        }
        var last_value = {}
        var begin_label = labels[0].split("/").reverse().join("/")
        for (var i in resultado){
            var label = resultado[i].mes+"/"+resultado[i].año
            var label_comparition = label.split("/").reverse().join("/")
            try {
                valores_posiciones[resultado[i].isin][label] = resultado[i].precio_compra_acumulado
            } catch (error) {
                valores_posiciones[resultado[i].isin] = {}
                valores_posiciones[resultado[i].isin][label] = resultado[i].precio_compra_acumulado
            }
            if ((label_comparition < begin_label) && (last_value[resultado[i].isin] === undefined)) {
                last_value[resultado[i].isin] = resultado[i].precio_compra_acumulado
            }
        }


        var tr = $("#resumen-posiciones-acumulada thead tr")
        tr.append($('<th></th>').text("Inversiones mensuales acumuladas"))
        for (var i in labels){
            tr.append($('<th></th>').text(labels[i]))
            total_month[labels[i]] = 0.0
        }


        var tbody = $("#resumen-posiciones-acumulada tbody")

        for (var valores_posicion in valores_posiciones){
            var row = $('<tr></tr>')
            row.append($('<td></td>').text(valores_posiciones[valores_posicion].nombre))
            for (var j in labels){
                var value = "-"
                if (valores_posiciones[valores_posicion][labels[j]] != undefined){
                    value = valores_posiciones[valores_posicion][labels[j]]
                    last_value[valores_posicion] = value
                    total_month[labels[j]] += value
                } else {
                    if (last_value[valores_posicion] != undefined){
                        value = last_value[valores_posicion]
                        total_month[labels[j]] += value
                    }
                }
                row.append($('<td></td>').text(value))
            }
            tbody.append(row)
        }

        var row = $('<tr></tr>')
        row.append($('<td></td>').text("Total"))
        for (var j in labels){
            var value = total_month[labels[j]]
            row.append($('<td></td>').text(parseFloat(value).toFixed(2)))
        }
        tbody.append(row)
        callback(labels, "#resumen-posiciones-acumulada")
    });
}

create_table = function(labels, id_table){
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

    render_valor = function (data, type, row, meta) {
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
                render: render_valor
            }
        )
    }
    var table = $(id_table)
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
    return table
}


create_table_ganancias = function(labels, table_pocisiones_meses, table_posiciones_meses_acumulada, callback){
    data_posiciones_meses = table_pocisiones_meses.data()
    data_posiciones_meses_acumulada = table_posiciones_meses_acumulada.data()
    dataset = []
    var total_month = {}
    for (let i = 0; i < table_pocisiones_meses.data().length-1; i++) {
        element = {}
        element["nombre"]=data_posiciones_meses[i]["nombre"]
        for (j in labels){
            month_label = labels[j]
            resta = parseFloat(data_posiciones_meses[i][month_label])-parseFloat(data_posiciones_meses_acumulada[i][month_label])
            if (!Number.isNaN(resta)) {
                 element[month_label] = resta
            }
        }
        dataset.push(element)
    }

    var tr = $("#resumen-ganancias-acumulada thead tr")
        tr.append($('<th></th>').text("Ganancias mensuales acumuladas"))
        for (var i in labels){
            tr.append($('<th></th>').text(labels[i]))
            total_month[labels[i]] = 0.0
        }

        var tbody = $("#resumen-ganancias-acumulada tbody")

        for (var i in dataset){
            var row = $('<tr></tr>')
            row.append($('<td></td>').text(dataset[i].nombre))
            for (var j in labels){
                var value = "-"
                if (dataset[i][labels[j]] != undefined){
                    value = dataset[i][labels[j]]
                    total_month[labels[j]] += value
                }
                row.append($('<td></td>').text(value))
            }
            tbody.append(row)
        }

        var row = $('<tr></tr>')
        row.append($('<td></td>').text("Total"))
        for (var j in labels){
            var value = total_month[labels[j]]
            row.append($('<td></td>').text(parseFloat(value).toFixed(2)))
        }
        tbody.append(row)
        callback(labels, "#resumen-ganancias-acumulada")

}

$(document).ready(function() {

    $.get("finanzas/producto", function( data_productos ) {
        create_tabla_posiciones_meses(data_productos, function(labels, id){
             var table_posiciones_meses = create_table(labels, id)
             create_tabla_posiciones_meses_acumuladas(data_productos, function(labels2, id2){
                var table_posiciones_meses_acumulada = create_table(labels2, id2)
                create_table_ganancias(labels, table_posiciones_meses, table_posiciones_meses_acumulada, create_table)
             });
        });
    });
});


