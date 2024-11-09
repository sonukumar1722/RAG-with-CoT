<template>
  <div id="app">
    <header class="app-header">
      <h1>Interactive Chatbot</h1>
    </header>
    <main>
      <ChatWindow />
    </main>
  </div>
</template>

<script>
import ChatWindow from './components/ChatWindow.vue';

export default {
  components: {
    ChatWindow
  }
};
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f3f4f6;
  font-family: Arial, sans-serif;
}

.app-header {
  padding: 16px;
  background-color: #007bff;
  color: white;
  text-align: center;
}

main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px;
}
</style>
