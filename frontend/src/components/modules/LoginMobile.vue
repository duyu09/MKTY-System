<script>
import {errHandle, msgHandle} from "../../utils/tools";
import {loginVerification, setToken} from "../../api/api";
import Cookies from "js-cookie";

export default
{
  name: "LoginMobile",
  data()
  {
    return{
      "userId":'',
      "password":'',
    }
  },
  mounted()
  {
    if(window.innerWidth>640){
      this.$router.push('/Login');
    }
  },
  methods:
      {
        LoginBtn()
        {
          if(this.userId===0||this.password==='')
          {
            msgHandle('请您输入账号和密码');
            return;
          }
          loginVerification(this.userId,this.password)
              .then(res=>{
                if(res.data.code===0)
                {
                  //登录成功
                  setToken(res.data.token);
                  Cookies.set('userId',this.userId);
                  this.$router.push('/main/HomePage');
                }
                else
                {
                  errHandle('警告：登录出错！');
                }
              })
              .catch(res=>{
                errHandle('警告：登录出错:'+res);
              })
        },
      }
}
</script>

<template>
<div id="lm-mainDiv">
  <div id="lm-div02">
    智能学习大平台<br>
    用户登录
  </div>
  <div id="lm-div04">
    <div id="lm-div03">

      请输入账号：<br><br>
      <el-input v-model="userId" placeholder="Please input" clearable /><br><br>
      请输入密码：<br><br>
      <el-input
          v-model="password"
          type="password"
          placeholder="Please input password"
          show-password
      />

    </div>
  </div>
  <div id="lm-div05">
    <el-button type="primary" @click="LoginBtn()">登录</el-button>
    <el-button type="success" @click="this.$router.push('/Register')">注册</el-button>
  </div>


</div>
</template>

<style scoped>
@font-face
{
  font-family: HPHS;
  src:url("../../assets/fonts/HPHS.woff");
}
#lm-mainDiv
{
  height: 100%;
  width: 100%;
  background-image: url("../../../src/assets/images/05.jpg");
  background-size: cover;
  background-attachment: fixed;
  background-repeat: no-repeat;
  overflow: auto;
  font-size: 2rem;
}
#lm-div02
{
  margin-top: 2rem;
  text-align: center;
  font-family:HPHS, serif;
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
}
#lm-div05
{
  display: flex;
  justify-content: center;
  margin-top: 2.5rem;
}
</style>