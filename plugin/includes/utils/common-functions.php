<?php
// Example: Retrieve the WebSocket URL from settings
function get_chatbot_websocket_url() {
    return get_option('chatbot_websocket_url', 'ws://localhost:8000/ws/chat');
}
