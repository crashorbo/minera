const loader = document.querySelector('.loader');

window.addEventListener('DOMContentLoaded', () => {
    loader.style.visibility = 'hidden';
});

const listaCargas = document.querySelector("#lista-cargas");
console.log(listaCargas);
listaCargas.addEventListener('click', async(e) => {

    const rowTable = e.target.closest(".row-carga");
    const el = e.target;

    if (e.target.classList.contains("bi-bullseye")){
        console.log();
        await axios(el.getAttribute("data-entrega"))
            .then(res => {
                e.target.classList.remove("bi-bullseye");
                e.target.classList.add("bi-check-circle-fill");
                rowTable.querySelector(".bi-trash").classList.add("d-none");
            });               
        return ;
    }

    if (e.target.classList.contains("bi-check-circle-fill")){
        await axios(el.getAttribute("data-entrega"))
            .then(res => {
                e.target.classList.remove("bi-check-circle-fill");
                e.target.classList.add("bi-bullseye");
                rowTable.querySelector(".bi-trash").classList.remove("d-none");        
            });
        return;
    }

    if (e.target.classList.contains("bi-trash")){
        await axios(el.getAttribute("data-remove"))
            .then(res => {
                e.target.closest(".row-carga").remove();                
            });
        return;
    }

});