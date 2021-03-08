console.log("Hello")

// Get buttons as array.
const modalBtns = [...document.getElementsByClassName('modal-button')];
// Get modal body
const modalBody = document.getElementById('modal-body-confirm');
// start quiz button
const startBtn = document.getElementById('start-btn"');
const url = window.location.href

// Add click event listener to each button
modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    // Get data from attributes
    const pk = modalBtn.getAttribute('data-pk');
    const name = modalBtn.getAttribute('data-quiz');
    const numQuestions = modalBtn.getAttribute('data-questions');
    const difficulty = modalBtn.getAttribute('data-pass');
    const scoreToPass = modalBtn.getAttribute('data-pass');
    const time = modalBtn.getAttribute('data-time');

    // inject data into modal.
    modalBody.innerHTML = `
        <div class="h5 mb-3">
            Are you sure you want to start <b>${name}</b>
        </div>
        <div class="text-muted">
            <ul>
                <li>Difficulty: <b>${difficulty}</b></li>
                <li>Questions: <b>${numQuestions}</b></li>
                <li>Score to pass: <b>${scoreToPass}%</b></li>     
                <li>Time: <b>${time} mins</b></li>     
            </ul>
        </div>       
    `
    // on click, redirect to url
    startBtn.addEventListener('click', ()=>{
        // set the url to quiz
        window.location.href = url + pk
    })
}));
