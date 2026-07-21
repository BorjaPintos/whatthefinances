$(document).ready(function() {
    get_line_ahorros_gastos_ingresos();
});

function get_line_ahorros_gastos_ingresos(){

    var today = new Date()
    var año_antes_today = new Date(today)
    año_antes_today.setFullYear(año_antes_today.getFullYear()-1)
    año_antes_today.setDate(1)
    var end_date = today.getDate()+"/"+ (today.getMonth()+1) + "/" + today.getFullYear()
    var begin_date = "1/"+ (año_antes_today.getMonth()+1) + "/" + año_antes_today.getFullYear()

    $.get("finanzas/resumen/total?begin_fecha="+begin_date+"&end_fecha="+end_date, function( totales ) {
        $.get("finanzas/resumen/total-ingresos?begin_fecha="+begin_date+"&end_fecha="+end_date, function( ingresos ) {
            $.get("finanzas/resumen/total-gastos?begin_fecha="+begin_date+"&end_fecha="+end_date, function( gastos ) {
                $.get("finanzas/cuenta", function(cuentas) {
                    $.get("finanzas/resumen/posiciones_meses?begin_fecha="+begin_date+"&end_fecha="+end_date, function( posiciones ) {
                        $.get("finanzas/resumen/posiciones_meses_acumuladas?begin_fecha="+begin_date+"&end_fecha="+end_date, function( posiciones_acumuladas ) {

                            var labels = []
                            var datos_totales = {}
                            var datos_ingresos = {}
                            var datos_gastos = {}
                            var datos_posiciones = {}
                            var datos_invertido = {}

                            var suma_total_cuentas = 0
                            for (i in cuentas){
                                suma_total_cuentas+=cuentas[i].total
                            }

                            var fecha_iterada = new Date(año_antes_today)
                            for (var i=1;i<=13;i++){
                                 label = (fecha_iterada.getMonth()+1) + "/" + fecha_iterada.getFullYear()
                                 labels.push(label)
                                 datos_totales[label] = 0
                                 datos_ingresos[label] = 0
                                 datos_gastos[label] = 0
                                 datos_posiciones[label] = 0
                                 datos_invertido[label] = 0
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
                            for (var i=0;i<posiciones.length;i++){
                                label = posiciones[i].mes+"/"+posiciones[i].año
                                if (datos_posiciones[label] === undefined) datos_posiciones[label] = 0
                                datos_posiciones[label] += posiciones[i].valor * posiciones[i].suma_participaciones
                            }
                            for (var i=0;i<posiciones_acumuladas.length;i++){
                                label = posiciones_acumuladas[i].mes+"/"+posiciones_acumuladas[i].año
                                if (datos_invertido[label] === undefined) datos_invertido[label] = 0
                                datos_invertido[label] += posiciones_acumuladas[i].precio_compra_mes
                            }

                            var datos_grafica_totales = []
                            var datos_grafica_ingresos = []
                            var datos_grafica_gastos = []
                            var datos_grafica_invertido = []
                            var suma_ahorrado = 0
                            for (var i in labels){
                                label = labels[i]
                                datos_grafica_totales.push(datos_totales[label] + datos_invertido[label])
                                suma_ahorrado+=datos_totales[label]
                                datos_grafica_ingresos.push(datos_ingresos[label])
                                datos_grafica_gastos.push(datos_gastos[label] - datos_invertido[label])
                                datos_grafica_invertido.push(datos_invertido[label])
                            }


                            var datos_grafica_acumulado = []
                            var datos_grafica_acumulado_invertido = []
                            var patrimonio = []
                            var current_mes = suma_total_cuentas-suma_ahorrado
                            for (var i in datos_totales){
                                current_mes += datos_totales[i]
                                datos_grafica_acumulado_invertido.push(datos_posiciones[i])
                                datos_grafica_acumulado.push(current_mes)
                                patrimonio.push(current_mes+datos_posiciones[i])
                            }

                            create_chart_line_ahorros_gastos_ingresos(labels, datos_grafica_totales, datos_grafica_ingresos, datos_grafica_gastos, datos_grafica_invertido)
                            create_chart_ahorros_acumulado(labels, datos_grafica_acumulado, datos_grafica_acumulado_invertido, patrimonio)
                        });
                    });
                });
            });
        });
    });
}

function create_chart_line_ahorros_gastos_ingresos(labels, datos_grafica_totales, datos_grafica_ingresos, datos_grafica_gastos, datos_grafica_invertido){
    const ctx = $('#resumen_totales');
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
        },
        {
          label: 'Invertido',
          data: datos_grafica_invertido,
          borderColor: '#F7DC6F',
          backgroundColor: '#F7DC6F',
          pointStyle: 'circle',
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
}

function create_chart_ahorros_acumulado(labels, datos_grafica_acumulado, datos_grafica_acumulado_invertido, patrimonio){
    const ctx = $('#crecimiento-total');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Ahorros acumulados',
          data: datos_grafica_acumulado,
          borderColor: '#AED6F1',
          backgroundColor: '#AED6F1',
          borderWidth: 2,
          yAxisID: 'y',
        },
        {
          label: 'Inversión acumulada',
          data: datos_grafica_acumulado_invertido,
          borderColor: '#F7DC6F',
          backgroundColor: '#F7DC6F',
          borderWidth: 2,
          yAxisID: 'y',
        },
        {
          label: 'Patrimonio',
          data: patrimonio,
          borderColor: '#82E0AA',
          backgroundColor: '#82E0AA',
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
}
