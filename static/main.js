$(document).ready(function() {
    board.init();

    $("#close").click(function() {
        $("#start-screen").removeClass("active");
    });

    $(".demo").click(function() {
        $("#start-screen").removeClass("active");
    });


    $('#browseButton').click(function(){
        $('#file-input').click();
    });
    
    $('#file-input').change(function(){
        var filename = $(this).val().replace(/C:\\fakepath\\/i, '')
        $('#filename').val(filename);

    });

    
});

