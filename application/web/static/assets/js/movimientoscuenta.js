var id_cuenta = null;
var chart = null;

get_local_number = function (num) {
    return $.fn.dataTable.render.number('', ',', 2).display(num);
}

render_dinero = function (data, type) {
    var number = get_local_number(data);
    var add_class = ""
    if (type === 'display') {
        if (data > 0)
            add_class = "text-success"
        else if (data < 0)
            add_class = "text-danger"
        return "<span class='ms-2 font-weight-bold " + add_class + "'>" + number + "</span><span class='ms-2 font-weight-bold " + add_class + "'>€</span>"
    }
    return data
}

render_texto = function (data, type) {
    var new_data = data
    if (data == undefined)
        new_data = "-"
    if (type === 'display') {
        return '<span class="badge custom-badge">' + new_data + '</span>'
    }
    return new_data
}

get_datapicker_conf = function () {
    return {
        singleDatePicker: true,
        timePicker: false,
        autoApply: false,
        autoUpdateInput: true,
        locale: {
            format: "DD/MM/YYYY",
            applyLabel: "Aplicar",
            cancelLabel: "Limpiar",
            weekLabel: "S",
            daysOfWeek: [
                "Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"
            ],
            monthNames: [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ],
            firstDay: 1
        }
    }
}

function load_categorias() {
    $.get("finanzas/categoria_gasto?order_property=descripcion&order_type=asc", function (categorias) {
        var selector = $("#search-categoria-gasto-select");
        for (i in categorias) {
            if (!categorias[i].eliminado) {
                selector.append(new Option(categorias[i].descripcion, categorias[i].id));
            }
        }
    });
    $.get("finanzas/categoria_ingreso?order_property=descripcion&order_type=asc", function (categorias) {
        var selector = $("#search-categoria-ingreso-select");
        for (i in categorias) {
            if (!categorias[i].eliminado) {
                selector.append(new Option(categorias[i].descripcion, categorias[i].id));
            }
        }
    });
}

function load_chart() {
    $.get("finanzas/cuenta/" + id_cuenta, function (cuenta) {
        var cantidad_inicial = cuenta.cantidad_inicial || 0;

        $.get("finanzas/movimiento_cuenta?id_cuenta=" + id_cuenta + "&order_property=fecha&order_type=asc&count=10000&offset=0", function (response) {
            var elements = response.elements;
            var labels = [];
            var datos_saldo = [];
            var saldo = cantidad_inicial;

            for (var i = 0; i < elements.length; i++) {
                saldo += elements[i].cantidad;
                labels.push(elements[i].fecha);
                datos_saldo.push(saldo);
            }

            var today = new Date();
            var yearAgo = new Date(today);
            yearAgo.setFullYear(yearAgo.getFullYear() - 1);

            var filteredLabels = [];
            var filteredData = [];
            for (var i = 0; i < labels.length; i++) {
                var parts = labels[i].split("/");
                var fecha = new Date(parts[2], parts[1] - 1, parts[0]);
                if (fecha >= yearAgo) {
                    filteredLabels.push(labels[i]);
                    filteredData.push(datos_saldo[i]);
                }
            }

            if (filteredLabels.length === 0 && labels.length > 0) {
                filteredLabels = labels;
                filteredData = datos_saldo;
            }

            create_chart_evolucion(filteredLabels, filteredData);
        });
    });
}

function create_chart_evolucion(labels, data) {
    var ctx = document.getElementById('evolucion-cuenta');
    if (chart) {
        chart.destroy();
    }
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Saldo Cuenta',
                data: data,
                borderColor: '#AED6F1',
                backgroundColor: '#AED6F1',
                pointStyle: 'circle',
                pointRadius: 4,
                borderWidth: 2,
                yAxisID: 'y',
                fill: true,
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
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return 'Saldo: ' + get_local_number(context.parsed.y) + ' €';
                        }
                    }
                }
            }
        }
    });
}

$(document).ready(function () {
    id_cuenta = $('#id_cuenta').val();

    if (!id_cuenta || id_cuenta === 'None') {
        return;
    }

    load_categorias();
    load_chart();

    $('#search-fecha-begin-datapicker').daterangepicker(get_datapicker_conf());
    $('#search-fecha-begin-datapicker').val('');
    $('#search-fecha-end-datapicker').daterangepicker(get_datapicker_conf());
    $('#search-fecha-end-datapicker').val('');

    $('#search-fecha-begin-datapicker').on('cancel.daterangepicker', function (ev, picker) {
        $('#search-fecha-begin-datapicker').val('');
    });
    $('#search-fecha-end-datapicker').on('cancel.daterangepicker', function (ev, picker) {
        $('#search-fecha-end-datapicker').val('');
    });

    table = $('#lista_tabla')
        .on('preXhr.dt', function (e, settings, data) {
            data.count = data.length
            data.offset = data.start
            data.order_property = data.columns[data.order[0].column].data
            data.order_type = data.order[0].dir
        })
        .on('xhr.dt', function (e, settings, json, xhr) {
            json.recordsTotal = json.total_elements;
            json.recordsFiltered = json.total_elements;

            var cantidad_inicial = 0;
            $.ajax({
                url: "finanzas/cuenta/" + id_cuenta,
                async: false,
                dataType: 'json',
                success: function (cuenta) {
                    cantidad_inicial = cuenta.cantidad_inicial || 0;
                }
            });

            $.ajax({
                url: "finanzas/movimiento_cuenta?id_cuenta=" + id_cuenta + "&order_property=fecha&order_type=asc&count=10000&offset=0",
                async: false,
                dataType: 'json',
                success: function (response) {
                    var saldo_map = {};
                    var saldo = cantidad_inicial;
                    for (var i = 0; i < response.elements.length; i++) {
                        saldo += response.elements[i].cantidad;
                        saldo_map[response.elements[i].id] = saldo;
                    }
                    for (var i = 0; i < json.elements.length; i++) {
                        json.elements[i].saldo = saldo_map[json.elements[i].id] || 0;
                        if (json.elements[i].id_categoria_gasto != undefined && json.elements[i].id_categoria_ingreso != undefined) {
                            json.elements[i].DT_RowClass = "transferencia";
                        } else if (json.elements[i].id_categoria_gasto != undefined) {
                            json.elements[i].DT_RowClass = "gasto";
                        } else {
                            json.elements[i].DT_RowClass = "ingreso";
                        }
                    }
                }
            });
        })
        .DataTable({
            dom: '<flrt<"#table_fotter"ip>',
            serverSide: true,
            ajax: {
                url: '/finanzas/movimiento_cuenta',
                data: function (d) {
                    d.id_cuenta = id_cuenta;
                    var begin_fecha = $('#search-fecha-begin-datapicker').val();
                    var end_fecha = $('#search-fecha-end-datapicker').val();
                    var id_categoria_gasto = $("#search-categoria-gasto-select").val();
                    var id_categoria_ingreso = $("#search-categoria-ingreso-select").val();

                    if (begin_fecha != '')
                        d.begin_fecha = begin_fecha;
                    if (end_fecha != '')
                        d.end_fecha = end_fecha;
                    if (id_categoria_gasto != '')
                        d.id_categoria_gasto = id_categoria_gasto;
                    if (id_categoria_ingreso != '')
                        d.id_categoria_ingreso = id_categoria_ingreso;
                },
                dataSrc: 'elements',
            },
            columns: [
                {
                    data: 'fecha',
                    type: "string",
                    render: render_texto,
                    width: "15%"
                },
                {
                    data: 'descripcion',
                    type: "string",
                    render: render_texto,
                    orderSequence: [],
                    width: "30%"
                },
                {
                    data: 'cantidad',
                    type: "num",
                    render: render_dinero,
                    width: "15%"
                },
                {
                    data: 'saldo',
                    type: "num",
                    render: render_dinero,
                    width: "15%"
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
                info: 'Total _MAX_ Movimientos',
                infoEmpty: 'No hay Movimientos',
                zeroRecords: "No hay Movimientos",
                loadingRecords: "Cargando...",
                decimal: ",",
            }
        });

    $('#search-button').on("click", function () {
        table.ajax.reload(null, false);
    });
});
