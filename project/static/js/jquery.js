$(function(){

	console.log("This loaded")

	$('.searchicon').on('click', function(e){
		if ($('.mobilenavpages').css('display').toLowerCase() == 'none'){
			$('.mobilenavpages').show()
			$('.content').css('margin-top', '0px')
			$('.searchcontent').css('margin-top', '0px')
		}else{
			$('.mobilenavpages').hide()
			$('.content').css('margin-top', '10vw')
			$('.searchcontent').css('margin-top', '10vw')
		}
	})

	$('.hamburgericon').on('click', function(e){
		if ($('.mobilesearch').css('display').toLowerCase() == 'none'){
			$('.mobilesearch').show()
			$('.content').css('margin-top', '0px')
			$('.searchcontent').css('margin-top', '0px')
		}else{
			$('.mobilesearch').hide()
			$('.content').css('margin-top', '10vw')
			$('.searchcontent').css('margin-top', '10vw')
		}
	})

	$('.mobileinput').on('input',function(e){
 		if($('.mobileinput').val() !== ''){
 			$('.content').css("display", "none");
			$('.searchcontent').css("display", "block");
 		}else{
 			$('.searchcontent').css("display", "none");
			$('.content').css("display", "block");
 		}
	});

	$('.searchcontent').hide()

	$('.myinput').on('input',function(e){
 		if($('.myinput').val() !== ''){
 			$('.content').css("display", "none");
			$('.searchcontent').css("display", "block");
 		}else{
 			$('.searchcontent').css("display", "none");
			$('.content').css("display", "block");
 		}
	});

// Invite User Modal Form
$(function() {

$("#invite-modal-submit").on('click', function(e) {
    e.preventDefault();
    $("#modal-message").html('<p>This might take a moment...</p>');
    var email = $("#invite-email").val();
    var name = $("#invite-name").val();
    $.ajax({
        type: "POST",
        url: "/users/invite",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({name: name, email: email}),
        success: function(response) {
            console.log(response)
            $("modal-message").modal("show");
            $("#modal-message").html('<p>Succesfully sent invite!</p>');
        },
        error: function(e) {
            console.log(e)
            if (JSON.parse(e.responseText) === "Missing form info") {
                $("#modal-message").html('<span style="color:red">Please fill in name and email</span>');
                }
            if (JSON.parse(e.responseText) === "Email already exists") {
                $("#modal-message").html('<span style="color:red">Invite already sent to this email</span>');
                $("modal-message").modal("show")
            }
        }
    });
    });
});



});
