const body = document.querySelector('body'),
    sidebar = body.querySelector('nav'),
    toggle = body.querySelector(".toggle"),
    modeSwitch = body.querySelector(".toggle-switch"),
    table = body.querySelector(".table"),
    runBtn = body.querySelector("#start-bot-btn"),
    attachAccountBtn = body.querySelector("#attach-account-btn"),
    removeAccountBtn = document.getElementById("remove-attach-btn");
deleteHistoryBtn = document.getElementById("delete-history-btn");
selectedMode = body.querySelector(".selectedMode").innerText


modeText = body.querySelector(".mode-text");

console.log(selectedMode);
if (selectedMode === 'dark') {
    modeText.innerText = "Light mode";
    body.classList.add("dark");
} else {
    modeText.innerText = "Dark mode";
    body.classList.remove("dark");

}

toggle.addEventListener("click", () => {
    // sidebar.classList.toggle("close");
    return

})

modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");
    table.classList.toggle("table-dark");


    if (body.classList.contains("dark")) {
        modeText.innerText = "Light mode";
    } else {
        modeText.innerText = "Dark mode";
    }

    fetch('/switch-mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            mode: 'dark'
        }),
    })
        .then(response => response.text())
        .then(data => {
            // if light mode is selected then change the mode to dark
            if (selectedMode === 'light') {

                document.body.classList.add('dark');
            } else {

                document.body.classList.remove('dark');
            }

            window.location.reload();

        });


});


runBtn.addEventListener("click", () => {
    if (is_attached_account === "False") {
        alert("Please attach your Uber account to the bot first");
        window.location.href = "/settings";
        return;
    }
    fetch('/start-bot', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => response.text())
        .then(data => {
            window.location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });

})


attachAccountBtn.addEventListener("click", () => {
    // disable the button

    fetch('/attach-account', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => response.text())
        .then(data => {
            const user_response = confirm("Please login to your Uber account and then click OK to attach your account to the bot.");
            if (user_response) {
                fetch('/confirm-attach-account', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },

                }).then(
                    response => response.text()
                ).then(data => {
                    window.location.reload();
                })


            } else {
                window.location.reload();
            }


        })
        .catch((error) => {
            console.error('Error:', error);
        });
})


removeAccountBtn.addEventListener("click", () => {
    fetch('/remove-account', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => response.text())
        .then(data => {
            window.location.reload();
            console.log(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });


})


// on click of delete history button ask for confirmation and then go to /delete-history
deleteHistoryBtn.addEventListener("click", () => {
    let confirmDelete = confirm("Are you sure you want to delete the history?");
    if (confirmDelete) {
        fetch('/delete-history', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => response.text())
            .then(data => {
                window.location.reload();
                console.log(data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
})