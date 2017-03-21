$(function() {

    $.ajax({
        type: "POST",
        url: "/users/loadentries",
        data: JSON.stringify({
            content: 'initial'
        }),
        dataType: "json",
        contentType: "application/json",
    }).then(function(response) {
        response.forEach((v, i, a) => (
            $('ul').prepend('<li class="entry" data="' + response[i].entry_id + '">' + 
            '<a class="nameanchor" href="/users/' + response[i].id + '"><div class="name">' + response[i].name +
            '</div></a>' + '<div class="text">' + response[i].data + '</div>' + '</li>')
        ))
    }).then(() => {
        let reload = () => {
            console.log('Checking for updates')
            let latest = $('ul li:first').attr('data')
                $.ajax({
                    type: "POST",
                    url: "/users/loadentries",
                    data: JSON.stringify({
                        content: latest
                    }),
                    dataType: "json",
                    contentType: "application/json",
                }).then(function(response) {
                    if(response[0].id !== 0){
                        response.forEach((v, i, a) => (
                            $('ul').prepend('<li class="entry" data="' + response[i].entry_id + '">' + 
                            '<a class="nameanchor" href="/users/' + response[i].id + '"><div class="name">' + response[i].name +
                            '</div></a>' + '<div class="text">' + response[i].data + '</div>' + '</li>')
                        ))
                        console.log('Page Updated')
                    }else{
                        console.log('No New Updates')
                    }
                })
        }
        setInterval(reload, 10000)
    })


    let $content = $('.content');
    let $searchContent = $('.searchcontent');

    $('.searchicon').on('click', function(e) {
        if ($('.mobilenavpages').css('display').toLowerCase() == 'none') {
            $('.mobilenavpages').show()
            $content.css('margin-top', '0px')
            $searchContent.css('margin-top', '0px')
        } else {
            $('.mobilenavpages').hide()
            $content.css('margin-top', '10vw')
            $searchContent.css('margin-top', '10vw')
        }
    })

    $('.hamburgericon').on('click', function(e) {
        if ($('.mobilesearch').css('display').toLowerCase() == 'none') {
            $('.mobilesearch').show()
            $content.css('margin-top', '0px')
            $searchContent.css('margin-top', '0px')
        } else {
            $('.mobilesearch').hide()
            $content.css('margin-top', '10vw')
            $searchContent.css('margin-top', '10vw')
        }
    })

    $(window).on('resize', function() {
        var win = $(this); //this = window
        if (win.width() > 1000) {
            $content.css('margin-top', '50px')
            $searchContent.css('margin-top', '50px')
        }
        if (win.width() < 1000) {
            $content.css('margin-top', '10vw')
            $searchContent.css('margin-top', '10vw')
        }
        if (win.width() > 1920) {
            $content.css('margin-top', '75px')
            $searchContent.css('margin-top', '75px')
        }
    });

    $('.mynavitems').on('click', function(e) {
        window.location = '/users/logout';
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
                $('ul').prepend('<li class="entry" data="' + response.entry_id + '">' + 
                '<a class="nameanchor" href="/users/' + response.id + '"><div class="name">' + response.name +
                '</div></a>' + '<div class="text">' + response.data + '</div>' + '</li>')
            }).catch(function(error) {
                $('.flashes').prepend('<div>' + JSON.parse(error.responseText).message + '</div>')
            })
        }
    });


    // Invite User Modal Form


    $("#invite-modal-submit").on('click', function(e) {
        e.preventDefault();
        $("#modal-message").html('<p>This might take a moment...</p>');
        var email = $("#invite-email").val();
        var name = $("#invite-name").val();
        $.ajax({
            type: "POST",
            url: "/users/invite",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({ name: name, email: email }),
            success: function(response) {
                $("modal-message").modal("show");
                $("#modal-message").html('<p>Succesfully sent invite!</p>');
            },
            error: function(e) {
                if (JSON.parse(e.responseText) === "Missing form info") {
                    $("#modal-message").html('<span style="color:red">Please fill in name and email</span>');
                }
                if (JSON.parse(e.responseText) === "Email already exists") {
                    $("#modal-message").html('<span style="color:red">Invite already sent to this email</span>');
                    $("modal-message").modal("show")
                }
            }
        });
    });




});
