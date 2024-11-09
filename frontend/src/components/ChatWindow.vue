<template>
    <div class="chat-window">
      <header class="chat-header">
        <h2>ChatBot Assistant</h2>
      </header>
      
      <div class="messages" ref="messages">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="msg.isBot ? 'bot-message' : 'user-message'"
        >
          {{ msg.text }}
        </div>
      </div>
      
      <InputField @send="sendMessage" />
    </div>
  </template>
  
  <script>
  import InputField from './InputField.vue';
  
  export default {
    components: {
      InputField
    },
    data() {
      return {
        messages: [],
        socket: null,
      };
    },
    methods: {
      connectWebSocket() {
        this.socket = new WebSocket("ws://localhost:8000/ws/chat");
        
        this.socket.onmessage = (event) => {
          const { response } = JSON.parse(event.data);
          this.messages.push({ text: response, isBot: true });
          this.scrollToBottom();
        };
        
        this.socket.onerror = (error) => {
          console.error("WebSocket Error:", error);
        };
        
        this.socket.onclose = () => {
          console.log("WebSocket connection closed");
        };
      },
      sendMessage(text) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
          this.messages.push({ text, isBot: false });
          this.socket.send(text);
          this.scrollToBottom();
        } else {
          console.error("WebSocket is not connected.");
        }
      },
      scrollToBottom() {
        this.$nextTick(() => {
          const messagesContainer = this.$refs.messages;
          messagesContainer.scrollTop = messagesContainer.scrollHeight;
        });
      }
    },
    mounted() {
      this.connectWebSocket();
    }
  };
  </script>
  
  <style scoped>
  .chat-window {    
    display: flex;
    flex-direction: column;
    max-width: 500px;
    height: auto;
    max-height: 80vh;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    background-color: #f9f9f9;
  }
  
  .chat-header {
    background-color: #007bff;
    color: white;
    text-align: center;
    padding: 12px;
    font-weight: bold;
  }
  
  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    background-color: #f4f7fa;
  }
  
  .user-message,
  .bot-message {
    max-width: 80%;
    padding: 10px 14px;
    border-radius: 20px;
    line-height: 1.4;
    font-size: 0.9em;
    position: relative;
    animation: fadeIn 0.3s ease-in-out;
  }
  
  .user-message {
    align-self: flex-end;
    background-color: #007bff;
    color: white;
    box-shadow: 0px 3px 6px rgba(0, 123, 255, 0.2);
  }
  
  .bot-message {
    align-self: flex-start;
    background-color: #e0e0e0;
    color: #333;
    box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  </style>
  