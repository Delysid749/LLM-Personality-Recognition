<template>
  <div class="app-container">
    <!-- 左侧聊天区域 -->
     <ChatArea v-if="!isplaying" :messages="messages" />
     <AICallComponent v-if="isplaying" ref="aicallComponent" />
    <!-- 右侧视频区域 -->
    <div class="right-section">
      <VideoArea ref="videoArea" />
      <!-- 将方法作为属性传递给子组件 -->
      <AppButtons 
        @start="handleStart"
        @end="handleEnd"
        @save="saveAndDownload"
      />
    </div>
  </div>
</template>

<script>
import VideoArea from "./components/VideoArea.vue";
import AICallComponent from "./components/AICallComponent.vue";
import AppButtons from "./components/AppButtons.vue";
import ChatArea from "./components/ChatArea.vue";
export default {
  components: { AICallComponent, VideoArea, AppButtons,ChatArea },
  data() {
    return {
      messages: [
        { sender: "AI", text: "Hello, what can I do for you." },
        { sender: "User", text: "What is Apple?" },
      ],
      isplaying: false,
    };
  },
  methods: {
    async handleStart() {
      try {
        // 1. 启动摄像头视频
        this.$refs.videoArea.startVideo();
        this.isplaying = true;
      } catch (error) {
        console.error('初始化失败:', error);
      }
    },


    handleEnd() {
      this.$refs.videoArea.stopVideo();
      this.isplaying = false;
      this.saveMessages();
    },
    saveAndDownload() {
      alert("正在保存当前对话和视频！");
      this.$refs.videoArea.saveRecording(); // 调用子组件的方法保存录音
      this.saveMessages();
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

</style>