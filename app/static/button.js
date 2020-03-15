
document.addEventListener('DOMContentLoaded', function () {

});

function checkForm(form) {
    form._submit.disabled = true;
    return true;
}

function disableLink(link) {
    link.style.display = 'none'
}
