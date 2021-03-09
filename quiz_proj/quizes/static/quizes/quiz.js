console.log('hello quiz')
const url = window.location.href;

// the div to place questions.
const quizBox = document.getElementById('quiz-box');
// let data;

$.ajax({
    type: 'GET',
    url: `${url}data`, // matches url in urls.py
    success: function (response) {
        console.log(response)
        const data = response.data;
        // iter over questions (entries in dict.)
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {
                // display questions
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer =>{
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}"
                               name="${question}"
                               value="${answer}">
                            <label for="${question}">
                                ${answer}
                            </label>
                        </div>
                    `
                });
            }
        });
    },
    error: function (error) {
        console.log(error)
    }
});

const quizForm = document.getElementById('quiz-form');
const csrf = document.getElementsByName('csrfmiddlewaretoken');

// Get selected answers
const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')];
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value;

    elements.forEach(el => {
        if (el.checked){
            data[el.name] = el.value;
        } else {
            if (!data[el.name]) {
                // Question is not answered
                data[el.name] = null;
            }
        }
    });

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    })
}

quizForm.addEventListener('submit', e=>{
    e.preventDefault();
    sendData();
})



