$(document).ready(function() {
    const ctx = $('#resumen_totales');

    var today = new Date()
    var año_antes_today = new Date(today)
    año_antes_today.setFullYear(año_antes_today.getFullYear()-1)
    var end_date = today.getDate()+"/"+ (today.getMonth()+1) + "/" + today.getFullYear()
    var begin_date = "1/"+ (año_antes_today.getMonth()+1) + "/" + año_antes_today.getFullYear()



    $.get("finanzas/resumen/total?begin_fecha="+begin_date+"&end_fecha="+end_date, function( data ) {

        var labels = []
        var datos = {}
        var fecha_iterada = new Date(año_antes_today)
        for (var i=1;i<=13;i++){
             label = (fecha_iterada.getMonth()+1) + "/" + fecha_iterada.getFullYear()
             labels.push(label)
             datos[label] = 0
             fecha_iterada.setMonth(fecha_iterada.getMonth()+1)
        }
        for (var i=data.length-1;i>=0;i--){
            resumen = data[i];
            label = resumen.mes+"/"+resumen.año
            datos[label] = resumen.total
        }

        var datos_grafica = []
        for (var i in labels){
            datos_grafica.push(datos[labels[i]])
        }

        new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Meses',
              data: datos_grafica,
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
    });



});