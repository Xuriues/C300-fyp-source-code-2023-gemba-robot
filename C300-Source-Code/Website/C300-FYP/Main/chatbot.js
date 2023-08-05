// Wait for the DOM to be fully loaded before executing the code inside the function
document.addEventListener('DOMContentLoaded', function () {
    // Get references to the necessary HTML elements
    const submitBtn = document.querySelector('button[name="btnSubmit"]');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const responseMessage = document.getElementById('responseMessage');

    // Add a click event listener to the submit button
    submitBtn.addEventListener('click', function () {
        // When the submit button is clicked, display the loading spinner and hide the response message
        loadingSpinner.style.display = 'block';
        responseMessage.style.display = 'none';
    });

    let recognition; // Variable to hold the SpeechRecognition object

    // Function to handle speech input
    function startSpeechRecognition() {
        // Create a new SpeechRecognition object (using the Web Speech API)
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

        // Enable interim results to get partial recognition while speaking
        recognition.interimResults = true;

        // Set the language for speech recognition to English (United States)
        recognition.lang = 'en-US';

        // Event listener for when speech recognition yields a result
        recognition.onresult = function (event) {
            // Extract the transcript from the event results and concatenate them into a single string
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript)
                .join('');

            // Update the textarea with the recognized text
            const textAreaChatbot = document.querySelector('textarea[name="textAreaChatbot"]');
            textAreaChatbot.value = transcript;
        };

        // Event listener for when speech recognition ends
        recognition.onend = function () {
            // Enable the microphone button after recognition has ended
            btnSpeech.disabled = false;
            btnSpeech.textContent = 'Microphone'; // Reset button text to "Microphone"
        };

        // Event listener for when speech recognition starts
        recognition.onstart = function () {
            btnSpeech.textContent = 'Stop'; // Set button text to "Stop" when recognition starts
        };

        // Start the speech recognition process
        recognition.start();
    }

    // Get a reference to the microphone button
    const btnSpeech = document.getElementById('btnSpeech');

    // Add a click event listener to the microphone button
    btnSpeech.addEventListener('click', function () {
        if (recognition && recognition.running) {
            // If recognition is running, stop it when the button is clicked
            recognition.stop();
        } else {
            // If recognition is not running, start it when the button is clicked
            btnSpeech.disabled = true; // Disable the button to prevent multiple recognition instances
            startSpeechRecognition();
        }
    });
});