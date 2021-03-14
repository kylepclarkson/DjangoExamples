console.log('hello quiz')
const url = window.location.href;

// the div to place questions.
const quizBox = document.getElementById('quiz-box');
const scoreBox = document.getElementById('score-box');
const resultBox = document.getElementById('result-box');

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

    // Pass data (questions and answers) to save view
    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function (response) {
            // console.log(response);
            const results = response.results;
            console.log(results)
            quizForm.classList.add('not-visible');

            scoreBox.innerHTML = `${response.passed ? 'You passed!' : "You failed!"} Your score is: ${response.score}%.`

            // display results for each question
            results.forEach(res => {
                const resDiv = document.createElement("div");
                for (const [question, response]  of Object.entries(res)) {
                    // console.log(question)
                    // console.log(response)

                    resDiv.innerHTML += question
                    // classes
                    const cls = ['container', 'p-3', 'text-light', 'h3']
                    resDiv.classList.add(...cls)

                    if (response == 'not answered') {
                        resDiv.innerHTML += '- not answered';
                        resDiv.classList.add('bg-danger');
                    } else {
                        const answer = response['answered']
                        const correct = response['correct_answer']

                        if (answer == correct) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` answered: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | correct answer: ${correct}`
                            resDiv.innerHTML += ` | answered: ${answer}`
                        }
                    }

                    // add div to body
                    // const body = document.getElementsByTagName('BODY')[0]
                    resultBox.append(resDiv)
                }
            })
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



