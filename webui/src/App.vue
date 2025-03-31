<template>
  <div class="app-container">
    <!-- 左侧聊天区域 -->
    <!-- <ChatArea :messages="messages" /> -->
    <AICallComponent  />
    <!-- 右侧视频区域 -->
    <div class="right-section">
      <VideoArea ref="videoArea" />
      <div class="button-area">
        <button @click="start">开始</button>
        <button @click="end">结束</button>
        <button @click="save">保留</button>
      </div>
    </div>
  </div>

  
</template>

<script>
import VideoArea from "./components/VideoArea.vue";
import AICallComponent from "./components/AICallComponent.vue";

export default {
  components: {  VideoArea,AICallComponent },
  // components: { ChatArea, VideoArea },
  data() {
    return {
      messages: [
        { sender: "AI", text: "Hello, what can I do for you." },
        { sender: "User", text: "What is Apple?" },
      ],
    };
  },
  methods: {
    start() {
      this.$refs.videoArea.startVideo();
    },
    end() {
      this.$refs.videoArea.stopVideo();
      this.saveMessages();
    },
    save() {
      alert("保存当前对话和视频！");
    },
    saveMessages() {
      console.log("保存对话内容:", this.messages);
    },
  },
};
</script>

<style>
.app-container {
  display: flex;
  height: 100vh;
}
.right-section {
  display: flex;
  flex-direction: column;
  flex: 1;
}
.button-area {
  background-color: #d3d3d3;
  height: 80px;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.button-area button {
  background-color: #ffff00;
  color: #ff0000;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
}
.button-area button:hover {
  background-color: #ffeb3b;
}
</style>