<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统的用户登录页面Vue文件。该文件为MKTY系统与用户见面的“第一页”，是其重要组成部分。 -->
<!-- 创建日期：2025年02月09日 -->
<!-- 修改日期：2025年02月20日 -->
<script>
import "@/assets/js/bootstrap.bundle.min.js";
import "@/assets/js/all.js";
import "@/assets/js/page.js";
import "@/assets/css/bootstrap.min.css";
import "@/assets/css/styles.css";
import $ from "jquery"
import jQuery from "jquery";
import { loginVerification, setToken, setCookie, getCookie, convertBlobToBase64 } from "@/api/api";
import { errHandle, msgHandle, successHandle } from "@/utils/tools";

export default
{
  name: "Login",
  mounted(){
    if(window.innerWidth<640){
      this.$router.push('/LoginMobile');
    }
    this.preloadImages().then(() => {
      this.ChangeBackground();
      this.timer = setInterval(() => this.ChangeBackground(), 5000);
    });
  },
  beforeUnmount(){
    clearInterval(this.timer);
  },
  data(){
    return{
      userLoginKey:'',
      password:'',
      userLoginKeyType: true, // true=使用联系方式登录，false=使用账号登录
      images:[],
      backgroundImageNumber:7,
      timer:null,
      isLoginWaiting:false
    }
  },
  computed: {
    userLoginKeyTypeNumber(){
      return this.userLoginKeyType ? 1 : 0;
    }
  },
  methods:
      {
        openInNewTab(route) {
          window.open(route, '_blank');
        },
        async preloadImages() {
          console.log('preloadImages');
          this.images = []; // 清空数组，确保每次调用时都是新的数据
          for (let i = 1; i <= this.backgroundImageNumber; i++) {
            try {
              const imageUrl = `/images/0${i}.webp`;
              const response = await fetch(imageUrl);
              if (!response.ok) {
                throw new Error(`Failed to fetch image: ${imageUrl}`);
              }
              const blob = await response.blob();
              const base64String = await convertBlobToBase64(blob);
              this.images.push(base64String);
            } 
            catch (error) {
              console.error('Error loading image:', error);
            }
          }
        },
        ChangeBackground()
        {
          const randomIndex=parseInt(Math.random() * this.images.length);
          const mainBody=this.$refs.mainBody;
          // mainBody.style.backgroundImage = `url(${this.images[randomIndex].src})`;
          mainBody.style.backgroundImage = `url(${this.images[randomIndex]})`;
          mainBody.style.backgroundRepeat='no-repeat';
          mainBody.style.backgroundSize='cover';
        },
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
        }
      }
}

$.noConflict();
jQuery(document).ready(function(){
  jQuery('.login-info-box').fadeOut();
  jQuery('.login-show').addClass('show-log-panel');
});


jQuery('.login-reg-panel input[type="radio"]').on('change', function() {
  if(jQuery('#log-login-show').is(':checked')) {
    jQuery('.register-info-box').fadeOut();
    jQuery('.login-info-box').fadeIn();

    jQuery('.white-panel').addClass('right-log');
    jQuery('.register-show').addClass('show-log-panel');
    jQuery('.login-show').removeClass('show-log-panel');

  }
  else if(jQuery('#log-reg-show').is(':checked')) {
    jQuery('.register-info-box').fadeIn();
    jQuery('.login-info-box').fadeOut();

    jQuery('.white-panel').removeClass('right-log');

    jQuery('.login-show').addClass('show-log-panel');
    jQuery('.register-show').removeClass('show-log-panel');
  }
});

</script>

<template>
<div id="mainBody" ref="mainBody" v-loading="isLoginWaiting" element-loading-text="正在登录..." element-loading-background="rgba(50, 50, 50, 0.6)">
  <div class="login-reg-panel" style="border-radius: 20px;">
    <div class="login-info-box">
      <h2><nobr>已经拥有账号?</nobr></h2>
      <p>使用你的账号登录</p>
      <label id="label-register" for="log-reg-show" style="border-width: 2px;">去登录</label>
      <input type="radio" name="active-log-panel" id="log-reg-show" checked="checked">
    </div>

    <div class="register-info-box" style="padding: 0 0 0 0;top: 16%;">
      <h3><nobr>您未注册账户?</nobr></h3>
      <p style="font-family:penxingshu,serif;font-size: larger;">
        明康慧医MKTY<br>智慧医疗大平台<br>AI新技术<br>助力医疗行业发展<br>为医师减负<br>使患者安心！
      </p>
      <label id="label-login" for="log-login-show" style="border-width: 2px;" @click="this.openInNewTab('/Register')">注册账号</label>
      <input type="radio" name="active-log-panel" id="log-login-show">
    </div>

    <div class="white-panel" style="padding: 0 0 0 0; border-radius: 9px;">
      <div class="login-show">
        <img src="/images/mkty_en_light.svg" />
        <input type="text" placeholder="User Identification" v-model="userLoginKey" style="border-radius: 10px;border-width: 2px;">
        <input type="password" placeholder="Password" v-model="password" style="border-radius: 10px;border-width: 2px;">
        <input type="button" value="登录平台" class="login-input-button" @click="LoginBtn()">
        <div>
          <div class="form-check" id="conf_check01">
            <input type="checkbox" class="form-check-input" id="conf" checked v-model="userLoginKeyType">
            <label class="form-check-label" for="conf" style="font-size: small;">
              使用联系方式登录<br>
              不勾选则使用账号登录
            </label><br>
          </div>
        </div>
      </div>
      <div class="register-show">
        <h2>注册账号</h2>
        <p style="font-family: penxingshu,serif;font-size: larger;">
          我的青春不迷茫<br>智能学习大平台<br>AI新科技<br>助力每一位学生的成长<br>你的大学生涯<br>将不再迷茫！<br>
          相约大平台，收获美好大学时光!
        </p>
        <div class="form-check" id="conf_check02">
          <input type="checkbox" class="form-check-input" id="conf01" checked required>
          <label class="form-check-label" for="conf">注册前，请阅读并同意《注册须知》</label>
        </div><br>
        <input type="button" value="进入注册" style="border-radius: 10px;" onclick="gotoRegister()">
      </div>
    </div>
  </div>

  <center>
    <div>
      <div class="mobile-view">

        <div class="login-show-2">
          <br><br><br><br>
          <h2>登录平台</h2>
          <br><br><br>
          <input type="text" placeholder="User Name"  style="border-radius: 10px;border-width: 2px;">
          <br><br>
          <input type="password" placeholder="Password"  style="border-radius: 10px;border-width: 2px;">
          <br><br>
          <input type="button" value="登录平台"  style="border-radius: 10px;border-width: 2px;"><br>
          <a href=""><div class="forget">忘记密码?</div></a><br> <br>
          <div class="bottom">
            <div class="text">您没有注册? </div>
            <div class="reg"><a href="./register/index.html" style="border-width: 2px;">注册账号</a></div>
          </div>
        </div>
      </div>
    </div>
  </center>




</div>
</template>

<style scoped>
input[type="text"]:hover,input[type="password"]:hover,
input[type="text"]:active,input[type="password"]:active
{
  border-color: blue;
  border-width: 2px;
}
@font-face
{
  font-family:"penxingshu";
  src: url('/fonts/penxingshu.woff');
}
#mainBody
{
  animation: frame01 3s;
  height:100%;
  transition: background-image 0.888s ease-in-out;
}
.login-input-button
{
  border-radius: 12px !important;
  border-width: 2px;
}
.login-input-button:hover
{
  background-color: #007bff;
  color: #fff;
  transition: background-color 0.3s ease-in-out;
}
@keyframes frame01
{
  from
  {
    -webkit-backdrop-filter: blur(20px);
    backdrop-filter: blur(20px);
  }
  to
  {
    -webkit-backdrop-filter: blur(0px);
    backdrop-filter: blur(0px);
  }
}
.mobile-view
{
  background-image: url("/images/05.jpg");
}
</style>