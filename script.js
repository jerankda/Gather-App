document.addEventListener('DOMContentLoaded', function() {
    // Wrap every letter in a span
    var textWrapper = document.querySelector('.ml2');
    textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

    // Create an animation timeline
    var animation = anime.timeline({
        loop: false, // Set loop to false
        complete: function() {
            // Function to be called when the animation completes
            // Set opacity to 1 after the text animation
            textWrapper.style.opacity = 1;
        }
    });

    // Add animation sequences to the timeline
    animation.add({
        targets: '.ml2 .letter',
        scale: [4, 1],
        opacity: [0, 1],
        translateZ: 0,
        easing: "easeOutExpo",
        duration: 1200,
        delay: (el, i) => 70 * i
    }).add({
        targets: '.ml2',
        opacity: 1, // Set opacity to 1 at the end of the animation
        duration: 1000, // Adjust the duration to your preference
        easing: "easeOutExpo",
        delay: 1000
    });

    // Start the animation
    animation.play();
});

// JavaScript to set opacity to 1 after the page is loaded
document.body.style.opacity = "1";

function redirectTo(page) {
    window.location.href = page;
}
