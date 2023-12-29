function on_change_password() {
    var password = document.getElementById("typePasswordX").value;
    var newpassword = document.getElementById("typeNewPasswordX").value;
    var repeatNewpassword = document.getElementById("typeRepeatNewPasswordX").value;

    if (newpassword === repeatNewpassword) {

        var data = {
            password: password,
            new_password:newpassword
        }
        var xhttp = new XMLHttpRequest();

        xhttp.open("POST", "/user/change_password", true);
        xhttp.setRequestHeader("Content-Type", "application/json");


        xhttp.onreadystatechange = function () {
            if (xhttp.readyState === 4)
                if (xhttp.status === 200) {
                    window.location = '/resumen-general.html';
                } else if (xhttp.status != 200){
                    var respuesta = JSON.parse(xhttp.responseText).message;
                    document.getElementById("typeMessageX").innerText = respuesta
                }
        };
        xhttp.send(JSON.stringify(data));
    }
    else {
        document.getElementById("typeMessageX").innerText = "Las contraseñas nuevas no coinciden"
    }
}

$("#form_change_password").submit(function(e){
    on_change_password();
    e.preventDefault(e);
});