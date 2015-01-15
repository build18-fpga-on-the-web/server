$(document).ready(function() {
    board.init();

    $("#close").click(function() {
        $("#start-screen").removeClass("active");
    });

    $(".demo").click(function() {
        $("#start-screen").removeClass("active");
    });
});

