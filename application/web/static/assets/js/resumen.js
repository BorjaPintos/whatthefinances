$(document).ready(function() {
    get_line_ahorros_gastos_ingresos_bar();
    get_tabla_cuentas();
    get_tabla_monederos();
});

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

function create_tabla_cosas_concreta(data_entidades_totales, resumen, entidad, id_entidad){

    var today = new Date()
    var año_antes_today = new Date(today)
    año_antes_today.setFullYear(año_antes_today.getFullYear()-1)
    var end_date = today.getDate()+"/"+ (today.getMonth()+1) + "/" + today.getFullYear()
    var begin_date = "1/"+ (año_antes_today.getMonth()+1) + "/" + año_antes_today.getFullYear()

    $.get("finanzas/resumen/"+entidad+"-"+resumen+"?begin_fecha="+begin_date+"&end_fecha="+end_date, function( resultado ) {
            var cosas={}
            var cosa_total_resumen = {}
            for (var i in data_entidades_totales){
                cosas[data_entidades_totales[i].id]={}
                cosas[data_entidades_totales[i].id].nombre= data_entidades_totales[i].nombre
                cosas[data_entidades_totales[i].id].total=0
            }
            var labels = []
            var fecha_iterada = new Date(año_antes_today)
            for (var i=1;i<=13;i++){
                label = (fecha_iterada.getMonth()+1) + "/" + fecha_iterada.getFullYear()
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

            tr.append($('<th></th>').text(entidad))
            for (var i in labels){
                tr.append($('<th></th>').text(labels[i]))
            }
            tr.append($('<th></th>').text("Total"))


            var tbody = $("#resumen-"+entidad+"-"+resumen+" tbody")
            for (var i in cosas){
                var row = $('<tr></tr>')
                row.addClass("resumen-"+resumen)
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
            row.append($('<td></td>').text("Total"))
            var total_totales = 0
            for (var j in labels){
                var value = cosa_total_resumen[labels[j]]
                row.append($('<td></td>').text(parseFloat(value).toFixed(2)))
                total_totales += value
            }
            row.append($('<td></td>').text(parseFloat(total_totales).toFixed(2)))
            tbody.append(row)


            var columns = [{
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
                }
            })
        });

}

function get_tabla_cuentas(){

    $.get("finanzas/cuenta?order_property=id&order_type=asc", function( data_cuentas ) {
        create_tabla_cosas_concreta(data_cuentas, "total", "cuentas", "id_cuenta");
        create_tabla_cosas_concreta(data_cuentas, "ingreso", "cuentas", "id_cuenta");
        create_tabla_cosas_concreta(data_cuentas, "gasto", "cuentas", "id_cuenta");
    });
}

function get_tabla_monederos(){

    $.get("finanzas/monedero?order_property=id&order_type=asc", function( data_monederos ) {
        create_tabla_cosas_concreta(data_monederos, "total", "monederos", "id_monedero");
        create_tabla_cosas_concreta(data_monederos, "ingreso", "monederos", "id_monedero");
        create_tabla_cosas_concreta(data_monederos, "gasto", "monederos", "id_monedero");
    });
}

function get_line_ahorros_gastos_ingresos_bar(){
    const ctx = $('#resumen_totales');

    var today = new Date()
    var año_antes_today = new Date(today)
    año_antes_today.setFullYear(año_antes_today.getFullYear()-1)
    var end_date = today.getDate()+"/"+ (today.getMonth()+1) + "/" + today.getFullYear()
    var begin_date = "1/"+ (año_antes_today.getMonth()+1) + "/" + año_antes_today.getFullYear()



    $.get("finanzas/resumen/total?begin_fecha="+begin_date+"&end_fecha="+end_date, function( totales ) {
        $.get("finanzas/resumen/total-ingresos?begin_fecha="+begin_date+"&end_fecha="+end_date, function( ingresos ) {
            $.get("finanzas/resumen/total-gastos?begin_fecha="+begin_date+"&end_fecha="+end_date, function( gastos ) {

                var labels = []
                var datos_totales = {}
                var datos_ingresos = {}
                var datos_gastos = {}
                var fecha_iterada = new Date(año_antes_today)
                for (var i=1;i<=13;i++){
                     label = (fecha_iterada.getMonth()+1) + "/" + fecha_iterada.getFullYear()
                     labels.push(label)
                     datos_totales[label] = 0
                     datos_ingresos[label] = 0
                     datos_gastos[label] = 0
                     fecha_iterada.setMonth(fecha_iterada.getMonth()+1)
                }
                for (var i=totales.length-1;i>=0;i--){
                    label = totales[i].mes+"/"+totales[i].año
                    datos_totales[label] = totales[i].total
                }
                for (var i=ingresos.length-1;i>=0;i--){
                    label = ingresos[i].mes+"/"+ingresos[i].año
                    datos_ingresos[label] = ingresos[i].total
                }
                for (var i=gastos.length-1;i>=0;i--){
                    label = gastos[i].mes+"/"+gastos[i].año
                    datos_gastos[label] = -gastos[i].total
                }

                var datos_grafica_totales = []
                var datos_grafica_ingresos = []
                var datos_grafica_gastos = []
                for (var i in labels){
                    label = labels[i]
                    datos_grafica_totales.push(datos_totales[label])
                    datos_grafica_ingresos.push(datos_ingresos[label])
                    datos_grafica_gastos.push(datos_gastos[label])
                }

                new Chart(ctx, {
                  type: 'line',
                  data: {
                    labels: labels,
                    datasets: [{
                      label: 'Ahorro',
                      data: datos_grafica_totales,
                      borderColor: '#AED6F1',
                      backgroundColor: '#AED6F1',
                      pointStyle: 'circle',
                      borderWidth: 2,
                      yAxisID: 'y',
                    },
                    {
                      label: 'Ingresos',
                      data: datos_grafica_ingresos,
                      borderColor: '#82E0AA',
                      backgroundColor: '#82E0AA',
                      pointStyle: 'circle',
                      borderWidth: 2,
                      yAxisID: 'y',
                    },
                    {
                      label: 'Gastos',
                      data: datos_grafica_gastos,
                      borderColor: '#F5B7B1',
                      pointStyle: 'circle',
                      backgroundColor: '#F5B7B1',
                      borderWidth: 2,
                      yAxisID: 'y',
                    }]
                  },
                  options: {
                    responsive: true,
                    interaction: {
                      mode: 'index',
                      intersect: false,
                    },
                    stacked: false,
                    scales: {
                      y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                      }
                    }
                  }
                });
            });
        });
    });
}