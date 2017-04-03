$(function(){
  var sendServer = false;
  var lookupResults;
  $('#tag').autocomplete({
    ajaxSettings: {
      beforeSend: function(xhr) {
        xhr.setRequestHeader('X-Requested-With', 'XMLHTTPRequest');
      }
    },
    onSearchStart: function(params) {
      return true;
    },
    lookup: function(query, done){
      $.ajax({
        url: '/companies/tags/autocomplete',
        data: {
          params: query
        }
      }).then(function(response){
        lookupResults = jQuery.parseJSON(response);
        done(lookupResults);
      });
    },
  });
});


$(function(){
  var sendServer = false;
  var lookupResults;
  $('#tag').autocomplete({
    ajaxSettings: {
      beforeSend: function(xhr) {
        xhr.setRequestHeader('X-Requested-With', 'XMLHTTPRequest');
      }
    },
    onSearchStart: function(params) {
      return true;
    },
    lookup: function(query, done){
      $.ajax({
        url: '/persons/tags/autocomplete',
        data: {
          params: query
        }
      }).then(function(response){
        lookupResults = jQuery.parseJSON(response);
        done(lookupResults);
      });
    },
  });
});
