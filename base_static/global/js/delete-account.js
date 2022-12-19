const formsDeleteAcc = document.querySelectorAll(".js-form-delete-acc");
const modalDeleteAcc = document.getElementById('modal-delete-acc');
const btnCancelDeleteAcc = document.getElementById('btn-cancel-del-acc');
const btnConfirmDeleteAcc = document.getElementById('btn-confirm-del-acc');

formsDeleteAcc.forEach((form) => {
    form.addEventListener("submit", (event) => {

        event.preventDefault();
        openModalDelAcc();

        btnCancelDeleteAcc.addEventListener("click", closeModalDelAcc);
        modalDeleteAcc.children[0].addEventListener("click", closeModalDelAcc);
        btnConfirmDeleteAcc.addEventListener("click", () => {
            form.submit();
        })

    });
});

function openModalDelAcc() {
    modalDeleteAcc.children[0].classList.remove('hide');
    modalDeleteAcc.children[1].classList.remove('hide');
}

function closeModalDelAcc() {
    modalDeleteAcc.children[0].classList.add('hide');
    modalDeleteAcc.children[1].classList.add('hide');
}
