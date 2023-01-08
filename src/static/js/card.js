async function likedTrack(trackId) {
    console.log("Liked track: " + trackId);
    const response = await fetch(
        "http://127.0.0.1:8080/api/addsong?id=" + trackId
    );
}

class Card {
    constructor({
        id,
        song,
        artist,
        cover,
        onDismiss,
        onLike,
        onDislike,
        preview,
    }) {
        this.id = id;
        this.song = song;
        this.artist = artist;
        this.cover = cover;
        this.preview = preview;
        this.onDismiss = onDismiss;
        this.onLike = onLike;
        this.onDislike = onDislike;
        this.#init();
    }

    // private properties
    #startPoint;
    #offsetX;
    #offsetY;

    #isTouchDevice = () => {
        return (
            "ontouchstart" in window ||
            navigator.maxTouchPoints > 0 ||
            navigator.msMaxTouchPoints > 0
        );
    };

    #init = () => {
        const card = document.createElement("div");
        card.classList.add("card");
        card.className = "card";

        // card.style.backgroundImage= "url(" + this.cover + ")";

        /* Add the blur effect */
        card.style.background = "rgba(255, 255, 255, 0.2)";
        card.style.backdropFilter = "blur(80px)";
        const albumCover = document.createElement("img");
        albumCover.className = "albumCover";
        albumCover.src = this.cover;
        card.setAttribute("data-preview", this.preview);
        albumCover.style.width = "80%";
        albumCover.style.height = "auto";
        card.appendChild(albumCover);

        const songName = document.createElement("div");
        songName.className = "songName";
        songName.innerHTML = this.song;
        card.appendChild(songName);

        const artistName = document.createElement("div");
        artistName.className = "artistName";
        artistName.innerHTML = this.artist;
        card.appendChild(artistName);

        //   document.getElementById('inside').appendChild(card);

        this.element = card;
        if (this.#isTouchDevice()) {
            this.#listenToTouchEvents();
        } else {
            this.#listenToMouseEvents();
        }
    };

    #listenToTouchEvents = () => {
        this.element.addEventListener("touchstart", (e) => {
            const touch = e.changedTouches[0];
            if (!touch) return;
            const { clientX, clientY } = touch;
            this.#startPoint = { x: clientX, y: clientY };
            document.addEventListener("touchmove", this.#handleTouchMove);
            this.element.style.transition = "transform 0s";
        });

        document.addEventListener("touchend", this.#handleTouchEnd);
        document.addEventListener("cancel", this.#handleTouchEnd);
    };

    #listenToMouseEvents = () => {
        this.element.addEventListener("mousedown", (e) => {
            const { clientX, clientY } = e;
            this.#startPoint = { x: clientX, y: clientY };
            document.addEventListener("mousemove", this.#handleMouseMove);
            this.element.style.transition = "transform 0s";
        });

        document.addEventListener("mouseup", this.#handleMoveUp);

        // prevent card from being dragged
        this.element.addEventListener("dragstart", (e) => {
            e.preventDefault();
        });
    };

    #handleMove = (x, y) => {
        this.#offsetX = x - this.#startPoint.x;
        this.#offsetY = y - this.#startPoint.y;
        const rotate = this.#offsetX * 0.1;
        this.element.style.transform = `translate(${this.#offsetX}px, ${
            this.#offsetY
        }px) rotate(${rotate}deg)`;
        // dismiss card
        if (Math.abs(this.#offsetX) > this.element.clientWidth * 0.7) {
            this.#dismiss(this.#offsetX > 0 ? 1 : -1);
        }
    };

    // mouse event handlers
    #handleMouseMove = (e) => {
        e.preventDefault();
        if (!this.#startPoint) return;
        const { clientX, clientY } = e;
        this.#handleMove(clientX, clientY);
    };

    #handleMoveUp = () => {
        this.#startPoint = null;
        document.removeEventListener("mousemove", this.#handleMouseMove);
        this.element.style.transform = "";
    };

    // touch event handlers
    #handleTouchMove = (e) => {
        if (!this.#startPoint) return;
        const touch = e.changedTouches[0];
        if (!touch) return;
        const { clientX, clientY } = touch;
        this.#handleMove(clientX, clientY);
    };

    #handleTouchEnd = () => {
        this.#startPoint = null;
        document.removeEventListener("touchmove", this.#handleTouchMove);
        this.element.style.transform = "";
    };

    #dismiss = (direction) => {
        this.#startPoint = null;
        document.removeEventListener("mouseup", this.#handleMoveUp);
        document.removeEventListener("mousemove", this.#handleMouseMove);
        document.removeEventListener("touchend", this.#handleTouchEnd);
        document.removeEventListener("touchmove", this.#handleTouchMove);
        this.element.style.transition = "transform 1s";
        this.element.style.transform = `translate(${
            direction * window.innerWidth
        }px, ${this.#offsetY}px) rotate(${90 * direction}deg)`;
        this.element.classList.add("dismissing");
        setTimeout(() => {
            this.element.remove();
        }, 1000);
        if (typeof this.onDismiss === "function") {
            this.onDismiss();
        }
        if (typeof this.onLike === "function" && direction === 1) {
            this.onLike();
            likedTrack(this.id);
        }
        if (typeof this.onDislike === "function" && direction === -1) {
            this.onDislike();
        }
    };
}
