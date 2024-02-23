const body = document.querySelector('body'),
    sidebar = body.querySelector('nav'),
    toggle = body.querySelector(".toggle"),
    modeSwitch = body.querySelector(".toggle-switch"),
    table = body.querySelector(".table"),
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

        });


});