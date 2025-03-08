<script>
import { RouterLink, RouterView } from 'vue-router';

export default
{
    name: "NotFound",
    methods: 
    {
        GotoHomePage:function() 
        {
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