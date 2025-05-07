<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统的用户移动端登录页面Vue文件。该文件为MKTY系统在手机上与用户见面的“第一页”，是其重要组成部分。 -->
<!-- 创建日期：2025年05月07日 -->
<!-- 修改日期：2025年05月07日 -->
<script>
import "@/assets/js/bootstrap.bundle.min.js";
import "@/assets/js/all.js";
import "@/assets/js/page.js";
import "@/assets/css/bootstrap.min.css";
import "@/assets/css/styles.css";
import "@/assets/css/rainbow_text.css";
import { loginVerification, setToken, setCookie, getCookie, convertBlobToBase64 } from "@/api/api";
import { errHandle, msgHandle, successHandle, openNewTab } from "@/utils/tools";

export default
{
  name: "LoginMobile",
  data()
  {
    return{
      userLoginKey:'',
      password:'',
      userLoginKeyType: true, // true=使用联系方式登录，false=使用账号登录
      isLoginWaiting:false
    }
  },
  mounted()
  {
    if(window.innerWidth>640){
      this.$router.push('/Login');
    }
  },
  computed: 
  {
    userLoginKeyTypeNumber(){
      return this.userLoginKeyType ? 1 : 0;
    }
  },
  methods:
      {
        LoginBtn()
        {
          this.isLoginWaiting=true;
          if(this.userLoginKey===''||this.password==='')
          {
            msgHandle('请您输入账号（或联系方式）和密码');
            this.isLoginWaiting=false;
            return;
          }
          loginVerification(this.userLoginKey, this.userLoginKeyTypeNumber, this.password)
              .then(res=>{
                if(res.data.code===0) {  // 登录成功
                  const token = res.data.accessToken;
                  const userId = res.data.userId;
                  setToken(token);
                  setCookie('userId', userId);
                  this.isLoginWaiting=false;
                  successHandle('登录成功！');
                  setInterval(() => {
                    //this.$router.push('/main/HomePage');
                    location.href='/main/HomePage';
                  }, 1000);
                }
                else
                {
                  const errMsg = res.data.msg;
                  this.isLoginWaiting=false;
                  msgHandle('警告：登录出错：' + errMsg);
                }
              })
              .catch(res=>{
                this.isLoginWaiting=false;
                msgHandle('警告：登录出错:' + res);
              })
        },
        openInNewTab(url) {
          openNewTab(url, '_blank'); // 打开新标签页 
        }
      }
}
</script>

<template>
<div id="lm-mainDiv">
  <div id="lm-div02">
    <div style="background-color: rgba(230,230,230,0.65); padding: 0.4rem; border-radius: 12px;">
      明康慧醫<span class="rainbow_text" style="font-family: HPHS; font-weight: bold;">MKTY</span><br>
      智慧醫療系統<br>
    </div>
    <span style="font-size: 1.5rem; font-family: HPHS;">移动版&nbsp;用户登录</span>
  </div>
  <div id="lm-div04">
    <div id="lm-div03">
      请输入账号：<br>
      <el-input v-model="userLoginKey" placeholder="User Identification" clearable /><br><br>
      请输入密码：<br>
      <el-input
          v-model="password"
          type="password"
          placeholder="Password"
          show-password
      /><br><br>
      <input type="checkbox" class="form-check-input" id="conf" checked v-model="userLoginKeyType">
      <label class="form-check-label" for="conf" style="font-size: small;">
        &nbsp;使用联系方式登录<br>不勾选则使用账号登录
      </label><br>
    </div>
  </div>
  <div id="lm-div05">
    <el-button type="primary" @click="LoginBtn()">登录</el-button>
    <el-button type="success" @click="openInNewTab('/Register')">注册</el-button>
  </div>
  <div style="height: 3rem; font-size: 1.25rem; margin-bottom: 0.75rem; text-align: center;">
    &copy; 2023~2025 DU Yu (MKTY Sys. Developer) All Rights Reserved.
  </div>
</div>
</template>

<style scoped>
@font-face
{
  font-family: HPHS;
  src:url("/fonts/HPHS.woff");
}
@font-face {
  font-family: hanwang;
  src: url("/fonts/hanwang.woff2");
}
#lm-mainDiv
{
  height: 100%;
  width: 100%;
  background-image: url("/images/05.jpg");
  background-size: cover;
  background-attachment: fixed;
  background-repeat: no-repeat;
  overflow: auto;
  font-size: 2rem;
  justify-items: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh
}
#lm-div02
{
  width: 85%;
  margin-top: 2rem;
  text-align: center;
  font-family:hanwang, serif;
}
#lm-div03
{
  width: 85%;
  font-size: 1.25rem;
}
#lm-div04
{
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  width: 85%;
}
#lm-div05
{
  display: flex;
  justify-content: center;
  margin-top: 2.5rem;
  flex: 1;
}
</style>
