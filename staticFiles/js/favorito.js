document.addEventListener('DOMContentLoaded', function() {
    const favoritoBtn = document.getElementById('favorito');
    const csrftoken = getCookie('csrftoken');
    const userAuthenticated = favoritoBtn.getAttribute('data-authenticated') === 'True';

    favoritoBtn.addEventListener('click', function(event) {
        event.preventDefault();
        if (!userAuthenticated) {
            window.location.href = '/usuarios/login/';
            return;
        }
        fetch(favoritoBtn.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.favorito) {
                favoritoBtn.innerHTML = '<i class="fas fa-heart" style="color: red;"></i>';
            } else {
                favoritoBtn.innerHTML = '<i class="far fa-heart"></i>';
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}