quantity = document.getElementById("id_quantity");
quantity.min = "1";
quantity.max = "10";
quantity.onkeydown = "return false"

price = document.getElementById("price")

order_price = document.createElement("p")
order_price.setAttribute("id", "order_price");
price.appendChild(order_price)

order_price = document.getElementById("order_price");
order_price.innerHTML = prod_price * quantity.value;

total = () => {
    order_price.innerHTML = prod_price * quantity.value;
}

quantity.addEventListener("input", total);