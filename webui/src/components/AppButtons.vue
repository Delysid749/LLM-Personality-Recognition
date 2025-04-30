<template>
  <div class="button-area">
    <!-- 使用 $emit 触发自定义事件 -->
    <button @click="$emit('start')">start</button>
    <button @click="$emit('end')">stop</button>
    <!-- <button @click="$emit('save')">保留</button> -->
  </div>
</template>


<script>
export default {

};
</script>
<style>
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