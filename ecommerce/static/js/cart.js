

var updateBtns = document.getElementsByClassName("update-cart");

for (var i=0; i<updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function (){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'action:', action);

        console.log("User:", user)
        if (user === 'AnonymousUser') {
            console.log("user not logged in")
            addCookieItem(productId, action)
        } else {
            // update user order
            updateUserOrder(productId, action)
        }
    })
}


function addCookieItem(productId, action) {
    console.log('cart action:', action)

    if (action=='add') {
        if(cart[productId] == undefined) {
            cart[productId] = {'quantity': 1};
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0) {
            console.log("Removing item: ", productId)
            delete cart[productId]
        }
    }
    console.log("cart:", cart)
    // update cookie
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    // build cart

}

// call url. View will update this user's cart.
function updateUserOrder(productId, action) {
    console.log("User is logged in, updating order.")
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action,
        })
    }).then((res) => {
        return res.json();
    }).then((data) => {
        console.log("Data:", data)
        // reload page
        location.reload()
    })
}


