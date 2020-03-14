

document.addEventListener('DOMContentLoaded', function () {
    const elems = document.querySelectorAll('.sidenav');
    const tabs = document.querySelectorAll('.tabs');
    const instances = M.Sidenav.init(elems);
    const instance = M.Tabs.init(tabs);
});