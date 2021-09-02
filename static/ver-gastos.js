
function bt1() {
    const target = document.querySelector("#foo");
    target.style.color="red";
}

function listen() {
    document.querySelector("#btn-anuales").onclick = bt1;

    let input = document.querySelector(".btn-filtrar-fecha")
    input.addEventListener("keyup", function(){

        $.get("/" + input.value)
    })
}

document.addEventListener("DOMContentLoaded", listen);