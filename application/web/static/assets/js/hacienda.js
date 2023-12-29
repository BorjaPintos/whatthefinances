function get_dinero_total_operaciones(response_operaciones){
    var suma_total = 0;
    for (var i in response_operaciones.elements){
        suma_total += response_operaciones.elements[i].cantidad
    }
    return suma_total
}

async function get_total_operaciones(data, callback, suma_parcial){
    var suma_total = (suma_parcial === undefined) ? 0 : suma_parcial;
    $.ajax({
        url: "/finanzas/operacion",
        contentType: "application/json",
        data: data,
        type: "get",
        success: function(response){
            suma_total += get_dinero_total_operaciones(response)
            if (response.has_more_elements) {
                data.offset = response.offset + response.pagination_size
                get_total_operaciones(data, callback, suma_total)
            } else {
                callback(suma_total);
            }
        },
        error: function(response){
        }
    })
}

function get_valor_actual(response_operaciones){
    var suma_total = 0;
    for (var i in response_operaciones.elements){
        suma_total += response_operaciones.elements[i].valor_actual
    }
    return suma_total
}

async function  get_total_brokers_extrangeros(data, callback, suma_parcial){
    var suma_total = (suma_parcial === undefined) ? 0 : suma_parcial;
    data.abierto = true
    data.end_fecha_compra = data.end_fecha
    $.ajax({
        url: "/finanzas/posicionaccion",
        contentType: "application/json",
        data: data,
        type: "get",
        success: function(response){
            suma_total += get_valor_actual(response)
            if (response.has_more_elements) {
                data.offset = response.offset + response.pagination_size
                get_total_brokers_extrangeros(data, callback, suma_total)
            } else {
                callback(suma_total);
            }
        },
        error: function(response){
        }
    })
}

function get_suma_total_compra_acciones(response_operaciones){
    var suma_total = 0;
    for (var i in response_operaciones.elements){
        suma_total += response_operaciones.elements[i].valor_adquisicion
    }
    return suma_total
}

function get_suma_total_venta_acciones(response_operaciones){
    var suma_total = 0;
    for (var i in response_operaciones.elements){
        suma_total += response_operaciones.elements[i].valor_transmision
    }
    return suma_total
}

async function get_total_acciones(data, callback, suma_parcial_compra, suma_parcial_venta){
    var suma_total_compra = (suma_parcial_compra === undefined) ? 0 : suma_parcial_compra;
    var suma_total_venta = (suma_parcial_venta === undefined) ? 0 : suma_parcial_venta;
    data.abierta = false
    $.ajax({
        url: "/finanzas/posicionaccion",
        contentType: "application/json",
        data: data,
        type: "get",
        success: function(response){
            suma_total_compra += get_suma_total_compra_acciones(response)
            suma_total_venta += get_suma_total_venta_acciones(response)
            if (response.has_more_elements) {
                data.offset = response.offset + response.pagination_size
                get_total_acciones(data, callback, suma_total_compra, suma_total_venta)
            } else {
                callback(suma_total_compra, suma_total_venta);
            }
        },
        error: function(response){
        }
    })
}



async function get_total_dividendos(data, callback){

    $.ajax({
        url: "/finanzas/dividendorango",
        contentType: "application/json",
        data: data,
        type: "get",
        success: function(response){
        var suma_total = 0;
            var suma_dividendos_bruto = 0;
            var suma_retencion_dividendos = 0;
            for (var i in response){
                suma_dividendos_bruto += response[i].dividendo
                suma_retencion_dividendos += response[i].retencion
            }
            callback(suma_dividendos_bruto, suma_retencion_dividendos);

        },
        error: function(response){
        }
    })
}

async function afiliaciones_colegios_partidos_sindicatos(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_colegio = 48
    id_partido_politico = 62
    id_sindicatos = 63
    */
    data.list_id_categoria_gasto = "48,62,63"
    get_total_operaciones(data, function(suma_total){
        $("#afiliaciones").text(suma_total.toFixed(2));
    })
}

async function donaciones_beneficas(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_donaciones_beneficas = 14
    */
    data.id_categoria_gasto = 14
    get_total_operaciones(data, function(suma_total){
        $("#donaciones").text(suma_total.toFixed(2));
    })
}

async function hipoteca(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_hipoteca = 19
    */
    data.id_categoria_gasto = 19
    get_total_operaciones(data, function(suma_total){
        $("#hipoteca").text(suma_total.toFixed(2));
    })
}

async function alquiler(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_alquiler = 20
    */
    data.id_categoria_gasto = 20
    get_total_operaciones(data, function(suma_total){
        $("#alquiler").text(suma_total.toFixed(2));
    })
}

async function aportaciones_plan_pensiones(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_planes_pensiones = 68
    */
    data.id_categoria_gasto = 68
    get_total_operaciones(data, function(suma_total){
        $("#planespension").text(suma_total.toFixed(2));
    })
}

async function material_escolar(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_material_escolar = 66
    */
    data.id_categoria_gasto = 66
    get_total_operaciones(data, function(suma_total){
        $("#materialescolar").text(suma_total.toFixed(2));
    })
}

async function rehabilitacion_vivienda(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_rehabilitacion_vivienda = 64
    */
    data.id_categoria_gasto = 64
    get_total_operaciones(data, function(suma_total){
        $("#rehabilitacionvivienda").text(suma_total.toFixed(2));
    })
}

async function guarderia(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_guarderia = 65
    */
    data.id_categoria_gasto = 65
    get_total_operaciones(data, function(suma_total){
        $("#guarderia").text(suma_total.toFixed(2));
    })
}

async function nominas(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_nominas = 1
    id_finiquito = 27
    id_paro = 30
    id_pension_alimenticia = 26
    id_pension_viudedad = 31
    id_pension_jubilacion = 32
    id_dietas = 25
    */
    data.list_id_categoria_ingreso = "1,27,26,31,32,25"
    get_total_operaciones(data, function(suma_total){
        $("#nominas").text(suma_total.toFixed(2));
    })
}

async function otras_ganancias_patrimoniales(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_ingresos_extraordinarios = 3
    id_otras_ganancias = 2
    id_otras_ganancias = 12
    */
    data.list_id_categoria_ingreso = "2,3,12"
    get_total_operaciones(data, function(suma_total){
        $("#otrasganancias").text(suma_total.toFixed(2));
    })
}

async function becas_subvenciones(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_becas = 4
    id_subvenciones = 5
    */
    data.list_id_categoria_ingreso = "4,5"
    get_total_operaciones(data, function(suma_total){
        $("#becassubvenciones").text(suma_total.toFixed(2));
    })
}

async function rentas_de_alquileres(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_rentas_alquiler = 17
    */
    data.id_categoria_ingreso = 17
    get_total_operaciones(data, function(suma_total){
        $("#rentasalquiler").text(suma_total.toFixed(2));
    })
}

async function regalos(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    /*
    id_regalos = 11
    */
    data.id_categoria_ingreso = 1
    get_total_operaciones(data, function(suma_total){
        $("#regalos").text(suma_total.toFixed(2));
    })
}

async function compraventaacciones(begin_date, end_date){

    var data = {"begin_fecha_venta":begin_date, "end_fecha_venta":end_date}

    get_total_acciones(data, function(adquisicion, transmision){
        $("#accionesadquisicion").text(adquisicion.toFixed(2));
        $("#accionestansmision").text(transmision.toFixed(2));
    })
}

async function dividendos(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}

    $.ajax({
        url: "/finanzas/dividendo",
        contentType: "application/json",
        data: data,
        type: "get",
        success: function(dividendos){
            var list_isin = ""
            for (var i in dividendos){
                list_isin+=dividendos[i].isin + ","
            };
            data.list_isin = list_isin
            if (list_isin.length > 0){
                list_isin = list_isin.slice(0, -1)
            }

            get_total_dividendos(data, function(bruto, retencion){
                $("#dividendosbruto").text(bruto.toFixed(2));
                $("#dividendosretencion").text(retencion.toFixed(2));
            })
        },
        error: function(){

        }
    });
}

async function brokers_extrangeros(begin_date, end_date){

    var data = {"begin_fecha":begin_date, "end_fecha":end_date}
    data.extrangero = true
    $.ajax({
        url: "/finanzas/broker",
        contentType: "application/json",
        data: data,
        type: "get",
        success: function(brokers){
            var list_id = ""
            for (var i in brokers){
                list_id+=brokers[i].id + ","
            };
            if (brokers.length > 0){
                list_id = list_id.slice(0, -1)
            }
            data.list_id_broker = list_id

            get_total_brokers_extrangeros(data, function(suma_total){
                $("#brokersextrangeros").text(suma_total.toFixed(2));
            })
        },
        error: function(){

        }
    });
}

async function hacer_hacienda() {
    var year = $("#fechaDataPicker").val()

    var begin_date = moment().year(year).startOf('year').format('DD/MM/YYYY');
    var end_date = moment().year(year).endOf('year').format('DD/MM/YYYY');

    await Promise.all([
        nominas(begin_date, end_date),
        otras_ganancias_patrimoniales(begin_date, end_date),
        becas_subvenciones(begin_date, end_date),
        rentas_de_alquileres(begin_date, end_date),
        regalos(begin_date, end_date),
        afiliaciones_colegios_partidos_sindicatos(begin_date, end_date),
        donaciones_beneficas(begin_date, end_date),
        aportaciones_plan_pensiones(begin_date, end_date),
        hipoteca(begin_date, end_date),
        alquiler(begin_date, end_date),
        material_escolar(begin_date, end_date),
        guarderia(begin_date, end_date),
        rehabilitacion_vivienda(begin_date, end_date),
        brokers_extrangeros(begin_date, end_date),
        compraventaacciones(begin_date, end_date),
        dividendos(begin_date, end_date),
    ]);
}



get_local_number = function(num){
    return $.fn.dataTable.render.number('', ',', 2).display(num);
}

get_local_integer = function(num){
    return $.fn.dataTable.render.number('').display(num);
}

get_datepicker_conf = function(){
    return {
        format: 'yyyy'
    }
}



$(document).ready(function() {

    $('#fechaDataPicker').datepicker(get_datepicker_conf());
    $("#fechaDataPicker").val(moment().subtract(1, 'year').format("YYYY"));
    $('#hacer-button').on( "click", function() {
        hacer_hacienda()
    });
});

