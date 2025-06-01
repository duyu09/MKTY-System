<!--
- 文件描述：明康慧医MKTY智慧医疗系统知识库管理组件头部标题
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 文件名：KnowledgeHeader.vue
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
-->

<template>
    <el-header id="Forum-elHeader">
      <div id="Forum-elHeader-title01">
        <div id="Forum-elHeader-title03">
          <nobr>资源中心知识库</nobr>
        </div>
        <div id="Forum-elHeader-title02">
          <nobr>MKTY专属医疗领域电子资源与知识库</nobr><br>
          <span id="Forum-elHeader-title04">
            <nobr>MKTY Exclusive Electronic Resources and Knowledge Base in the Medical Field</nobr>
          </span>
        </div>
      </div>
    </el-header>
</template>

<style scoped>
@font-face
{
  font-family: ubuntu;
  src:url("/fonts/ubuntu.woff2");
}
@font-face
{
  font-family: HPHS;
  src: url("/fonts/HPHS.woff");
}
@font-face
{
  font-family: xinwei;
  src: url("/fonts/xinwei.woff");
}
#Forum-elHeader
{
  height: 3.75rem;
  color: white;
  background-image: linear-gradient(to right, rgb(0, 135, 255), rgb(0, 0, 108));
  box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
  border-radius: 0 0 10px 10px;
  display: flex;
  align-items: center;
}
#Forum-elHeader-title01
{
  font-family: xinwei, serif;
  padding-left: 1.5rem;
  font-size: 2.25rem;
  display: flex;
}
#Forum-elHeader-title02
{
  font-family: HPHS, serif;
  font-size: 1.1rem;
  padding-top: 0.3rem;
  padding-left: 1.35rem;
  font-style: italic;
  color: rgb(180, 255, 255);
  text-shadow: 1px 1px black;
  flex-grow: 14;
}
#Forum-elHeader-title03
{
  flex-grow: 1;
  text-shadow: 2px 2px black;
  display: flex;
  justify-content: center;
  align-items: center;
}
#Forum-elHeader-title04
{
  font-size: 0.9rem;
  font-family: ubuntu,serif;
  color: rgb(100, 255, 255);
  text-shadow: 1px 1px black;
}
@media screen and (max-width:40rem)
{
  #Forum-elHeader
  {
    height: 5rem;
    text-align: center;
    display: flex;
    justify-content: center;
  }
  #Forum-elHeader-title01
  {
    font-size: 1.85rem;
    padding-left: 0;
    display: block;
    text-align: center;
  }
  #Forum-elHeader-title02
  {
    font-size: 1rem;
    padding-top: 0.2rem;
    text-align: center;
    padding-left: 0;
  }
  #Forum-elHeader-title03
  {
    text-align: center;
  }
  #Forum-elHeader-title04
  {
    display: none;
  }
}
</style>