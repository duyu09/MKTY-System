<!--
- 文件描述：明康慧医MKTY智慧医疗系统知识库管理总组件
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 文件名：KnowledgeOverview.vue
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
-->

<template>
  <div style="width: 100%;">
    <KnowledgeHeader />
    <Knowledge />
  </div>
</template>

<script>
import Knowledge from "@/components/modules/Knowledge.vue";
import KnowledgeHeader from "@/components/modules/KnowledgeHeader.vue";

export default {
  components: {
    Knowledge,
    KnowledgeHeader
  }
};

</script>

<style scoped>

</style>