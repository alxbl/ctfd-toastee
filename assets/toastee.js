const SplashDuration = 3000;
const AudioContext = window.AudioContext || window.webkitAudioContext;
const context = new AudioContext();
let toastee_buf = null;
let splash = $("#toastee");
let splashTimeout = null;

// Function called on every solve.
function on_toast(data) {
    // Play the toast sound.
    var source = context.createBufferSource();
    source.buffer = toastee_buf;
    source.connect(context.destination);
    source.start();

    if (data.team != '') data.user = data.team;

    $("#toastee-banner .user").text(data.user);
    $("#toastee-banner b").text(data.chal);
    $("#toastee-banner .pts").text(data.pts);

    // Show splash screen.
    splash.removeClass("hidden");
    // Extend duration if a timeout is ongoing.
    if (splashTimeout) clearTimeout(splashTimeout);
    splashTimeout = setTimeout(() => {
        splash.addClass("hidden");
        splashTimeout = null;
    }, SplashDuration);
}

// XHR stuff because <audio> doesn't work.
// This is used to pre-load the toast sound.
// https://stackoverflow.com/questions/46856331/web-audio-api-get-audiobuffer-of-audio-element
fetch('/plugins/toastee/assets/toast.wav', r => {
    var ad = r.response;
    context.decodeAudioData(ad, buf => toastee_buf = buf, e => console.log('Error decoding buffer:', e))
})

function fetch(url, resolve) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'arraybuffer';
    request.onload = function () { resolve(request) }
    request.send()
}

// Establish SocketIO connection to receive solve events.
var socket = io();
socket.on('connect', function() {
    console.log("Socket.io: Connection Established");
});

socket.on('solve', function(data) {
    console.log('Solve>', data);
    on_toast(data);
});