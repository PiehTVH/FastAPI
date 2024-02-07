
async function add_booking(room_id, hotel_id, block_id) {
    const url = "/bookings";
    const date_from = document.getElementById("date_from").value;
    const date_to = document.getElementById("date_to").value;
    let myDiv = document.getElementById('nav_box');
    let myDiv_1 = document.getElementById(block_id);
    await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            room_id: room_id,
            date_from: date_from,
            date_to: date_to
        }),
    }).then(response => {
        if (response.status === 200) {

            alert("Номер добавлен в корзину");

            var url_1 = 'pages/hotels/' + hotel_id + '/rooms?date_from=' + date_from + '&date_to=' + date_to;
            fetch('pages/bookings')
                .then(response => response.text())
                .then(data => { myDiv.innerHTML = data, htmx.process(myDiv); });
            fetch(url_1)
                .then(response => response.text())
                .then(data => { myDiv_1.innerHTML = data, htmx.process(myDiv_1); });
                
        }
        else if (response.status === 401) {
            alert("Войдите в систему");
            }
        else if (response.status === 409) {
            alert("Не осталось свободных номеров");
        }

    });
    refresh_nav();
}


function cancel(val) {
    let obj = document.getElementById(val);
    obj.style.display = "none";
}


async function loginUser() {
    const wrongCredentialsSpan = document.getElementById("wrong_credentials");
    wrongCredentialsSpan.textContent = "";

    const url = "/auth/login";
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    let myDiv = document.getElementById('nav_box');
    await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, password: password }),
    }).then(response => {
        if (response.status === 200) {
            //window.location.href = "/pages/bookings"
            var url = "/pages/bookings";
            fetch(url)
                .then(response => response.text())
                .then(data => { myDiv.innerHTML = data, htmx.process(myDiv); });
            cancel("logpanel");
            refresh_panel();

        } else {
            wrongCredentialsSpan.textContent = "Неверный email или пароль";
        }
    });
}


async function logoutUser() {
    const url = "/auth/logout";

    await fetch(url, {
        method: 'POST',
    }).then(response => {
        if (response.status === 200) {
            window.location.href = "/pages"
        }
    });
}


async function regUser() {
    const wrongCredentialsSpan = document.getElementById("wrong_credentials");
    wrongCredentialsSpan.textContent = "";
    let email_pole = document.getElementById("email");
    let password_pole = document.getElementById("password");
    let button = document.getElementById("log_button");
    let l_pass = document.getElementById("l_pass");
    let l_em = document.getElementById("l_em");
    const url = "/auth/register";
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    if (email == "" || password == "") {
        wrongCredentialsSpan.textContent = "Не введён email или пароль";
    }
    else {
        await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password }),
        }).then(response => {
            if (response.status === 200) {
                wrongCredentialsSpan.textContent = "Вы зарегистрированы. Войдите в систему.";
                button.style.display = "none";
                email_pole.style.display = "none";
                password_pole.style.display = "none";
                l_pass.style.display = "none";
                l_em.style.display = "none";
            } else if (response.status === 409) {
                wrongCredentialsSpan.textContent = "Пользователь с таким логином уже существует";
            } else {
                wrongCredentialsSpan.textContent = "Ошибка регистрации";
            }
        });
    }
}


async function refresh_nav(){
    let myDiv = document.getElementById('nav_box');
    fetch('pages/bookings')
        .then(response => response.text())
        .then(data => { myDiv.innerHTML = data, htmx.process(myDiv); } );
}


async function refresh_anon_nav(){
    let myDiv = document.getElementById('nav_box');
    fetch('pages/anon_bookings')
        .then(response => response.text())
        .then(data => { myDiv.innerHTML = data, htmx.process(myDiv); } );
}


async function refresh_my_bookings(){
    let myDiv = document.getElementById('bookings_list');
    fetch('pages/my_bookings')
        .then(response => response.text())
        .then(data => { myDiv.innerHTML = data, htmx.process(myDiv); } );
}

async function refresh_my_cart(){
    let myDiv = document.getElementById('bookings_list');
    fetch('pages/cart')
        .then(response => response.text())
        .then(data => { myDiv.innerHTML = data, htmx.process(myDiv); } );
}

async function refresh_panel(){
    let myDiv = document.getElementById('anon_cart');
    let myDiv_1 = document.getElementById('bookings_list');
    if (myDiv != null) {
    fetch('pages/cart')
        .then(response => response.text())
        .then(data => { myDiv.innerHTML = data, htmx.process(myDiv_1); } );
}}

async function refresh_anon_cart(){
    let myDiv = document.getElementById('bookings_list');
    fetch('pages/cart/anon')
        .then(response => response.text())
        .then(data => { myDiv.innerHTML = data, htmx.process(myDiv); } );
}

async function add_cart(room_id, hotel_id, block_id) {
    const url = "/cart";
    const date_from = document.getElementById("date_from").value;
    const date_to = document.getElementById("date_to").value;
    let myDiv = document.getElementById('nav_box');
    let myDiv_1 = document.getElementById(block_id);
    await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            room_id: room_id,
            date_from: date_from,
            date_to: date_to
        }),
    }).then(response => {
        if (response.status === 201) {
            alert("Номер добавлен в корзину");
            var url_1 = 'pages/hotels/' + hotel_id + '/rooms?date_from=' + date_from + '&date_to=' + date_to;
            fetch(url_1)
                .then(response => response.text())
                .then(data => { myDiv_1.innerHTML= data, htmx.process(myDiv_1); });
            refresh_nav();
        }
        else if (response.status === 401) {
            fetch("/cart/anon", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    room_id: room_id,
                    date_from: date_from,
                    date_to: date_to
                }),
            }).then(response => {
                if (response.status === 201) {
                    alert("Номер добавлен в корзину");
                    fetch('pages/anon_bookings')
                    .then(response => response.text())
                    .then(data => { myDiv.innerHTML = data, htmx.process(myDiv); });     
                }
        });}
        else if (response.status === 409) {
            alert(response.statusText);
        }

    });
    
}

async function book_all_checked(){
    var choice = []
    var choice_list = document.getElementsByClassName('choice');
    for (var i = 0; i < choice_list.length; i++) {
        if (choice_list[i].checked) {
            const strng = choice_list[i].value.split('/');
            strng.push(choice_list[i].name)
            choice.push(strng);
        }
    }
    url = "/bookings";
    for (let i = 0; i < choice.length; i++) {
        
        
        await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                room_id: Number(choice[i][0]),
                date_from: choice[i][1],
                date_to: choice[i][2]
            }),
        }).then(response => {});

        url_1 = "/cart/" + choice[i][3];
        await fetch(url_1, {method: 'DELETE'})
        .then(response => {});

        let myDiv = document.getElementById('bookings_list');
        await fetch('pages/cart')
        .then(response => response.text())
        .then(data => { myDiv.innerHTML = data, htmx.process(myDiv); } );
        
}
       refresh_nav();
}


async function add_fav(room_id, hotel_id, block_id) {
    const url = "/fav";
    const date_from = document.getElementById("date_from").value;
    const date_to = document.getElementById("date_to").value;
    let myDiv = document.getElementById('nav_box');
    let myDiv_1 = document.getElementById(block_id);
    await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            id: room_id,
        }),
    }).then(response => {
        if (response.status === 201) {
            var url_1 = 'pages/hotels/' + hotel_id + '/rooms?date_from=' + date_from + '&date_to=' + date_to;
            fetch(url_1)
            .then(response => response.text())
            .then(data => { myDiv_1.innerHTML = data, htmx.process(myDiv_1)});
            refresh_nav();
        }
        else if (response.status === 401) {
            fetch("/fav/anon", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    id: room_id,
                }),
            }).then(response => {
                if (response.status === 201) {
                    var url_1 = 'pages/hotels/' + hotel_id + '/rooms?date_from=' + date_from + '&date_to=' + date_to;
                    fetch(url_1)
                    .then(response => response.text())
                    .then(data => { myDiv_1.innerHTML = data, htmx.process(myDiv_1); });
                    refresh_anon_nav();     
                }
        });}
        else if (response.status === 409) {
            alert(response.statusText);
        }

    })
    
}

