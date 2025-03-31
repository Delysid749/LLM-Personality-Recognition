<template>
    <div ref="aicallContainer" class="aicall-container"></div>
  </template>
  
  <script>
  /* global ARTCAICallUI */
  export default {
    name: 'AICallComponent',
    mounted() {
      this.initAICallUI();
    },

    data() {
        return {
            // 
            shareToken: 'eyJSZXF1ZXN0SWQiOiJCREMzRjFGMi1DREY4LTVCMUMtOENCMC0zNTNGQkIyMzY2OUYiLCJXb3JrZmxvd1R5cGUiOiJWb2ljZUNoYXQiLCJUZW1wb3JhcnlBSUFnZW50SWQiOiIyNjJkMzQzOTczMDM0NTRiODUzZmQ4ZDQ5ZmJmOGIwYiIsIkV4cGlyZVRpbWUiOiIyMDI1LTAzLTI4IDA3OjQwOjM4IiwiTmFtZSI6InRVajRaS2k1IiwiUmVnaW9uIjoiY24taGFuZ3pob3UifQ==',
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