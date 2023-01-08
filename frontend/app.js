// const song = "song";
// const artist = "artist";
// const cover = "https://i.scdn.co/image/ab67616d0000b273409c576a374c0e7dc31f1dd3"
    
// DOM
const swiper = document.querySelector('#swiper');
const like = document.querySelector('#like');
const dislike = document.querySelector('#dislike');

// constants
const urls = [
  ["song", "artist", "https://i.scdn.co/image/ab67616d0000b273409c576a374c0e7dc31f1dd3"],
  ["song", "artist", "https://i.scdn.co/image/ab67616d0000b273409c576a374c0e7dc31f1dd3"],
  ["song", "artist", "https://i.scdn.co/image/ab67616d0000b273409c576a374c0e7dc31f1dd3"],
  ["song", "artist", "https://i.scdn.co/image/ab67616d0000b273409c576a374c0e7dc31f1dd3"],
  ["song", "artist", "https://i.scdn.co/image/ab67616d0000b273409c576a374c0e7dc31f1dd3"]
];

// variables
let cardCount = 0;

// functions
function appendNewCard() {
  const card = new Card({
    song: urls[cardCount % 5][0],
    artist: urls[cardCount % 5][1],
    cover: urls[cardCount % 5][2],
    // imageUrl: urls[cardCount % 5],
    // imageText: `Image ${cardCount + 1}`,
    onDismiss: appendNewCard,
    onLike: () => {
      like.style.animationPlayState = 'running';
      like.classList.toggle('trigger');
    },
    onDislike: () => {
      dislike.style.animationPlayState = 'running';
      dislike.classList.toggle('trigger');
    }
  });
  swiper.append(card.element);
  cardCount++;

  const cards = swiper.querySelectorAll('.card:not(.dismissing)');
  cards.forEach((card, index) => {
    card.style.setProperty('--i', index);
  });
}

// first 5 cards
for (let i = 0; i < 5; i++) {
  appendNewCard();
}


document.body.addEventListener("click", clickDemo)
function clickDemo(e) {
    var audio = new Audio('https://p.scdn.co/mp3-preview/254bb84cd1dddb6ca91db2ea027d551ae57824e8');
    audio.play();
}
