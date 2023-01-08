// DOM
const swiper = document.querySelector("#swiper");
const like = document.querySelector("#like");
const dislike = document.querySelector("#dislike");

// Variables
let tracks = [];

let audio = new Audio();

// Event listener on array update
function playSong() {
    // Get the top card
    const topCard = swiper.querySelector(".card:not(.dismissing)");

    // Console log the value of div with class of songName
    console.log(topCard.querySelector(".songName").innerHTML);

    // Get the value of data-preview attribute
    const preview = topCard.getAttribute("data-preview");

    // Stop any current audio
    if (audio) {
        audio.pause();
    }

    // Play the song (preview)
    audio = new Audio(preview);
    audio.play();
}

// API service
async function fetchRecommendations() {
    const response = await fetch("http://127.0.0.1:8080/api/recommendations");
    const data = await response.json();

    data.tracks.map((track) => {
        if (track.preview_url) {
            tracks.push([
                track.id,
                track.name,
                track.artists[0].name,
                track.album.images[0].url,
                track.preview_url,
                track.external_urls.spotify,
            ]);
        }
    }, tracks);
}

window.onload = () => {
    fetchRecommendations();
};

// variables
let cardCount = 0;

// functions
function appendNewCard() {
    /* 
        Track array index

        0: track id
        1: track name
        2: artist name
        3: album cover
        4: preview url
        5: spotify url
    */

    const card = new Card({
        id: tracks[cardCount % tracks.length][0],
        song: tracks[cardCount % tracks.length][1],
        artist: tracks[cardCount % tracks.length][2],
        cover: tracks[cardCount % tracks.length][3],
        preview: tracks[cardCount % tracks.length][4],
        // imageUrl: tracks[cardCount % tracks.length],
        // imageText: `Image ${cardCount + 1}`,
        onDismiss: appendNewCard,
        onLike: () => {
            like.style.animationPlayState = "running";
            like.classList.toggle("trigger");
            tracks.splice(cardCount % tracks.length, 1);
            if (tracks.length < 4) {
                fetchRecommendations();
            }
            playSong();
        },
        onDislike: () => {
            dislike.style.animationPlayState = "running";
            dislike.classList.toggle("trigger");
            tracks.splice(cardCount % tracks.length, 1);
            if (tracks.length < 4) {
                fetchRecommendations();
            }
            playSong();
        },
    });
    swiper.append(card.element);
    cardCount++;

    const cards = swiper.querySelectorAll(".card:not(.dismissing)");
    cards.forEach((card, index) => {
        card.style.setProperty("--i", index);
    });
}

// first 5 cards, wait for tracks array to be populated
setTimeout(() => {
    for (let i = 0; i < tracks.length; i++) {
        appendNewCard();
    }
}, 1000);
