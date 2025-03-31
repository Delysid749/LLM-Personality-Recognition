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
        isPlaying: true,
      };
    },
    mounted() {
        this.startVideo();
    },
    methods: {
      startVideo() {
        navigator.mediaDevices
          .getUserMedia({ video: true, audio: true })
          .then((stream) => {
            this.isPlaying = true;
            this.$refs.videoPlayer.srcObject = stream;
          })
          .catch((error) => {
            console.error("无法访问摄像头", error);
          });
      },
      stopVideo() {
        const videoStream = this.$refs.videoPlayer.srcObject;
        if (videoStream) {
          videoStream.getTracks().forEach((track) => track.stop());
          this.isPlaying = false;
        }
      },
    },
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