<script>
import CreateForum from "./CreateForum.vue";
import CreateOrg from "./CreateOrg.vue";
import JoinOrg from "./JoinOrg.vue";
import ForumOverview from "./ForumOverview.vue";
export default
{
  name: "Forum",
  components:
      {
        'CreateForum':CreateForum,
        'CreateOrg':CreateOrg,
        'JoinOrg':JoinOrg,
        'ForumOverview':ForumOverview,
      },
}
</script>

<template>
  <div id="Forum-MainDiv">
    <el-header id="Forum-elHeader">
      <div id="Forum-elHeader-title01">
        <div id="Forum-elHeader-title03">
          <nobr>ILP专属论坛与纳新基地</nobr>
        </div>
        <div id="Forum-elHeader-title02">
          <nobr>技术与学术的海洋，社团与组织的天堂</nobr><br>
          <span id="Forum-elHeader-title04">
            <nobr>ILP Exclusive Forum and Enrollment Base</nobr>
          </span>
        </div>
      </div>
    </el-header>


    <div id="Forum-Div01">
      <el-tabs tab-position="top" id="Forum-elTab01" class="demo-tabs">
        <el-tab-pane label="论坛概览"><ForumOverview></ForumOverview></el-tab-pane>
        <el-tab-pane label="加入学生组织"><JoinOrg></JoinOrg></el-tab-pane>
        <el-tab-pane label="创建论坛"><CreateForum></CreateForum></el-tab-pane>
        <el-tab-pane label="创建学生组织"><CreateOrg></CreateOrg></el-tab-pane>
      </el-tabs>
    </div>

  </div>
</template>

<style scoped>
@font-face
{
  font-family: font01;
  src: url("../../assets/fonts/font01.woff");
}
@font-face
{
  font-family: ubuntu;
  src:url("../../assets/fonts/ubuntu.woff2");
}
@font-face
{
  font-family: HPHS;
  src: url("../../assets/fonts/HPHS.woff");
}
#Forum-Div01
{
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}
#Forum-elTab01
{
  height: 30rem;
  width:80%;
  font-size: larger;
  font-family: HPHS, serif;
}
#Forum-MainDiv
{
  width: 100%;
  background-color: white;
  overflow: auto;
}
#Forum-elHeader
{
  height: 3.75rem;
  color: white;
  background-image:linear-gradient(to right, rgb(0, 220, 0), darkgreen);
  box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
  border-radius: 0 0 10px 10px;
  display: flex;
  align-items: center;
}
#Forum-elHeader-title01
{
  font-family: font01,serif;
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
  color: rgb(180, 255, 220);
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
  color: rgb(180, 255, 210);
  text-shadow: 1px 1px black;
}
.demo-tabs > .el-tabs__content
{
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.el-tabs--right .el-tabs__content,
.el-tabs--left .el-tabs__content
{
  height: 100%;
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