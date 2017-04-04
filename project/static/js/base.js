$(function(){
    $('.modal').on('shown.bs.modal', function() {
        $(this).find('[autofocus]').focus();
    });
    $(".modal").on("hidden.bs.modal", function(){
        $("#tweet-message").val("");
    });
});

$(function(){
    $('.tags_select span').click(function() {
         var value = $(this).text()[0];
         var input = $('#tweet-message');
         input.focus();
         input.val(input.val() + value + value);
         var position = input.val().length-1;
         input[0].setSelectionRange(position,position);
         return false;
     });
});

$(function() {
    let $content = $('.content');
    let $searchContent = $('.searchcontent');
    let $modalMessage = $('#modal-message')

    // Invite User Modal Form
    $("#invite-modal-submit").on('click', function(e) {
        e.preventDefault();
        input.focus();
        $modalMessage.html('<p>One moment...</p>');
        var email = $("#invite-email").val();
        var name = $("#invite-name").val();
        $.ajax({
            type: "POST",
            url: "/users/invite",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({ name, email })
        }).then(function(response) {
            function sent(){
              $modalMessage.html('<p></p>');
              $("#invite-modal").modal('toggle');
            }
            $modalMessage.html('<p style="color:green">Successfully sent invite!</p>');
            $(".invite-modal-form").trigger('reset');
            setTimeout(sent, 2000)
        }).catch(function(e) {
            if (JSON.parse(e.responseText) === "Missing form info") {
                $modalMessage.html('<span style="color:red">Please fill in name and email</span>');
            }
        })
    });
});
