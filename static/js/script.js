let messages = document.getElementById('msg');
let alert = new bootstrap.Alert(messages);

/*
Wait for DOM to finish loading before adding event listeners 
and displaying the welcome modal
*/
$(document).ready(function () {
    $('#like').submit(toggleLike);
    $('#save').submit(toggleSave);
});

function toggleLike(e) {
    e.preventDefault();
    // Get form action attribute
    const likeFormAction = $(this).attr('action');
    // Get csrf token
    const csrfToken = $(this).find("input[name='csrfmiddlewaretoken']").val();
    // Get like button text
    const likeBtnText = $(this).find("span[id='like-button-text']");
    // Get like icon
    const likeIcon = $(this).find("i[id='like-icon']");
    // Get total likes span
    const totalLikesSpan = $("#total-likes");
    // Get total likes value
    const totalLikesVal = parseInt(totalLikesSpan.text());

    // post like form
    $.post(likeFormAction,
        {
            'csrfmiddlewaretoken': csrfToken,
        },
        // change html elements
        function(){
            if (likeIcon.hasClass("fas")) {
                likeIcon.addClass("far").removeClass("fas");
                likeBtnText.text(" Like");
                totalLikesSpan.text(totalLikesVal - 1);
            } else if (likeIcon.hasClass("far")) {
                likeIcon.addClass("fas").removeClass("far");
                likeBtnText.text(" Liked");
                totalLikesSpan.text(totalLikesVal + 1);
            }
        }
    );
}

function toggleSave(e) {
    e.preventDefault();
    // Get form action attribute
    const saveFormAction = $(this).attr('action');
    // Get csrf token
    const csrfToken = $(this).find("input[name='csrfmiddlewaretoken']").val();
    // Get like button text
    const saveBtnText = $(this).find("span[id='save-button-text']");
    // Get like icon
    const saveIcon = $(this).find("i[id='save-icon']");

    // post save form
    $.post(saveFormAction,
        {
            'csrfmiddlewaretoken': csrfToken,
        },
        // change html elements
        function(){
            if (saveIcon.hasClass("fas")) {
                saveIcon.addClass("far").removeClass("fas");
                saveBtnText.text(" Save");
            } else if (saveIcon.hasClass("far")) {
                saveIcon.addClass("fas").removeClass("far");
                saveBtnText.text(" Saved");
            }
        }
    );
}

// timer to dismiss messages
setTimeout(function() {
    alert.close();
}, 3000);
