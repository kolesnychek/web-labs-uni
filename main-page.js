const OPEN_CLASSNAME = "open";
const navLinks = document.getElementById("nav-links");

function toggleMenu() {
    navLinks.classList.toggle(OPEN_CLASSNAME);
}

var header = document.getElementById("headernav");
window.onscroll = function(){
    if (window.pageYOffset > header.offsetTop) {
        header.classList.add("sticky");
    }
    else {
        header.classList.remove("sticky");
    }
}


const actualphotos = document.getElementsByClassName('actual-photo');
const hiddenactuals = document.getElementsByClassName('hidden-actual');

for (let i = 0; i < actualphotos.length; i++) {
    actualphotos[i].addEventListener('mouseover', function() {
        hiddenactuals[i].style.display = 'flex';
    });
    
    actualphotos[i].addEventListener('mouseout', function() {
        hiddenactuals[i].style.display = 'none';
    });    
}

const catalogphotos = document.getElementsByClassName('katalog-photo');
const hiddencatalog = document.getElementsByClassName('hidden-katalog');

for (let i = 0; i < catalogphotos.length; i++) {
    catalogphotos[i].addEventListener('mouseover', function() {
        hiddencatalog[i].style.display = 'flex';
    });
    
    catalogphotos[i].addEventListener('mouseout', function() {
        hiddencatalog[i].style.display = 'none';
    });    
}

const arrowhrefs = document.getElementsByClassName('arrow-href');
const answershidden = document.getElementsByClassName('answer-right');

let isTargetVisible = false;

for (let i = 0; i < arrowhrefs.length; i++) {
    arrowhrefs[i].addEventListener('click', function() {
        if (isTargetVisible) {
            answershidden[i].style.display = 'none';
            isTargetVisible = false;
        } else {
            answershidden[i].style.display = 'block';
            isTargetVisible = true;
        }
    });
}

//Cart

const cartIcon = document.querySelector('.button-basket');
const autoIcon = document.querySelector('.button-auto');
const cart = document.querySelector('.cart');
const closeCart = document.querySelector('.close-cart');

cartIcon.onclick = () => {
    cart.classList.add("active");
    cartIcon.style["opacity"] = 0;
    autoIcon.style["opacity"] = 0;
}

closeCart.onclick = () => {
    cart.classList.remove("active");
    cartIcon.style["opacity"] = 1;
    autoIcon.style["opacity"] = 1;
}

if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready);
} else {
    ready();
}

function ready() {
    const removeCartButtons = document.getElementsByClassName("cart-remove");
    for (let i = 0; i < removeCartButtons.length; i++) {
        const button = removeCartButtons[i];
        button.addEventListener('click', removeCartItem);
    }
    const quantityInputs = document.getElementsByClassName('cart-quantity');
    for (let i = 0; i < quantityInputs.length; i++) {
        const input = quantityInputs[i];
        input.addEventListener('change', quantityChanged);
    }
    //add to cart
    const addCart = document.getElementsByClassName("button-actual");
    for (let i = 0; i < addCart.length; i++) {
        const button = addCart[i];
        button.addEventListener('click', addCartClicked);
    }
    //buy button
    document.querySelector('.button-order-cart').addEventListener('click', buyButtonClicked);
}

function buyButtonClicked() {
    // alert('Ваше замовлення розміщено');
    var cartContent = document.getElementsByClassName('cart-content')[0];
    if (cartContent.innerHTML == "") {
        alert("Кошик пустий");
        return;
    }
    while (cartContent.hasChildNodes()) {
        cartContent.removeChild(cartContent.firstChild);
    }
    updatetotal();
    location.href = 'order.html#order-hero-id';
} 

function removeCartItem(event) {
    var buttonClicked = event.target;
    buttonClicked.parentElement.remove();
    updatetotal();
}

function quantityChanged(event) {
    var input = event.target;
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1;
    }
    updatetotal();
} 

//add to cart
function addCartClicked(event) {
    var button = event.target;
    var shopProducts = button.parentElement;
    var title = shopProducts.getElementsByClassName("name-product-text")[0].innerText;
    var price = shopProducts.getElementsByClassName("cost-product")[0].innerText;
    var productImg = shopProducts.getElementsByClassName("actual-photo")[0].src;
    addProductToCart(title, price, productImg);
    updatetotal();
}

function addProductToCart(title, price, productImg) {
    var cartShopBox = document.createElement('div');
    cartShopBox.classList.add("cart-box");
    var cartItems = document.getElementsByClassName('cart-content')[0];
    var cartItemsNames = cartItems.getElementsByClassName("cart-product-title");
    for (let i = 0; i < cartItemsNames.length; i++) {
        if (cartItemsNames[i].innerText === title) {
            alert('Цей товар вже є у вашому кошику!');
            return;
        }
    }

    var cartBoxContent = `
        <img src="${productImg}" class="cart-img"/>
        <div class="detail-box">
            <p class="cart-product-title">${title}</p>
            <div class="cart-price">${price}</div>
            <div class="cart-quantity-container">
                <img src="../photos/ArrowPinkDown.png" class="arrow-down"/>
                <input type="number" value="1" class="cart-quantity">
                <img src="../photos/ArrowPinkUp.png" class="arrow-up"/>
            </div>
        </div>
        <img src="/photos/trash-bin.png" class="cart-remove"/>`;
    cartShopBox.innerHTML = cartBoxContent;
    cartItems.append(cartShopBox);
    cartShopBox.getElementsByClassName("cart-remove")[0].addEventListener('click', removeCartItem);
    cartShopBox.getElementsByClassName("cart-quantity")[0].addEventListener('change', quantityChanged);
    cartShopBox.getElementsByClassName("arrow-down")[0].addEventListener('click', decreaseAmount);
    cartShopBox.getElementsByClassName("arrow-up")[0].addEventListener('click', increaseAmount);
}

function decreaseAmount(event) {
    var arrow = event.target;
    var cartQuantityContainer = arrow.parentElement;
    if (cartQuantityContainer.children[1].value > 1) {
        cartQuantityContainer.children[1].value -= 1;
    }
    quantityChanged(event);
}

function increaseAmount(event) {
    var arrow = event.target;
    var cartQuantityContainer = arrow.parentElement;
    cartQuantityContainer.children[1].value = Number(cartQuantityContainer.children[1].value) + 1;
    quantityChanged(event);
}

function updatetotal() {
    var cartContent = document.getElementsByClassName('cart-content')[0];
    var cartBoxes = cartContent.getElementsByClassName('cart-box');
    var total = 0;
    for (var i = 0; i < cartBoxes.length; i++) {
        var cartBox = cartBoxes[i];
        var priceElement = cartBox.getElementsByClassName('cart-price')[0];
        var quantityElement = cartBox.getElementsByClassName('cart-quantity')[0];
        var price = parseFloat(priceElement.innerText.replace('$',""));
        var quantity = quantityElement.value;
        total = total + (price * quantity);
    }
    total = Math.round(total * 100) / 100;
    document.getElementsByClassName('total-price')[0].innerText = total + '₴';
}