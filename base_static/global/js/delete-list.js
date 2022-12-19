const formsDeleteList = document.querySelectorAll(".js-form-delete-list");
const modalDeleteList = document.getElementById('modal-delete-list');
const btnCancelDeleteList = document.getElementById('btn-cancel-del-list');
const btnConfirmDeleteList = document.getElementById('btn-confirm-del-list');

formsDeleteList.forEach((form) => {
    form.addEventListener("submit", (event) => {

        event.preventDefault();
        openModalDelList();

        btnCancelDeleteList.addEventListener("click", closeModalDelList);
        modalDeleteList.children[0].addEventListener("click", closeModalDelList);
        btnConfirmDeleteList.addEventListener("click", () => {
            form.submit();
        })

    });
});

function openModalDelList() {
    modalDeleteList.children[0].classList.remove('hide');
    modalDeleteList.children[1].classList.remove('hide');
}

function closeModalDelList() {
    modalDeleteList.children[0].classList.add('hide');
    modalDeleteList.children[1].classList.add('hide');
}
