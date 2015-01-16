$(document).ready(function() {
    function form_response(responseText, statusText, xhr, $form)
    {
        console.log(responseText);
        console.log(typeof(responseText));
        response = JSON.parse(responseText);
        if(response["error"])
        {
            $("#form-error").text(response["message"]);
        }
        else
        {
            console.log("GOOD!");
            $("#start-screen").removeClass("active");
            $("#running").text("Running \"" + response["fname"] + ".\"");
      		$("#running").css('color', 'White');
      		$("#form-error").text("");
        }

    }

    $("#upload-form").submit(function(event) {
        event.preventDefault();
        $(this).ajaxSubmit({"success":form_response});

    });
});
