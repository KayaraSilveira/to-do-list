const formsLeaveList = document.querySelectorAll(".js-form-leave-list");
const modalLeaveList = document.getElementById('modal-leave-list');
const btnCancelLeaveList = document.getElementById('btn-cancel-leave-list');
const btnConfirmLeaveList = document.getElementById('btn-confirm-leave-list');

formsLeaveList.forEach((form) => {
    form.addEventListener("submit", (event) => {

        event.preventDefault();
        openModalLeaveList();

        btnCancelLeaveList.addEventListener("click", closeModalLeaveList);
        modalLeaveList.children[0].addEventListener("click", closeModalLeaveList);
        btnConfirmLeaveList.addEventListener("click", () => {
            form.submit();
        })

    });
});

function openModalLeaveList() {
    modalLeaveList.children[0].classList.remove('hide');
    modalLeaveList.children[1].classList.remove('hide');
}

function closeModalLeaveList() {
    modalLeaveList.children[0].classList.add('hide');
    modalLeaveList.children[1].classList.add('hide');
}
