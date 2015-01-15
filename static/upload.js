$(document).ready(function() {
    $("#upload-form").submit(function(event) {
        event.preventDefault();
        $(this).ajaxSubmit();

    });
});
