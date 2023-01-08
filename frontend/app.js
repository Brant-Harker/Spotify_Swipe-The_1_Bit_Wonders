const song = "song";
const artist = "artist";
const cover = "https://i.scdn.co/image/ab67616d0000b273409c576a374c0e7dc31f1dd3"
    
    var card = document.createElement("div"); 
    card.className = "card";

    var songName = document.createElement("div"); 
    songName.className = "songName";
    songName.innerHTML += song;
    card.appendChild(songName);

    var artistName = document.createElement("div"); 
    artistName.className = "artistName";
    artistName.innerHTML += artist;
    card.appendChild(artistName);

    var albumCover = document.createElement("img"); 
    albumCover.className = "albumCover";
    albumCover.src = cover;
    card.appendChild(albumCover);

    document.getElementById('inside').appendChild(card);

document.body.addEventListener("click", clickDemo)
function clickDemo(e) {
    var audio = new Audio('https://p.scdn.co/mp3-preview/254bb84cd1dddb6ca91db2ea027d551ae57824e8');
    audio.play();
}
