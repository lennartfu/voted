for (let el of document.querySelectorAll("input")) {
    el.classList.add("form-control");
}
for (let el of document.querySelectorAll("textarea")) {
    el.classList.add("form-control");
    el.rows = 2;
}
for (let el of document.querySelectorAll("select")) {
    el.classList.add("form-select");
}
for (let el of document.querySelectorAll("input[type=checkbox]")) {
    el.classList.remove("form-control");
    el.classList.add("form-check-input");
    el.classList.add("mt-0");
}
