$(function() {

    $.ajax({
        type: "POST",
        url: "/users/loadentries",
        data: JSON.stringify("initial"),
        dataType: "json",
        contentType: "application/json",
    }).then(function(response) {
        response.forEach((value, index) => {
            $('ul').prepend(`<li class="entry" data="${response[index].entry_id}">
                                <a class="nameanchor" href="/users/${response[index].id}">
                                    <div class="name">${response[index].name}
                                    </div>
                                </a>
                                <div class="text">${response[index].data}</div>
                            </li>`)
        })
    }).then(() => {
        let reload = () => {
            let latest = $('ul li:first').attr('data')
                $.ajax({
                    type: "POST",
                    url: "/users/loadentries",
                    data: JSON.stringify(latest),
                    dataType: "json",
                    contentType: "application/json",
                }).then(function(response) {
                    if(response[0].id !== 0){
                        response.forEach((value, index) => (
                            $('ul').prepend(`<li class="entry" data="${response[index].entry_id}">
                                                <a class="nameanchor" href="/users/${response[index].id}">
                                                    <div class="name">${response[index].name}
                                                    </div>
                                                </a>
                                                <div class="text">${response[index].data}</div>
                                            </li>`)
                        ))
                    }
                })
        }
        setInterval(reload, 20000)
    })

    $('#entry-form').on('submit', function(e) {
        e.preventDefault()
        if ($('#tweet-message').val() === "") {
            $('.flashes').prepend('<div>please enter person, company or tag</div>')
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
                $('ul').prepend(`<li class="entry" data="${response.entry_id}">
                                    <a class="nameanchor" href="/users/${response.id}">
                                        <div class="name">${response.name}
                                        </div>
                                    </a>
                                    <div class="text">${response.data}</div>
                                </li>`)
            }).catch(function(error) {
                $('.flashes').prepend('<div>' + JSON.parse(error.responseText).message + '</div>')
            })
        }
    });

});
