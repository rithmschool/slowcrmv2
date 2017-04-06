$(function(){
  //Entry Autocomplete
  var sendServer = false;
  $('#tweet-message').autocomplete({
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
    var re = /[**,$$,||]{2}/;
    if ($('#tweet-message').val() === "") {
      $('.flashes').empty().prepend(
        '<div>please enter person, company, or tag</div>'
      )
    }else if($('#tweet-message').val().match(re)){
      $('.flashes').empty().prepend(
        '<div>please enter a correct tag</div>'
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
        $('ul').prepend(
          `<li class="entry" data-id="${response.entry_id}">
            <a class="nameanchor" href="/users/${response.id}">
              <div class="name">${response.name}
              </div>
            </a>
            <div class="text">${response.data}</div>
          </li>`
        )
        $('#new-modal').modal('toggle');
        $('.flashes').html("<p></p>");
      }).catch(function(error) {
        $('.flashes').prepend('<div>' + JSON.parse(error.responseText).message + '</div>')
      })
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
});
