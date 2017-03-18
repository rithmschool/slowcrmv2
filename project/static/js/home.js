$(function(){

	let $content = $('content').css
	let $searchContent = $('searchcontent').css

	$('.searchicon').on('click', function(e){
		if ($('.mobilenavpages').css('display').toLowerCase() == 'none'){
			$('.mobilenavpages').show()
			$content.('margin-top', '0px')
			$searchContent.('margin-top', '0px')
		}else{
			$('.mobilenavpages').hide()
			$content.('margin-top', '10vw')
			$searchContent.('margin-top', '10vw')
		}
	})

	$('.hamburgericon').on('click', function(e){
		if ($('.mobilesearch').css('display').toLowerCase() == 'none'){
			$('.mobilesearch').show()
			$content.('margin-top', '0px')
			$searchContent.('margin-top', '0px')
		}else{
			$('.mobilesearch').hide()
			$content.('margin-top', '10vw')
			$searchContent.('margin-top', '10vw')
		}
	})

	$(window).on('resize', function(){
      var win = $(this); //this = window
      if (win.width() > 1000) { 
      	$content.('margin-top', '50px')
      	$searchContent.('margin-top', '50px')
      }
      if (win.width() < 1000) { 
      	$content.('margin-top', '10vw')
      	$searchContent.('margin-top', '10vw')
      }
      if (win.width() > 1920) { 
      	$content.('margin-top', '75px')
      	$searchContent.('margin-top', '75px')
      }
	});

	setInterval(loadEntries, 600000)

	function loadEntries(){
		$.ajax({
	      type: "POST",
	      url: "",
	      data: myDataVar.toString(),
	      dataType: "text",
	      success: function(resultData){
	          alert("Save Complete");
	      }
	});
	}

});

