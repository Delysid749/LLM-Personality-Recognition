<template>
    <div ref="aicallContainer" class="aicall-container"></div>
  </template>
  
  <script>
  /* global ARTCAICallUI */
  import { SHARETOKEN } from '../../my_personal_key';
  export default {
    name: 'AICallComponent',
    mounted() {
      this.initAICallUI();
    },

    data() {
        return {
            // 
            shareToken: SHARETOKEN ,
            userId : '1234567890'
        };
    },
    methods: {
      initAICallUI() {
        // 获取容器 DOM 元素
        const container = this.$refs.aicallContainer;
        if (!container) return;
  
        // 初始化 AICall UI 实例
        this.aicallInstance = new ARTCAICallUI({
          userId: this.userId,
          root: container,
          shareToken: this.shareToken
        });
        this.aicallInstance.render();
      },

    }
  };
  </script>
  
  <style scoped>
  .aicall-container {
  flex: 1;
  background-color: #e6ffe6;
  padding: 10px;
  display: flex;
  flex-direction: column;
  /* align-items: flex-start; */
  /* width: 200px; */
}
  </style>