const loader = document.querySelector('.loader');

window.addEventListener('DOMContentLoaded', () => {
    loader.style.visibility = 'hidden';
});

const listaCargas = document.querySelector("#lista-cargas");
const minimaLey = document.querySelector("#id_minima_ley");
const maximaLey = document.querySelector("#id_maxima_ley");
const pagado = document.querySelector("#id_pagado");
const container = document.querySelector("#lista-cargas");

$('#id_destino').select2({
    language: 'es',
    theme: "bootstrap4",
    width: "100%",
    placeholder: "SELECCIONAR DESTINO",
});

minimaLey.addEventListener('change', (e) => {
    insertarCargas(parseFloat(minimaLey.value), parseFloat(maximaLey.value), pagado.checked ? 1 : 0);
});
maximaLey.addEventListener('change', (e) => {
    insertarCargas(parseFloat(minimaLey.value), parseFloat(maximaLey.value), pagado.checked ? 1 : 0);
});

pagado.addEventListener('change', (e) => {
    insertarCargas(parseFloat(minimaLey.value), parseFloat(maximaLey.value), pagado.checked ? 1 : 0);
});

const insertarCargas = async (min, max, pagado = 1) => {
    const url = `/produccion/produccion-cargas/${min}/${max}/${pagado}`;
    await axios(url)
        .then(res => {
            container.innerHTML = res.data;
            refreshInfo();
        });
};

container.addEventListener("click", (e) => {
    if (e.target.classList.contains("fa-minus-circle")) {
        e.target.closest('.row-carga').remove();
        refreshInfo();
    }
});

const refreshInfo = () => {
    const totalCargas = document.querySelector("#id_total_cargas");
    const idTms = document.querySelector("#id_tms");
    const idCargas = document.querySelector("#id_cargas");
    let totalTMS = 0;
    let ids = []

    const dataIds = document.querySelectorAll(".carga-id");
    const dataTms = document.querySelectorAll(".carga-tms");

    dataIds.forEach(element => {
        ids.push(element.getAttribute("data-id"));
    });

    dataTms.forEach(element => {
        let aux = parseFloat(element.getAttribute("data-tms").replace(',', '.')).toFixed(2);
        totalTMS += Number(aux);
    })
    console.log(totalCargas.value);
    totalCargas.value = dataIds.length;
    console.log(totalCargas.value);
    idTms.value = totalTMS.toFixed(2);
    idCargas.value = ids.toString();
};