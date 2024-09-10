document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.querySelector('.messages-container');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');

    // Animate header
    anime({
        targets: '.chat-header',
        translateY: [-50, 0],
        opacity: [0, 1],
        duration: 800,
        easing: 'easeOutElastic(1, .8)'
    });

    // Animate avatar
    anime({
        targets: '.avatar',
        scale: [0, 1],
        duration: 1000,
        easing: 'spring(1, 80, 10, 0)'
    });

    // Animate messages
    document.querySelectorAll('.message').forEach((message, index) => {
        setTimeout(() => {
            message.classList.add('show');
        }, 100 * index);
    });

    // Animate input area
    anime({
        targets: '.input-area',
        translateY: [50, 0],
        opacity: [0, 1],
        duration: 800,
        easing: 'easeOutQuad'
    });

    // Send message function
    function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', 'receiver');
            messageElement.innerHTML = `<div class="message-content">${messageText}</div>`;
            messagesContainer.appendChild(messageElement);
            messageInput.value = '';

            // Animate new message
            anime({
                targets: messageElement,
                translateY: [20, 0],
                opacity: [0, 1],
                duration: 300,
                easing: 'easeOutQuad'
            });

            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
