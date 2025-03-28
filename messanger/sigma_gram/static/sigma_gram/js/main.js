document.getElementById('send-button').addEventListener('click', sendMessage);

function sendMessage() {
    const input = document.getElementById('message-input');
    if (input.value.trim() !== '') {
        console.log('Отправка:', input.value);
        input.value = '';
    }
}