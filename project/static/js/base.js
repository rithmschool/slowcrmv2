$(function() {

    let $content = $('.content');
    let $searchContent = $('.searchcontent');
    let $mobileSearch = $('.mobilesearch')
    let $searchIcon = $('.searchicon')
    let $mobileNav = $('.mobilenavpages')
    let $hamburger = $('.hamburgericon')
    let $modalMessage = $("#modal-message")

    $searchIcon.on('click', function(e) {
        if ($mobileNav.css('display').toLowerCase() == 'none') {
            $mobileNav.show()
            $content.css('margin-top', '0px')
            $searchContent.css('margin-top', '0px')
        } else {
            $mobileNav.hide()
            $content.css('margin-top', '10vw')
            $searchContent.css('margin-top', '10vw')
        }
    })

    $hamburger.on('click', function(e) {
        if ($mobileSearch.css('display').toLowerCase() == 'none') {
            $mobileSearch.show()
            $content.css('margin-top', '0px')
            $searchContent.css('margin-top', '0px')
        } else {
            $mobileSearch.hide()
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

        // Invite User Modal Form


    $("#invite-modal-submit").on('click', function(e) {
        e.preventDefault();
        $modalMessage.html('<p>One moment...</p>');
        var email = $("#invite-email").val();
        var name = $("#invite-name").val();
        $.ajax({
            type: "POST",
            url: "/users/invite",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({ name, email })
        }).then(function(response) {
                $modalMessage.html('<p>Succesfully sent invite!</p>');
        }).catch(function(e) {
                if (JSON.parse(e.responseText) === "Missing form info") {
                    $modalMessage.html('<span style="color:red">Please fill in name and email</span>');
                }
        })
    });
});
