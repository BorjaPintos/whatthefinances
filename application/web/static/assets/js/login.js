function on_login() {
    var name = document.getElementById("typeNameX").value;
    var password = document.getElementById("typePasswordX").value;

    var data = {
        name: name,
        password: password
    }
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/login", true);
    xhttp.setRequestHeader("Content-Type", "application/json");


    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4)
            if (xhttp.status === 200) {
                window.location = '/resumen.html';
            } else if (xhttp.status != 200){
                var respuesta = JSON.parse(xhttp.responseText).message;
                document.getElementById("typeMessageX").innerText = respuesta
            }
    };
    xhttp.send(JSON.stringify(data));
}

$("#form_login").submit(function(e){
    on_login();
    e.preventDefault(e);
});