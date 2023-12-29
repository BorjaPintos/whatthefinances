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
        return "<span class='ms-2 font-weight-bold texto-resumen "+add_class+"'>"+number+"</span><span class='ms-2 font-weight-bold texto-resumen "+add_class+"'>€</span>"
    }
    return data
}

function create_tabla_cosas_concreta(data_entidades_totales, end_point, resumen, entidad, id_entidad){

    var today = new Date()
    var año_antes_today = new Date(today)
    año_antes_today.setFullYear(año_antes_today.getFullYear()-1)
    var end_date = today.getDate()+"/"+ (today.getMonth()+1) + "/" + today.getFullYear()
    var begin_date = "1/"+ (año_antes_today.getMonth()+1) + "/" + año_antes_today.getFullYear()

    $.get("finanzas/resumen/"+end_point+"?begin_fecha="+begin_date+"&end_fecha="+end_date, function( resultado ) {
        var cosas={}
        var cosa_total_resumen = {}
        for (var i in data_entidades_totales){
            cosas[data_entidades_totales[i].id]={}
            cosas[data_entidades_totales[i].id].nombre= data_entidades_totales[i].nombre
            cosas[data_entidades_totales[i].id].total=0
        }
        var labels = []
        var fecha_iterada = new Date(año_antes_today)
        for (var i=1;i<=12;i++){
            label = (fecha_iterada.getMonth()+1) + "/" + fecha_iterada.getFullYear()
            console.log(label);
            labels.push(label)
            for (var j in data_entidades_totales){
                cosas[data_entidades_totales[j].id][label] = 0
            }
            cosa_total_resumen[label]=0
            fecha_iterada.setMonth(fecha_iterada.getMonth()+1)
        }

        for (var i in resultado){
            label = resultado[i].mes+"/"+resultado[i].año
            cosas[resultado[i][id_entidad]][label] = resultado[i].total
            cosas[resultado[i][id_entidad]].total += resultado[i].total
        }

        var tr = $("#resumen-"+entidad+"-"+resumen+" thead tr")
        tr.append($('<th></th>').text("tipo_row"))
        tr.append($('<th></th>').text(resumen))
        for (var i in labels){
            tr.append($('<th></th>').text(labels[i]))
        }
        tr.append($('<th></th>').text("Total"))

        var tbody = $("#resumen-"+entidad+"-"+resumen+" tbody")
        for (var i in cosas){
            var row = $('<tr></tr>')
            row.addClass("resumen-"+resumen)
            row.append($('<td></td>').text("dato"))
            row.append($('<td></td>').text(cosas[i].nombre))
            for (var j in labels){
                var value = parseFloat(cosas[i][labels[j]]).toFixed(2)
                cosa_total_resumen[labels[j]]+=cosas[i][labels[j]];
                row.append($('<td></td>').text(value))
            }
            row.append($('<td></td>').text(parseFloat(cosas[i].total).toFixed(2)))
            tbody.append(row)
        }
        var row = $('<tr></tr>')
        row.addClass("resumen-"+resumen)
        row.append($('<td></td>').text("Resumen"))
        row.append($('<td></td>').text("Total"))
        var total_totales = 0
        for (var j in labels){
            var value = cosa_total_resumen[labels[j]]
            row.append($('<td></td>').text(parseFloat(value).toFixed(2)))
            total_totales += value
        }
        row.append($('<td></td>').text(parseFloat(total_totales).toFixed(2)))
        tbody.append(row)


        var columns = [
            {
                data:'tipo_row',
                type: "string",
                visible:false
            },
            {
                data:'nombre',
                type: "string"
            }]
        for (var i in labels){
            columns.push({
                    data:labels[i],
                    type: "num",
                    render: render_dinero
                }
            )
        }
        columns.push({
                    data:"total",
                    type: "num",
                    render: render_dinero
                }
            )

        var table = $("#resumen-"+entidad+"-"+resumen).DataTable({
            columns: columns,
            rowGroup: {
                dataSrc: "tipo_row"
            },
            orderFixed: [0, 'asc'],
            order: [[1, 'asc']],
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
             initComplete: function(settings, json) {
                $('.dtrg-group').remove();
             }
        })
        table.on( 'draw', function () {
            $('.dtrg-group').remove();
        });
    });

}