$(function(){

  //Entry Autocomplete
  var sendServer = false;
  $('#tweet-message').autocomplete({
    deferRequestBy: 200,
    ajaxSettings: {
      beforeSend: function(xhr) {
        xhr.setRequestHeader('X-Requested-With', 'XMLHTTPRequest');
      }
    },
    onSearchStart: function(params) {
      if(params.query.length == 2){
        if(['|', '$', '*'].includes(params.query.slice(-2,-1))) {
          if(sendServer){
            sendServer = false;
            $('#tweet-message').autocomplete('hide');
          } else {
            sendServer = true;
          }
        }
      }
    },
    delimiter: ' ',
    tabDisabled: false,
    autoSelectFirst: true,
    lookup: function(query, done){
      $.ajax({
        url: '/tags/autocomplete',
        data: {
          params: query.slice(0),
          specialchars: 1
        }
      }).then(function(response){
        var lookupResults = jQuery.parseJSON(response);
        done(lookupResults);
      });
    },
  });

  //Entry form submission error handling
  $('#entry-form').on('submit', function(e) {
    e.preventDefault()
    var re = /\B\*\s*\*\B|\B\|\s*\|\B|\B\$\s*\$\B/;
    if ($('#tweet-message').val() === "") {
      $('.flashes').empty().prepend(
        '<div>please enter person, company, or tag</div>'
      )
    }else if($('#tweet-message').val().match(re)){
      $('.flashes').empty().prepend(
        '<div>please enter a non-empty tag</div>'
      )
    }else {
      $.ajax({
        type: "POST",
        url: "/users/entries",
        data: JSON.stringify({
          content: $('#tweet-message').val()
        }),
        dataType: "json",
        contentType: "application/json",
      }).then(function(response) {
        $('#tweet-message').val('');
        $('.entrieslist').prepend(
          `<li class="entry" data-id="${response.entry_id}">
            <a class="nameanchor" href="/users/${response.id}">
              <div class="name">${response.name}
              </div>
            </a>
            <div class="text">${response.data}</div>
            <div class="date">${response.time}</div>
          </li>`
        )
        $('#new-modal').modal('toggle');
        $('.flashes').html("<p></p>");
      }).catch(function(error) {
        $('.flashes').prepend('<div>' + JSON.parse(error.responseText).message + '</div>')
      })
      // If user is not on home page, redirect to home page on post
      if(window.location.pathname !== "/users/home"){
        window.location.pathname = "/users/home";
      };

    }
  });


  //Tag Autocomplete
  $('#tag').autocomplete({
    ajaxSettings: {
      beforeSend: function(xhr) {
        xhr.setRequestHeader('X-Requested-With', 'XMLHTTPRequest');
      }
    },
    lookup: function(query, done){
      $.ajax({
        url: '/tags/autocomplete',
        data: {
          params: query
        }
      }).then(function(response){
        var lookupResults = jQuery.parseJSON(response);
        done(lookupResults);
      });
    }
  });



  // toggle +/- on collapse

  $(".people-button").click(function(){
    if($("#persons").hasClass("collapsing") !== true){
      $(this).find('i').toggleClass('fa-plus fa-minus')
    }
  })

  $(".companies-button").click(function(){
    if($("#companies").hasClass("collapsing") !== true){
      $(this).find('i').toggleClass('fa-plus fa-minus')
    }
  })

  $(".entries-button").click(function(){
    if($("#entries").hasClass("collapsing") !== true){
      $(this).find('i').toggleClass('fa-plus fa-minus')
    }
  })

});
