
function bt1() {
    const target = document.querySelector(".logo");
    target.style.color="red";
}

function mostrar_diario(){
    const tabla = document.querySelector(".table-history-container")
    tabla.style.display= "none";
}

function listen() {

    document.querySelector("#btn-anuales").onclick = bt1;
    document.querySelector("#btn-diarios").onclick = mostrar_diario;
}

document.addEventListener("DOMContentLoaded", listen);

