
function bt1() {
    const target = document.querySelector(".logo");
    target.style.color = "red";
}

// Muestra la tabla de gastos diarios y oculta la de mensuales y anuales.
function mostrar_diario() {

    const tabla_diarios = document.querySelector(".table-history-container") // <- Tabla gastos diarios.
    const tabla_mensuales = document.querySelector(".tabla-gastos-mensuales-container")
    const tabla_anuales = document.querySelector(".tabla-gastos-anuales-container")

    tabla_mensuales.style.display = "none";
    tabla_anuales.style.display = "none";
    tabla_diarios.style.display = "block";

}

function mostrar_mensual() {

    const tabla_diarios = document.querySelector(".table-history-container") // <- Tabla gastos diarios.
    const tabla_mensuales = document.querySelector(".tabla-gastos-mensuales-container")
    const tabla_anuales = document.querySelector(".tabla-gastos-anuales-container")

    tabla_mensuales.style.display = "block";
    tabla_anuales.style.display = "none";
    tabla_diarios.style.display = "none";
}

function mostrar_anual() {
    const tabla_diarios = document.querySelector(".table-history-container") // <- Tabla gastos diarios.
    const tabla_mensuales = document.querySelector(".tabla-gastos-mensuales-container")
    const tabla_anuales = document.querySelector(".tabla-gastos-anuales-container")

    tabla_mensuales.style.display = "none";
    tabla_anuales.style.display = "block";
    tabla_diarios.style.display = "none";
}

function listen() {

    document.querySelector("#btn-anuales").onclick = mostrar_anual;
    document.querySelector("#btn-mensuales").onclick = mostrar_mensual;
    document.querySelector("#btn-diarios").onclick = mostrar_diario;
}

document.addEventListener("DOMContentLoaded", listen);

