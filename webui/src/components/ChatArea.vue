<template>
  <div class="chat-area">
    <div v-for="(message, index) in messages" :key="index" class="message-item">
      <div class="ai-avatar" v-if="message.sender === 'AI'">AI</div>
      <div class="user-avatar" v-else>User</div>
      <div class="message">{{ message.text }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.chat-area {
  flex: 1;
  background-color: #e6ffe6;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.ai-avatar {
  width: 40px;
  height: 40px;
  background-color: #800080;
  border-radius: 50%;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}
.user-avatar {
  width: 40px;
  height: 40px;
  background-color: #007bff;
  border-radius: 50%;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}
.message-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.message {
  margin-left: 10px;
  color: #ff69b4;
  font-size: 14px;
}
</style>