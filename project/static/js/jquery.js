$(function(){

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

	$(window).on('resize', function(){
      var win = $(this); //this = window
      if (win.width() > 1000) { 
      	$('.content').css('margin-top', '50px')
      	$('.searchcontent').css('margin-top', '50px')
      }
      if (win.width() < 1000) { 
      	$('.content').css('margin-top', '10vw')
      	$('.searchcontent').css('margin-top', '10vw')
      }
      if (win.width() > 1920) { 
      	$('.content').css('margin-top', '75px')
      	$('.searchcontent').css('margin-top', '75px')
      }
	});

	$('.mynavitems').on('click', function(e){
		window.location = '/users/logout';
	})

	$('#entry-form').on('submit', function(e){
		e.preventDefault()
		if($('#tweet-message').val() === ""){
			$('.flashes').prepend('<div>please enter person, company or tag</div')
		}
		else{
			$.ajax({
				type: "POST",
				url: "/users/entries",
				data: JSON.stringify({
					content: $('#tweet-message').val()
				}),
				dataType: "json",
				contentType: "application/json",
			}).then(function(response){
				console.log(response);
			}).catch(function(error){
				console.log(error)
			})
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
            $("modal-message").modal("show");
            $("#modal-message").html('<p>Succesfully sent invite!</p>');
        },
        error: function(e) {
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
