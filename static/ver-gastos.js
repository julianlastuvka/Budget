
function bt1() {
    const target = document.querySelector("#foo");
    target.style.color="red";
}

function listen() {
    document.querySelector("#btn-anuales").onclick = bt1;
}

document.addEventListener("DOMContentLoaded", listen);