

var updateBtns = document.getElementsByClassName("update-cart");

for (var i=0; i<updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function (){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'action:', action);

        console.log("User:", user)
        if (user === 'AnonymousUser') {
            console.log("user not logged in")
        } else {
            // update user order
            updateUserOrder(productId, action)
        }
    })
}

// call url. View will update this user's cart.
function updateUserOrder(productId, action) {
    console.log("User is logged in, updating order.")
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action,
        })
    }).then((res) => {
        return res.json();
    }).then((data) => {
        console.log("Data:", data)
    })
}


