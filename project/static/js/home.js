$(function() {
  function prependLiToHome($ul, id, entry_id, name, data) {
    $ul.prepend(
      `<li class="entry" data-id="${entry_id}">
        <a class="nameanchor" href="/users/${id}">
          <div class="name">${name}
          </div>
        </a>
        <div class="text">${data}</div>
      </li>`
    );
  }
  $.ajax({
    url: "/users/entries",
    data:{
      lastentry: -1
    },
    dataType: "json",
    contentType: "application/json",
  }).then(function(response) {
  console.log(response)
    response.forEach((value, index) => {
     if (!value.archived) {
      prependLiToHome($('ul'), response[index].id,
      response[index].entry_id, response[index].name,
      response[index].data);
      }
    })
  }).then(() => {
    let reload = () => {
      let latest = $('ul li:first').data('id')
      $.ajax({
        url: "/users/entries",
        data: {
          lastentry: latest
        },
        dataType: "json",
        contentType: "application/json",
      }).then(function(response) {
        if(Array.isArray(response) && response.length > 0){
          response.forEach((value, index) => {
           if (!value.archived) {
            prependLiToHome($('ul'), response[index].id,
            response[index].entry_id, response[index].name, response[index].data)
            }
          })
        }
      })
    }
    setInterval(reload, 20000)
  })

  //Autocomplete
  var start_idx;
  var sendServer = false;
  var lookupResults;
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
            start_idx = params.query.length-2;
            sendServer = true;
          }
        }
      }
      return sendServer;
    },
    delimiter: ' ',
    lookup: function(query, done){
      $.ajax({
        url: '/users/search/autocomplete',
        data: {
          params: query.slice(start_idx)
        }
      }).then(function(response){
        lookupResults = jQuery.parseJSON(response);
        done(lookupResults);
      });
    },
  });

  //Form submission error handling
  $('#entry-form').on('submit', function(e) {
    e.preventDefault()
    if ($('#tweet-message').val() === "") {
      $('.flashes').empty().prepend(
        '<div>please enter person, company, or tag</div>'
      )
    } else {
      $.ajax({
        type: "POST",
        url: "/users/entries",
        data: JSON.stringify({
          content: $('#tweet-message').val()
        }),
        dataType: "json",
        contentType: "application/json",
      }).then(function(response) {
        $('#tweet-message').val('')
        $('ul').prepend(
          `<li class="entry" data="${response.entry_id}">
            <a class="nameanchor" href="/users/${response.id}">
              <div class="name">${response.name}
              </div>
            </a>
            <div class="text">${response.data}</div>
          </li>`
        )
      }).catch(function(error) {
        $('.flashes').empty().prepend('<div>' + JSON.parse(error.responseText).message + '</div>')
      })
    }
  });
});
