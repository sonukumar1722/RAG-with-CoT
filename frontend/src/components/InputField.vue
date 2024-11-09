<template>
    <div class="input-field">
      <input
        v-model="message"
        @keyup.enter="handleSend"
        type="text"
        placeholder="Type a message..."
      />
      <button @click="handleSend">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white">
          <path d="M2.01 21l20.99-9-21-9-.01 7 15 2-15 2z"/>
        </svg>
      </button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        message: ""
      };
    },
    methods: {
      handleSend() {
        if (this.message.trim()) {
          this.$emit("send", this.message);
          this.message = "";
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .input-field {
    display: flex;
    padding: 10px;
    border-top: 1px solid #ddd;
    background-color: #f1f1f1;
  }
  
  input {
    flex: 1;
    padding: 10px 12px;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 20px;
    margin-right: 8px;
    outline: none;
    transition: border-color 0.3s;
  }
  
  input:focus {
    border-color: #007bff;
  }
  
  button {
    background-color: #007bff;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    outline: none;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  button svg {
    fill: white;
  }
  </style>
  