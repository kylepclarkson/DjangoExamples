console.log("hello js")

const spinner = document.getElementById('spinner')
const tableBody = document.getElementById('table-body-box')
const url = window.location.href



$.ajax({
    type: 'GET',
    url: '/data-json/',
    success: function (response){
        console.log(response)
        // convert data to json object
        const data = JSON.parse(response.data)
        console.log(data)
        data.forEach(el=>{
            console.log(el.fields)
            // inject html into table body
            tableBody.innerHTML += `
                <tr>
                    <td>${el.pk}</td>
                    <td><img src=media/${el.fields.item} height="200px" width="200px"></img></td>
                    <td>${el.fields.info}</td>
                </tr>    
            `
        })
        // make spinner not visible once data is loaded.
        spinner.classList.add('not-visible')
    },
    error: function (error) {
        console.log(error)
    }

})