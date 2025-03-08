<script>
import ShareRes from "./ShareRes.vue";
import FindRes from "./FindRes.vue";
export default
{
  name: "Resources",
  components:
      {
        "ShareRes":ShareRes,
        "FindRes":FindRes,
      },
}
</script>

<template>
<div id="Resources-MainDiv">
  <div id="Resources-HeaderDiv">
    <img src="../../../src/assets/images/09.jpg" style="height: 100%;border-radius: 0 6px 6px 0">
    <img src="../../assets/images/07.svg" style="height: 100%;margin-top: 0.5rem;">
  </div>
  <div id="Resources-Div02">
    <div id="Resources-Div01">
      <el-tabs tab-position="top" id="Resources-elTab01" class="demo-tabs">
        <el-tab-pane label="查找资源">
          <FindRes></FindRes>
        </el-tab-pane>
        <el-tab-pane label="分享资源">
          <ShareRes></ShareRes>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>

</div>
</template>

<style scoped>
@font-face
{
  font-family: HPHS;
  src: url("../../assets/fonts/HPHS.woff");
}
#Resources-MainDiv
{
  width: 100%;
  background-color: white;
}
#Resources-HeaderDiv
{
  height:6rem;
  width:100%;
  background-image: linear-gradient(to right, rgb(210, 174, 142),white);
  display: flex;
}
#Resources-Div01
{
  width:87.5%;
  font-family: HPHS, serif;
}
#Resources-Div02
{
  display: flex;
  justify-content: center;
}
#Resources-elTab01
{

}
</style>