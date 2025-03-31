<template>
  <div class="video-area">
    <video ref="videoPlayer" autoplay :style="{ display: isPlaying ? 'block' : 'none' }"></video>
    <div class="placeholder" v-if="!isPlaying">摄像头未启动</div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      isPlaying: false,
      mediaStream: null, // 存储视频流
      mediaRecorder: null,
      recordedChunks: [],
    };
  },
  mounted() {
    // this.startVideo();
  },
  methods: {
    async startVideo() {
      try {
        // 获取摄像头和麦克风权限
        this.mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        this.$refs.videoPlayer.srcObject = this.mediaStream;
        this.isPlaying = true;

        // 初始化录制
        this.mediaRecorder = new MediaRecorder(this.mediaStream);
        this.mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) this.recordedChunks.push(event.data);
        };
        this.mediaRecorder.start(1000); // 每秒触发录制
      } catch (error) {
        console.error('无法访问摄像头:', error);
      }
    },
    stopVideo() {
      if (this.mediaRecorder) this.mediaRecorder.stop();
      if (this.mediaStream) {
        this.mediaStream.getTracks().forEach(track => track.stop());
        this.isPlaying = false;
      }
    },
    saveRecording() {
      if (this.recordedChunks.length) {
        const blob = new Blob(this.recordedChunks, { type: "video/webm" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'recording.webm'; // 下载文件名
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      }
    },
  },
  beforeUnmount() {
    this.stopVideo();
  }
};
</script>
  
  <style scoped>
  .video-area {
    flex: 1;
    background-color: #e0ffff;
    position: relative;
  }
  video {
    width: 500px;
    height: 500px;
    background-color: black;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  .placeholder {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 16px;
    color: #666;
  }
  </style>