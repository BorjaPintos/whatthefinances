

function add_valor_accion() {
    var fecha = $("#addFechaDataPicker").val()
    var isin = $("#add-isin-select").val();
    var valor_accion = $("#addTypeValorAccionX").val();



    var data = {
        fecha: fecha,
        isin: isin,
        valor_accion: parseFloat(precio_accion).toFixed(4) ? precio_accion : null,
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/valoraccion", true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 201) {
                $('#add').modal('hide')
                table.ajax.reload( null, false );
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

$(document).ready(function() {

    $('#editFechaDataPickerInput').daterangepicker(get_daterangepicker_config());

    $('#addFechaDataPickerInput').daterangepicker(get_daterangepicker_config());

    $('#add-button').on( "click", function() {
        $('#addFechaDataPickerInput').val(moment().format("DD/MM/YYYY HH:mm"));
        $("#addTypeValorAccionX").val('')
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


