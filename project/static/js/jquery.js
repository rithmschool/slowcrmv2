$(function(){

	$('.searchcontent').hide()

	$('.myinput').on('input',function(e){
		console.log($('.myinput').val())
 		if($('.myinput').val() !== ''){
 			$('.content').css("display", "none");
			$('.searchcontent').css("display", "block");
 		}else{
 			$('.searchcontent').css("display", "none");
			$('.content').css("display", "block");
 		}
	});

<<<<<<< HEAD


	$('#entry-form').on('submit', function(e){
		e.preventDefault()
		$.ajax({
			type: "POST",
			url: "/users/entries",
			data: JSON.stringify({
				content: $('#tweet-message').val()
			}),
			dataType: "json",
			contentType: "application/json"
		}).then(function(response){
			debugger
		});
		// $.post("/users/entries", 
		// 	{
		// 		content: `$($('#tweet-message').val())`
		// 	},function(data){

		// 	})
			
	});
	

});
=======
	$('.mynavitems').on('click', function(e){
		window.location = '/users/logout';
	})

});
>>>>>>> adbcb6d788d08c3987c16f0be818c4538fbfd6fd
