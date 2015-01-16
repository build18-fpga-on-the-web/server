$(document).ready(function() {
    board.init();

    $("#close").click(function() {
        $("#start-screen").removeClass("active");
    });

    $(".demo").click(function() {
        $.post("/demo", {"demo":this.id}, function( data ) {
            console.log("Demo post request");
            response = JSON.parse(data);
            $("#running").text("Running \"" + response["fname"] + "\"");
            $("#running").css('color', 'White');
          console.log(data);
        });

        $("#start-screen").removeClass("active");
    });


    $('#browseButton').click(function(){
        $('#file-input').click();
    });

    $('#changeButton').click(function(){
        $("#start-screen").addClass("active");
    });

    $('#file-input').change(function(){
        var filename = $(this).val().replace(/C:\\fakepath\\/i, '')
        $('#filename').val(filename);

    });


});

