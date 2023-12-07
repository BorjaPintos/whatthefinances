$( document ).ready(function() {
    $('#addFechaDataPicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'es-ES'
    });
    $('#editFechaDataPicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'es-ES'
    });
});


$('#add-button').on( "click", function() {
    $("#addTypeNombreX").val('')
    $("#addTypeCantidadInicialX").val('')
    $("#addTypePonderacionX").val('')
    $("#addTypeMessageX").text('')
    $('#addFechaDataPicker').datepicker('update',  new Date());
    $('#add').modal('show')
} );

$('#add-close-button').on( "click", function() {
    $('#add').modal('hide')
});

$('#add-submit-button').on( "click", function() {
   add_operacion();
});

$('.edit-element').on( "click", function() {

    var id = $(this).attr("data-element")

    var fecha = $.trim($('#fecha-'+id).text())
    var descripcion = $.trim($('#descripcion-'+id).text());
    var cantidad = $.trim($('#cantidad-'+id).text());
    var id_cuenta_cargo= $.trim($('#id_cuenta_cargo-'+id).val());
    var id_monedero_cargo= $.trim($('#id_monedero_cargo-'+id).val());
    var id_categoria_gasto= $.trim($('#id_categoria_gasto-'+id).val());
    var id_cuenta_abono= $.trim($('#id_cuenta_abono-'+id).val());
    var id_monedero_abono= $.trim($('#id_monedero_abono-'+id).val());
    var id_categoria_ingreso= $.trim($('#id_categoria_ingreso-'+id).val());

    $("#editTypeIdX").val(id)
    $('#editFechaDataPicker').datepicker('update',  fecha);
    $("#editTypeDescripcionX").val(descripcion)
    $("#editTypeCantidadX").val(cantidad)


   var div_gasto = $("#edit-div-gasto")
   var div_ingreso = $("#edit-div-ingreso")
   var div_transferencia = $("#edit-div-transferencia")
   var radio_transferencia = $("#edit-tipo-transferencia")
   var radio_gasto = $("#edit-tipo-gasto")
   var radio_ingreso = $("#edit-tipo-ingreso")

   div_gasto.collapse('hide');
   div_ingreso.collapse('hide');
   div_transferencia.collapse('hide');
   radio_transferencia.prop("checked", false)
   radio_gasto.prop("checked", false)
   radio_ingreso.prop("checked", false)


   if ((id_categoria_gasto) && (id_categoria_ingreso)){
        $("#edit-transferencia-categoria-ingreso-select").val(id_categoria_ingreso).change();
        $("#edit-transferencia-cuenta-abono-select").val(id_cuenta_abono).change();
        $("#edit-transferencia-monedero-abono-select").val(id_monedero_abono).change();
        $("#edit-transferencia-categoria-gasto-select").val(id_categoria_gasto).change();
        $("#edit-transferencia-cuenta-cargo-select").val(id_cuenta_cargo).change();
        $("#edit-transferencia-monedero-cargo-select").val(id_monedero_cargo).change();
        radio_transferencia.prop("checked", true)
        div_transferencia.collapse('show');

   } else if (id_categoria_gasto){
        $("#edit-gasto-categoria-gasto-select").val(id_categoria_gasto).change();
        $("#edit-gasto-cuenta-cargo-select").val(id_cuenta_cargo).change();
        $("#edit-gasto-monedero-cargo-select").val(id_monedero_cargo).change();
        radio_gasto.prop("checked", true)
        div_gasto.collapse('show');

   } else if(id_categoria_ingreso){
        $("#edit-ingreso-categoria-ingreso-select").val(id_categoria_ingreso).change();
        $("#edit-ingreso-cuenta-abono-select").val(id_cuenta_abono).change();
        $("#edit-ingreso-monedero-abono-select").val(id_monedero_abono).change();
        radio_ingreso.prop("checked", true)
        div_ingreso.collapse('show');

   }

   $('#edit').modal('show')
});

$('#edit-close-button').on( "click", function() {
    $('#edit').modal('hide')
} );

$('#edit-submit-button').on( "click", function() {
   update_operacion()
});

$('.delete-element').on( "click", function() {
   delete_operacion($(this).attr("data-element"))
});

$('#add-ingreso-categoria-ingreso-select').on("change", function() {
   var option = $('#add-ingreso-categoria-ingreso-select option:selected')
   var id_cuenta = option.attr("data-id-cuenta-defecto")
   var id_monedero = option.attr("data-id-monedero-defecto")

   $("#add-ingreso-cuenta-abono-select").val(id_cuenta).change();
   $("#add-ingreso-monedero-abono-select").val(id_monedero).change();
});

$('#add-gasto-categoria-gasto-select').on("change", function() {
   var option = $('#add-gasto-categoria-gasto-select option:selected')
   var id_cuenta = option.attr("data-id-cuenta-defecto")

   var id_monedero = option.attr("data-id-monedero-defecto")
   $("#add-gasto-cuenta-cargo-select").val(id_cuenta).change();
   $("#add-gasto-monedero-cargo-select").val(id_monedero).change();
});

$('#add-transferencia-categoria-ingreso-select').on("change", function() {
   var option = $('#add-transferencia-categoria-ingreso-select option:selected')
   var id_cuenta = option.attr("data-id-cuenta-defecto")
   var id_monedero = option.attr("data-id-monedero-defecto")

   $("#add-transferencia-cuenta-abono-select").val(id_cuenta).change();
   $("#add-transferencia-monedero-abono-select").val(id_monedero).change();
});

$('#add-transferencia-categoria-gasto-select').on("change", function() {
   var option = $('#add-transferencia-categoria-gasto-select option:selected')
   var id_cuenta = option.attr("data-id-cuenta-defecto")

   id_monedero = option.attr("data-id-monedero-defecto")
   $("#add-transferencia-cuenta-cargo-select").val(id_cuenta).change();
   $("#add-transferencia-monedero-cargo-select").val(id_monedero).change();
});

$('#edit-ingreso-categoria-ingreso-select').on("change", function() {
   var option = $('#edit-ingreso-categoria-ingreso-select option:selected')
   var id_cuenta = option.attr("data-id-cuenta-defecto")
   var id_monedero = option.attr("data-id-monedero-defecto")

   $("#edit-ingreso-cuenta-abono-select").val(id_cuenta).change();
   $("#edit-ingreso-monedero-abono-select").val(id_monedero).change();
});

$('#edit-gasto-categoria-gasto-select').on("change", function() {
   var option = $('#edit-gasto-categoria-gasto-select option:selected')
   var id_cuenta = option.attr("data-id-cuenta-defecto")

   var id_monedero = option.attr("data-id-monedero-defecto")
   $("#edit-gasto-cuenta-cargo-select").val(id_cuenta).change();
   $("#edit-gasto-monedero-cargo-select").val(id_monedero).change();
});

$('#edit-transferencia-categoria-ingreso-select').on("change", function() {
   var option = $('#edit-transferencia-categoria-ingreso-select option:selected')
   var id_cuenta = option.attr("data-id-cuenta-defecto")
   var id_monedero = option.attr("data-id-monedero-defecto")

   $("#edit-transferencia-cuenta-abono-select").val(id_cuenta).change();
   $("#edit-transferencia-monedero-abono-select").val(id_monedero).change();
});

$('#edit-transferencia-categoria-gasto-select').on("change", function() {
   var option = $('#edit-transferencia-categoria-gasto-select option:selected')
   var id_cuenta = option.attr("data-id-cuenta-defecto")

   id_monedero = option.attr("data-id-monedero-defecto")
   $("#edit-transferencia-cuenta-cargo-select").val(id_cuenta).change();
   $("#edit-transferencia-monedero-cargo-select").val(id_monedero).change();
});

$('#add-seleccion_tipo input:radio[name=add_tipo]').on('change', function() {
   var tipo_opcion = $('#add-seleccion_tipo input:radio[name=add_tipo]:checked').attr('id')
   var div_gasto = $("#add-div-gasto")
   var div_ingreso = $("#add-div-ingreso")
   var div_transferencia = $("#add-div-transferencia")
   if (tipo_opcion == "add-tipo-gasto"){
        div_gasto.collapse('show');
        div_ingreso.collapse('hide');
        div_transferencia.collapse('hide');
   }
   else if (tipo_opcion == "add-tipo-ingreso"){
        div_gasto.collapse('hide');
        div_ingreso.collapse('show');
        div_transferencia.collapse('hide');
   }
   else if (tipo_opcion == "add-tipo-transferencia"){
        div_gasto.collapse('hide');
        div_ingreso.collapse('hide');
        div_transferencia.collapse('show');
   }
});

$('#edit-seleccion_tipo input:radio[name=edit_tipo]').on('change', function() {
   var tipo_opcion = $('#edit-seleccion_tipo input:radio[name=edit_tipo]:checked').attr('id')
   var div_gasto = $("#edit-div-gasto")
   var div_ingreso=$("#edit-div-ingreso")
   var div_transferencia=$("#edit-div-transferencia")
   if (tipo_opcion == "edit-tipo-gasto"){
        div_gasto.collapse('show');
        div_ingreso.collapse('hide');
        div_transferencia.collapse('hide');
   }
   else if (tipo_opcion == "edit-tipo-ingreso"){
        div_gasto.collapse('hide');
        div_ingreso.collapse('show');
        div_transferencia.collapse('hide');
   }
   else if (tipo_opcion == "edit-tipo-transferencia"){
        div_gasto.collapse('hide');
        div_ingreso.collapse('hide');
        div_transferencia.collapse('show');
   }
});

function add_operacion() {
    var fecha = $("#addFechaDataPicker").val()
    var descripcion = $("#addTypeDescripcionX").val();
    var cantidad = $("#addTypeCantidadX").val();

    tipo_opcion = $('#add-seleccion_tipo input:radio[name=add_tipo]:checked').attr('id')
   if (tipo_opcion == "add-tipo-gasto"){
    var id_categoria_ingreso = undefined;
    var id_cuenta_abono = undefined;
    var id_monedero_abono = undefined;
    var id_categoria_gasto = $("#add-gasto-categoria-gasto-select").val();
    var id_cuenta_cargo = $("#add-gasto-cuenta-cargo-select").val();
    var id_monedero_cargo = $("#add-gasto-monedero-cargo-select").val();
   }
   else if (tipo_opcion == "add-tipo-ingreso"){
    var id_categoria_ingreso = $("#add-ingreso-categoria-ingreso-select").val();
    var id_cuenta_abono = $("#add-ingreso-cuenta-abono-select").val();
    var id_monedero_abono = $("#add-ingreso-monedero-abono-select").val();
    var id_categoria_gasto = undefined;
    var id_cuenta_cargo = undefined;
    var id_monedero_cargo = undefined;
   }
   else if (tipo_opcion == "add-tipo-transferencia"){
    var id_categoria_ingreso = $("#add-transferencia-categoria-ingreso-select").val();
    var id_cuenta_abono = $("#add-transferencia-cuenta-abono-select").val();
    var id_monedero_abono = $("#add-transferencia-monedero-abono-select").val();
    var id_categoria_gasto = $("#add-transferencia-categoria-gasto-select").val();
    var id_cuenta_cargo = $("#add-transferencia-cuenta-cargo-select").val();
    var id_monedero_cargo = $("#add-transferencia-monedero-cargo-select").val();
   }

    var data = {
        fecha: fecha,
        descripcion: descripcion,
        cantidad: cantidad ? cantidad : null,
        id_categoria_gasto: parseInt(id_categoria_gasto) ? id_categoria_gasto : null,
        id_monedero_cargo: parseInt(id_monedero_cargo) ? id_monedero_cargo : null,
        id_cuenta_cargo: parseInt(id_cuenta_cargo) ? id_cuenta_cargo : null,
        id_categoria_ingreso: parseInt(id_categoria_ingreso) ? id_categoria_ingreso : null,
        id_monedero_abono: parseInt(id_monedero_abono) ? id_monedero_abono : null,
        id_cuenta_abono: parseInt(id_cuenta_abono) ? id_cuenta_abono : null
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/finanzas/operacion", true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 201) {
                window.location = '/operaciones.html';
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#addTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));

}

function delete_operacion(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/finanzas/operacion/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/operaciones.html';
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

function update_operacion() {
    var id = $.trim($("#editTypeIdX").val())
    var fecha = $("#editFechaDataPicker").val()
    var descripcion = $("#editTypeDescripcionX").val();
    var cantidad = $("#editTypeCantidadX").val();

    tipo_opcion = $('#edit-seleccion_tipo input:radio[name=edit_tipo]:checked').attr('id')
   if (tipo_opcion == "edit-tipo-gasto"){
    var id_categoria_ingreso = undefined;
    var id_cuenta_abono = undefined;
    var id_monedero_abono = undefined;
    var id_categoria_gasto = $("#edit-gasto-categoria-gasto-select").val();
    var id_cuenta_cargo = $("#edit-gasto-cuenta-cargo-select").val();
    var id_monedero_cargo = $("#edit-gasto-monedero-cargo-select").val();
   }
   else if (tipo_opcion == "edit-tipo-ingreso"){
    var id_categoria_ingreso = $("#edit-ingreso-categoria-ingreso-select").val();
    var id_cuenta_abono = $("#edit-ingreso-cuenta-abono-select").val();
    var id_monedero_abono = $("#edit-ingreso-monedero-abono-select").val();
    var id_categoria_gasto = undefined;
    var id_cuenta_cargo = undefined;
    var id_monedero_cargo = undefined;
   }
   else if (tipo_opcion == "edit-tipo-transferencia"){
    var id_categoria_ingreso = $("#edit-transferencia-categoria-ingreso-select").val();
    var id_cuenta_abono = $("#edit-transferencia-cuenta-abono-select").val();
    var id_monedero_abono = $("#edit-transferencia-monedero-abono-select").val();
    var id_categoria_gasto = $("#edit-transferencia-categoria-gasto-select").val();
    var id_cuenta_cargo = $("#edit-transferencia-cuenta-cargo-select").val();
    var id_monedero_cargo = $("#edit-transferencia-monedero-cargo-select").val();
   }

   var data = {
        fecha: fecha,
        descripcion: descripcion,
        cantidad: cantidad ? cantidad : null,
        id_categoria_gasto: parseInt(id_categoria_gasto) ? id_categoria_gasto : null,
        id_monedero_cargo: parseInt(id_monedero_cargo) ? id_monedero_cargo : null,
        id_cuenta_cargo: parseInt(id_cuenta_cargo) ? id_cuenta_cargo : null,
        id_categoria_ingreso: parseInt(id_categoria_ingreso) ? id_categoria_ingreso : null,
        id_monedero_abono: parseInt(id_monedero_abono) ? id_monedero_abono : null,
        id_cuenta_abono: parseInt(id_cuenta_abono) ? id_cuenta_abono : null
   }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/finanzas/operacion/"+id, true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/operaciones.html';
            } else if (xhttp.status != 201){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#editTypeMessageX").text(respuesta)
            }
    };
    xhttp.send(JSON.stringify(data));
}
