rating = document.getElementById('rating');
slider = document.getElementById('slider');
rate = document.createTextNode(slider.value);
rating.appendChild(rate);

rate_changer = () => {
    rate.textContent = slider.value;
}

slider.addEventListener("change", rate_changer);