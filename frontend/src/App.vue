<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统根组件Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年02月10日 -->
<!-- 修改日期：2025年04月06日 -->
<script>
import { RouterLink, RouterView } from 'vue-router';
import MainView from "@/components/MainView.vue";
export default
{
  components:
  {
    "MainView":MainView,
  },

}
</script>

<template>
  <RouterView style="font-family: noto_serif_cjk;"></RouterView>
</template>

<style>
@font-face
{
  font-family: cons;
  src: url("/fonts/consola.woff2");
}
@font-face {
  font-family: noto_serif_cjk;
  src: url("/fonts/Noto_Serif_CJK.otf");
}
:root {
  font-family: 'noto_serif_cjk', sans-serif;
}
body {
  font-family: inherit;
}
pre > code
{
  font-family: cons !important;
  margin-top: 0.5rem !important;
  margin-bottom: 0.5rem !important;
  padding-top: 0.5rem !important;
  padding-bottom: 0.5rem !important;
  padding-left: 0.75rem !important;
  border-radius: 4px;
  font-size: 0.85em;
}
code
{
  font-family: cons !important;
}
</style>
