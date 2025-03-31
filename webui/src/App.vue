<template>
  <div class="app-container">
    <!-- 左侧聊天区域 -->
    <ChatArea :messages="messages" />
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
import ChatArea from "./components/ChatArea.vue";
import AppButtons from "./components/AppButtons.vue";
import AICallEngine, { AICallAgentType }  from 'aliyun-auikit-aicall';
export default {
  components: { ChatArea, VideoArea, AppButtons },
  data() {
    return {
      messages: [
        { sender: "AI", text: "Hello, what can I do for you." },
        { sender: "User", text: "What is Apple?" },
      ],
      engine: null, // 存储 AICallEngine 实例
      agentInfo: null, // 智能体信息
    };
  },
  methods: {
    async handleStart() {
      try {
        // 1. 启动摄像头视频
        this.$refs.videoArea.startVideo();

        // 2. 获取智能体信息（需从服务端获取）
        this.agentInfo = await this.fetchAgentInfo();

        // 3. 初始化并调用语音通话智能体
        this.engine = new AICallEngine();
        await this.engine.init(AICallAgentType.VOICE); // 设置智能体类型
        this.engine.on('callBegin', () => console.log('通话已开始'));
        this.engine.on('callEnd', () => console.log('通话已结束'));

        // 4. 启动通话
        await this.engine.call(this.userId, this.agentInfo);
      } catch (error) {
        console.error('初始化失败:', error);
      }
    },

    // 模拟获取智能体信息（需替换为真实接口）
    async fetchAgentInfo() {
      // 这里应调用你的后端 API 获取真实数据
      return {
        instanceId: 'your_instance_id',
        channelId: 'your_channel_id',
        userId: 'your_user_id',
        rtcToken: 'your_rtc_token',
        reqId: 'your_req_id'
      };
    },

    // 其他方法保持不变...
    handleEnd() {
      this.$refs.videoArea.stopVideo();
      this.saveMessages();
      this.engine?.endCall(); // 结束通话
    },
    // ... 其他方法
    // start() {
    //   this.$refs.videoArea.startVideo();
    // },
    // end() {
    //   this.$refs.videoArea.stopVideo();
    //   this.saveMessages();
    // },
    saveAndDownload() {
      alert("正在保存当前对话和视频！");
      this.$refs.videoArea.saveRecording(); // 调用子组件的方法保存录音
      this.saveMessages();
    },
    saveMessages() {
      console.log("保存对话内容:", this.messages);
    },
  },
  beforeUnmount() {
    // 销毁时释放资源
    this.engine?.destroy();
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