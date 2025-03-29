<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统侧边栏按钮列组件Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年02月29日 -->
<!-- 修改日期：2025年03月30日 -->
<script>
import { HomeFilled } from "@element-plus/icons-vue";
import { Sunny } from "@element-plus/icons-vue";
import { Guide } from "@element-plus/icons-vue";
import { ChatDotSquare } from "@element-plus/icons-vue";
import { Management } from "@element-plus/icons-vue";
import { FolderOpened } from "@element-plus/icons-vue";
import { Flag } from "@element-plus/icons-vue";
import { getCookie, setCookie, getUserAvatar, getUserInfo } from '@/api/api';
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue';

export default
{
    name: "MainView",
    components: 
    {
      "HomeFilled":HomeFilled,
      "Sunny":Sunny,
      "Guide":Guide,
      "ChatDotSquare":ChatDotSquare,
      "Management":Management,
      "FolderOpened":FolderOpened,
      "Flag":Flag,
    },
    data()
    {
      return{
        routerIndex:'',
        userAvatar_mv:'',
        userName_mv:'',
        userType_mv:''  // 0=患者，1=医师，2=其他人员
      }
    },
    computed:
    {
      userType_mv_text(){
        if (this.userType_mv == 0) return '患者';
        else if (this.userType_mv == 1) return '医师';
        else return '其他人员';
      }
    },
    methods: 
    {
        openInNewTab(route) {
          window.open(route, '_blank');
        },
        mainViewLoad()
        {
          const userId = parseInt(getCookie('userId'));
          getUserAvatar(userId).then((res) => {
            this.userAvatar_mv = res.data.userAvatar;
            // console.log(this.userAvatar_mv);
          });
          getUserInfo(userId).then((res) => {
            this.userName_mv = res.data.userInfo.userName;
            this.userType_mv = res.data.userInfo.userType;
          });
        }
    },
    mounted()
    {
      this.mainViewLoad();
    }
}
</script>
<template>
    <div class="common-layout" style="height: 100%;">
    <el-container style="height:100%;">
      <el-aside id="MainView-Aside">
        <div style="margin-top: 1.5rem;">
          <div class="MainView-MenuItem" @click="() => this.$router.push('/main/PersonalPage')">
            <el-icon><HomeFilled /></el-icon>
            我的主页
          </div>
          <div class="MainView-MenuItem" @click="() => this.$router.push('/main/MultimodalDiagnosis')">
            <el-icon><Guide /></el-icon>
            机器辅诊
          </div>
          <div class="MainView-MenuItem" @click="() => this.$router.push('/main/PsyChat')">
            <el-icon><Sunny /></el-icon>
            医疗问答
          </div>
          <div class="MainView-MenuItem" @click="() => this.$router.push('/main/Forum')">
            <el-icon><ChatDotSquare /></el-icon>
            论坛社团
          </div>
          <div class="MainView-MenuItem" @click="() => this.$router.push('/main/StartStudy')">
            <el-icon><Management /></el-icon>
            云上自习
          </div>
          <div class="MainView-MenuItem" @click="() => this.$router.push('/main/ImportantList')">
            <el-icon><Flag /></el-icon>
            诊疗事项
          </div>
          <div class="MainView-MenuItem" @click="() => this.$router.push('/main/Resources')">
            <el-icon><FolderOpened /></el-icon>
            资源天地
          </div>
        </div>
        
        <div style="bottom: 1.2rem; position: absolute; width: 100%;text-align: center;">
          <el-avatar size="large" :src="userAvatar_mv" id="MainView-el-avatar-01" @click="this.openInNewTab('/main/PersonalPage')" /><br>
          <span style="font-size: medium; cursor: pointer;" @click="this.openInNewTab('/main/PersonalPage')">{{ userName_mv }}</span>
          <br>
          <span style="font-size: small; cursor: pointer;" @click="this.openInNewTab('/main/PersonalPage')">{{ userType_mv_text }}</span>
        </div>


      </el-aside>
      <RouterView></RouterView>
    </el-container>
  </div>
</template>
<style>
@font-face
{
  src:url("/fonts/HPHS.woff");
  font-family: HPHS;
}
#MainView-Aside
{
  color: white;
    /*background-color: rgb(221, 221, 223);*/
    width: 10rem;
    box-shadow: 0 0.9rem 0.9rem 0 rgba(0,0,0,0.6);
    /*background-image: url('../assets/images/05.jpg');*/
    background-color: #1b1e26;
    background-attachment: fixed;
    background-repeat: no-repeat;
    background-size: auto 100%;
    position: relative;
}
.MainView-MenuItem
{
  text-align: center;
  padding-top: 1.25rem;
  padding-bottom: 1.25rem;
  font-family: HPHS, serif;
  font-size: 1.15rem;
}
.MainView-MenuItem:hover
{
  background-color: dimgrey;
  cursor: pointer;
}
.MainView-MenuItem:active
{
  background-color: #5a5a5a;
}
#MainView-el-avatar-01
{
  cursor: pointer; 
  border-style: solid; 
  border-color: white; 
  border-width: medium;
}
#MainView-el-avatar-01:hover
{
  border-color: #686abc;
  transition: 0.3s ease-in-out;
}
@media screen and (max-width:40rem)
{
    #MainView-Aside
    {
        display: none;
    }
}
</style>
