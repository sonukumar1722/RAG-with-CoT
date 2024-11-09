const socketService = {
    init: function() {
        // Fetch WebSocket URL from WordPress settings
        const websocketUrl = window.chatbotConfig.websocket_url || 'ws://localhost:8000/ws/chat'; 

        const socket = new WebSocket(websocketUrl);

        socket.onopen = () => {
            console.log('Connected to WebSocket');
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Message from server: ', data.response);
            // Handle server response (update UI with the response)
        };

        socket.onerror = (error) => {
            console.error('WebSocket Error: ', error);
        };

        socket.onclose = () => {
            console.log('WebSocket connection closed');
        };

        return socket;
    }
};

export default socketService;
