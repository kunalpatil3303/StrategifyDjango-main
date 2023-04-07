const buttonRight = document.getElementById('slideRight');
const buttonLeft = document.getElementById('slideLeft');

buttonRight.onclick = function () {
  document.getElementById('mystrategy').scrollLeft += 800;
};
    
buttonLeft.onclick = function () {
  document.getElementById('mystrategy').scrollLeft -= 800;
};

function searchStrategyByName(){
    var input, filter, cards, cardContainer, h5, title, i;
    input = document.getElementById("searchStrategy");
    filter = input.value.toUpperCase();
    cardContainer = document.getElementById("mystrategy");
    cards = cardContainer.getElementsByClassName("strategyCard");
    for (i = 0; i < cards.length; i++) {
        title = cards[i].querySelector(".card-body h5.heading");
        if (title.innerText.toUpperCase().indexOf(filter) > -1) {
            cards[i].style.display = "";
        } else {
            cards[i].style.display = "none";
        }
    }
}



