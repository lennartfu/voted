$(document).ready(function() {
    $("textarea").addClass("form-control").attr("rows", 2);

    $("select").addClass("form-select");

    $("input").addClass("form-control");

    $("input[type=checkbox]").removeClass("form-control").addClass("form-check-input mt-0");

    $("label").addClass("input-group-text px-3");
});
