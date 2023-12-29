

function hacer_hacienda() {
    var year = $("#fechaDataPicker").val()

    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", "/finanzas/hacienda/"+year, true);
    xhttp.setRequestHeader("Content-Type", "application/json");

    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                console.log("correcto")
            } else if (xhttp.status != 200){
                var respuesta = JSON.parse(xhttp.responseText).message;
                $("#messageX").text(respuesta);
            }
    };
    xhttp.send();

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

