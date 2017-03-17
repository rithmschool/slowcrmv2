$(function(){

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
				contentType: "application/json"
			}).then(function(response){
				console.log(response);
			});
		}
	});
});
