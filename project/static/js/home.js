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
    response.forEach((value, index) => {
     if (!value.archived) {
      prependLiToHome($('ul.entrieslist'), response[index].id,
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
});
