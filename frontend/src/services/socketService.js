import { io } from 'socket.io-client';

const socketService = io('http://localhost:8000');  // Replace with the actual backend URL

export default socketService;
