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

});
