const loader = document.querySelector('.loader');

window.addEventListener('DOMContentLoaded', () => {
    loader.style.visibility = 'hidden';
});

const listaCargas = document.querySelector("#lista-cargas");
console.log(listaCargas);
listaCargas.addEventListener('click', (e) => {
    if (e.target.classList.contains("bi-bullseye")){
        console.log("prueba")
        e.target.classList.remove("bi-bullseye");
        e.target.classList.add("bi-check-circle-fill");
        return ;
    }

    if (e.target.classList.contains("bi-check-circle-fill")){
        e.target.classList.remove("bi-check-circle-fill");
        e.target.classList.add("bi-bullseye");
        return;
    }

    if (e.target.classList.contains("bi-trash")){
        console.log(e.target.closest(".row-carga"));
        return;
    }

});