<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统"404 Not Found"页面组件Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年02月22日 -->
<!-- 修改日期：2025年02月22日 -->
<script>
export default
{
    name: "NotFound",
    methods: 
    {
        GotoHomePage:function(){
            this.$router.push('/main/HomePage');
        }
    },
}
</script>
<template>
  <div id="NotFound-MainDiv">
    <el-empty description="你似乎来到了一片没有知识的荒原。。。">
      <el-button type="primary" @click="GotoHomePage()">返回首页</el-button>
    </el-empty>
  </div>
</template>
<style scoped>
#NotFound-MainDiv
{
    height: 100vh;
    background-color: rgb(210, 210, 210);
}
</style>
