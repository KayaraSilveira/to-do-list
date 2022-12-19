const formsLogout = document.querySelectorAll(".js-form-logout");
const modalLogout = document.getElementById('modal-logout');
const btnCancelLogout = document.getElementById('btn-cancel-logout');
const btnConfirmLogout = document.getElementById('btn-confirm-logout');

formsLogout.forEach((form) => {
    form.addEventListener("submit", (event) => {

        event.preventDefault();
        openModalLogout();

        btnCancelLogout.addEventListener("click", closeModalLogout);
        modalLogout.children[0].addEventListener("click", closeModalLogout);
        btnConfirmLogout.addEventListener("click", () => {
            form.submit();
        })

    });
});

function openModalLogout() {
    modalLogout.children[0].classList.remove('hide');
    modalLogout.children[1].classList.remove('hide');
}

function closeModalLogout() {
    modalLogout.children[0].classList.add('hide');
    modalLogout.children[1].classList.add('hide');
}
