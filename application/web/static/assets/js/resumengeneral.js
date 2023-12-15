$(document).ready(function() {
    get_line_ahorros_gastos_ingresos_bar();
});

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
