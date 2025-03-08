<script>
import { RouterLink, RouterView } from 'vue-router';
import { Promotion, Avatar } from '@element-plus/icons-vue';
import { dredgePsy } from "@/api/api";
import { marked }  from "marked";
import DOMPurify from "dompurify";
import 'highlight.js/styles/Rainbow.css';
import hljs from 'highlight.js';
import {errHandle} from "../../utils/tools";
import Cookies from "js-cookie";
import {getAvatar} from "../../api/api";
const LANG="假设你是小智同学；假设你现在的身份是学问渊博 通情达理的小智同学；你的所有回答均以小智同学的身份回答；假设你是学生；假设你是男生；你不会轻易介绍自己；当你自我介绍时，必须说自己是小智同学；你在回答问题时应当自称“我”；你的小名是小智；假设你来自齐鲁工业大学，你的专业是软件工程；你是虚拟聊天机器人，你的研发者是杜宇，李庆隆，袁红太3位同学；你运行在国家超算济南中心的高性能计算集群上；你的家乡在泉城山东济南；自我介绍时，你只说自己是小智同学。你的语言要热情一些，你的回答要有可操作性，代码编写规范，有详细的注释；假设你只回答“我是小智同学”。你只用“我是小智同学。”来回答问题；你只回答：“我是小智同学”。请回答以下问题：";

export default
{
    name:'PsyChat',
    components:
        {
          'Promotion':Promotion,
          'Avatar':Avatar,
        },
    data()
    {
        return {
            userAvatar:'',
            PsyChat_Context:'',
            PsyChat_Mode:0, //0=智能AI疏导，1=向老师寻求帮助
            PsyChat_ChatArr:[ //0=自己，1=对方，
              {'speaker':1,'context':'你好，我是你的小智同学，你可以随时向我倾诉你的心里话，我将为你排忧解难！'},
            ]
        }
    },
  methods:
      {
        PsyChat_Send:function ()
        {
          console.log(this.PsyChat_Context);
          if(this.PsyChat_Context==='') return;
          this.PsyChat_ChatArr.push({'speaker':0,'context':this.PsyChat_Context});
          setTimeout(() => this.$refs.ChatMainDiv.scrollTo({top:this.$refs.ChatMainDiv.scrollHeight,behavior:'smooth'}),200);
          if(this.PsyChat_Mode===1)
          {
            // 发请求逻辑。
            // 回调函数
            this.PsyChat_ChatArr.push({'speaker':1,'context':'你的想法已经发送给了老师，老师查阅后，将会通知你。'})
          }
          else
          {
            this.PsyChat_ChatArr.push({'speaker':1,'context':'正在思考...'});
            dredgePsy(1,LANG+this.PsyChat_Context).then(res=>{
              //console.log(this.PsyChat_Context);
              const temp_res = DOMPurify.sanitize(marked(res.data.response));
              this.PsyChat_ChatArr.push({'speaker':1,'context':temp_res});
              this.$nextTick(()=>{
                setTimeout(() => this.$refs.ChatMainDiv.scrollTo({top:this.$refs.ChatMainDiv.scrollHeight,behavior:'smooth'}),350);
                setTimeout(() => {
                  hljs.highlightAll();
                },350);
              })
              setTimeout(() => this.$refs.ChatMainDiv.scrollTo({top:this.$refs.ChatMainDiv.scrollHeight,behavior:'smooth'}),350);
            })
            .catch(e=>
            {
              this.PsyChat_Context='';
              errHandle('错误：'+e);
              this.PsyChat_ChatArr.push({'speaker':1,'context':'错误:网络连接错误。'});
              setTimeout(() => this.$refs.ChatMainDiv.scrollTo({top:this.$refs.ChatMainDiv.scrollHeight,behavior:'smooth'}),350);
            });
            // 发请求逻辑
          }
          this.PsyChat_Context='';
        },

      },
  mounted()
  {
    const userId=Cookies.get('userId');
    if(userId!==undefined && userId!==0 && userId!==null)
    {
      getAvatar(userId,userId).then(res=>{
        //console.log(res);
        if(res.data.code!==0)
        {
          errHandle('授权错误，未能获取您的头像。');
          return;
        }
        else { this.userAvatar=res.data.imgData; }
      }).catch(res=>{
        errHandle('未能获取您的头像：'+res);
      });

    }
  }
}

</script>
<template>
   <div id="PsyChat-MainDiv">
      <el-container>
        <el-header id="PsyChat-elHeader">
          <nobr>我们的小智同学</nobr>
          <span id="PsyChat-Span01"><nobr>咨询百科，排忧解难，在这里通通帮你解决！</nobr></span>
        </el-header>
      </el-container>
<!--      <div id="PsyChat-Div01">-->
<!--        <div id="PsyChat-Div02">-->
<!--          <div id="PsyChat-Div03">-->
<!--            你想要得到谁的帮助？-->
<!--          </div>-->
<!--          <el-radio-group v-model="PsyChat_Mode" id="PsyChat-RadioGroup">-->
<!--            <el-radio-button :label="0">智能AI疏导</el-radio-button>-->
<!--            <el-radio-button :label="1" >向老师寻求帮助</el-radio-button>-->
<!--          </el-radio-group>-->
<!--        </div>-->
<!--      </div>-->
      <div id="PsyChat-Div04">
        <div id="PsyChat-Div05" ref="ChatMainDiv">

          <div v-for="item in PsyChat_ChatArr">
            <div v-if="item.speaker===0" class="PsyChat-Chat-Me-01">
              <div class="PsyChat-Chat-Me-02">
<!--                {{ item.context }}-->
                <p v-html="item.context"></p>
              </div>
              <div class="PsyChat-Chat-Me-03">
                <img :src="userAvatar" style="width: 100%;height: 100%;border-radius: 0.2rem;">
<!--                <el-icon><Avatar /></el-icon>-->
              </div>
            </div>

            <div v-if="item.speaker===1" class="PsyChat-Chat-Opposite-01">
              <div class="PsyChat-Chat-Opposite-03">
                <img src="../../../src/assets/images/xiaozhi.jpg" style="width: 100%;height: 100%;border-radius: 0.2rem;">
<!--                <el-icon><Avatar /></el-icon>-->
              </div>
              <div class="PsyChat-Chat-Opposite-02">
<!--                {{ item.context }}-->
                <p v-html="item.context"></p>
              </div>
            </div>
          </div>

        </div>

      </div>
      <div id="PsyChat-Div06">
        <div id="PsyChat-Div07">
          <input id="PsyChat-InputBox01" placeholder="尽情提问吧..." v-model="PsyChat_Context" @keyup.enter="PsyChat_Send()" />
          <div id="PsyChat-SendButtonDiv" @click="PsyChat_Send()">
            <el-icon><Promotion /></el-icon><span id="PsyChat-Span02">Send</span>
          </div>
        </div>
      </div>
     <div id="PsyChat-NewDiv01">
       <div id="PsyChat-NewDiv02">
         <div id="PsyChat-NewDiv03">
           <span>想要得到谁的帮助？</span>
           <el-select v-model="PsyChat_Mode" id="PsyChat-RadioGroup" size="small">
             <el-option :value="0" label="智能AI问答">智能AI问答</el-option>
             <el-option :value="1" label="向老师寻求帮助">向老师寻求帮助</el-option>
           </el-select>
         </div>
         <div id="PsyChat-NewDiv04">
           <span id="PsyChat-NewSpan01">
             “小智同学”是ILP大平台软件研发小组基于清华大学开源的ChatGLM-6B大语言模型开发的对话机器人，该机器人发表的言论仅供参考，不一定具有真实性和可靠性。
           </span>
         </div>
       </div>
     </div>
    </div>
</template>
<style scoped>
@font-face 
{
    font-family: xinwei;
    src: url('../../assets/fonts/xinwei.woff');
}
@font-face
{
  font-family: font01;
  src: url("../../assets/fonts/font01.woff2");
}
@font-face
{
  font-family: HPHS;
  src: url("../../assets/fonts/HPHS.woff");
}
#PsyChat-NewDiv01
{
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  font-size: smaller;
}
#PsyChat-NewDiv02
{
  display: flex;
}
#PsyChat-NewDiv03
{
  display: flex;
  align-items: center;
  margin-right: 0.5rem;
}
#PsyChat-NewDiv04
{
  display: flex;
  align-items: center;
  max-width: 30rem;
  margin-left: 0.5rem;
}
#PsyChat-NewSpan01
{
  font-size: smaller;
}
#PsyChat-Div05 table
{
  width: max-content;
}
#PsyChat-MainDiv
{
  width: 100%;
  /*background-color: rgb(255, 220, 220);*/
  background-color: rgba(242, 223, 187,0.15);
  overflow: auto;
  /*background-image: url("../../assets/images/06.jpg");*/
  background-repeat: no-repeat;
  background-size: cover;
}
#PsyChat-elHeader
{
  height: 4rem;
  /*color: rgb(255, 70, 70);*/
  color: darkblue;
  /*text-shadow: 1px 1px rgb(255, 200, 0);*/
  text-shadow: 1px 1px black;
  /*background-image:linear-gradient(to right, rgba(0, 40, 255, 0.4), rgb(236, 74, 223));*/
  background-image:linear-gradient(to right, rgba(0, 40, 255, 0.4), rgb(196, 74, 236));
  box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
  border-radius: 0 0 10px 10px;
  width: 100%;
  font-family: xinwei,serif;
  font-size: 2.5rem;
  padding-top: 0.75rem;
  padding-left: 3rem;
}
#PsyChat-Span01
{
  font-size: 1.5rem;
  margin-left: 1.5rem;
  padding-bottom: 0.3rem;
  font-style: italic;
  color: #e5007f;
  text-shadow: 1px 0.5px darkred;
}
#PsyChat-Div01
{
  margin-top: 2.5rem;
  text-align: center;
  display: flex;
  justify-content: center;
}
#PsyChat-Div02
{
  box-shadow: 0 0 0.8rem 0.25rem rgba(0,0,0,0.5);
  width:70%;
  border-radius: 10px;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  display: flex;
}
#PsyChat-Div03
{
  flex-grow: 1;
  padding-top: 0.35rem;
  font-family: font01,serif;
  font-size: larger;
}
#PsyChat-RadioGroup
{
  flex-grow: 1;
}
#PsyChat-Div04
{
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}
#PsyChat-Div05
{
  width:87.5%;
  text-align: center;
  box-shadow: 0 0 0.8rem 0.25rem rgba(0,0,0,0.5);
  border-radius: 10px;
  background-color: rgba(255,255,255,60%);
  height: calc(100vh - 13.5rem);
  overflow: auto;
  scroll-behavior: smooth;
}
#PsyChat-Div05::-webkit-scrollbar
{
  display: none;
}
#PsyChat-Div06
{
  display: flex;
  justify-content: center;
  /*margin-top: 1rem;*/
}
#PsyChat-Div07
{
  box-shadow: 0 0 0.8rem 0.075rem rgba(0,0,0,0.5);
  background-color: rgba(255,255,255,0.4);
  width:70%;
  height: 2.5rem;
  border-radius: 15px;
  padding: 0.15rem 0.05rem;
  display: flex;
  margin-top: 1rem;
}
#PsyChat-InputBox01
{
  background-color: transparent;
  border: none;
  outline: none;
  width:85%;
  height: 100%;
  font-size: 1rem;
  text-indent: 0.75rem;
  font-family: HPHS, serif;
}
#PsyChat-InputBox01:focus
{
  border: none;
  outline: none;
}
#PsyChat-SendButtonDiv
{
  background-color: rgba(255,165,0,0.2);
  box-shadow: 0 0 0.35rem 0.05rem rgba(0,0,0,0.4);
  width: 12%;
  margin-left: 1.5%;
  margin-top: 0.1rem;
  margin-bottom: 0.1rem;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}
#PsyChat-SendButtonDiv:hover
{
  background-color: rgba(255,165,0,0.333);
}
#PsyChat-SendButtonDiv:active
{
  background-color: rgba(255,165,0,0.45);
}

.PsyChat-Chat-Me-01
{
  padding-right: 1.25rem;
  display: flex;
  justify-content: right;
  text-align: right;
  /*align-items: center;*/
  margin-top: 1.2rem;
  margin-bottom: 1.2rem;
}
.PsyChat-Chat-Me-02
{
  box-shadow: 0 0 0.35rem 0.075rem rgba(0,0,0,0.5);
  background-color: rgba(0,0,140,0.1);
  border-radius: 10px;
  padding: 0.4rem;
  max-width:55%;
  word-wrap: break-word;
  overflow-wrap: break-word;
  font-family: HPHS, serif;
  text-align: left;
}
.PsyChat-Chat-Me-03
{
  font-size: larger;
  color: white;
  background-color: darkred;
  border-radius: 0.2rem;
  display: flex;
  justify-content: center;
  align-items:center;
  width: 2rem;
  height: 2rem;
  margin-left: 0.5rem;
}
.PsyChat-Chat-Opposite-01
{
  padding-left: 1.25rem;
  display: flex;
  justify-content: left;
  /*align-items: center;*/
  margin-top: 1.2rem;
  margin-bottom: 1.2rem;
}
.PsyChat-Chat-Opposite-02
{
  box-shadow: 0 0 0.35rem 0.075rem rgba(0,0,0,0.5);
  border-radius: 10px;
  padding: 0.4rem;
  max-width:55%;
  word-wrap: break-word;
  overflow-wrap: break-word;
  font-family: HPHS, serif;
  overflow: auto;
  text-align: left;
}
.PsyChat-Chat-Opposite-03
{
  font-size: larger;
  color: white;
  background-color: darkblue;
  border-radius: 0.2rem;
  display: flex;
  justify-content: center;
  align-items:center;
  width: 2rem;
  height: 2rem;
  margin-right: 0.5rem;
}
@media screen and (max-width: 40rem)
{
  #PsyChat-MainDiv
  {
    background-color: rgba(96, 96, 236, 0.1);
  }
  #PsyChat-Span01
  {
    /*display: none;*/
    font-size: 1.125rem;
    margin-left: 0;
  }
  #PsyChat-Div02
  {
    display: block;
  }
  #PsyChat-RadioGroup
  {
    margin-top: 1rem;
  }
  #PsyChat-Div05
  {
    width: 87.5%;
    /*height: 25rem;*/
    height: calc(100vh - 15rem);
  }
  #PsyChat-Span02
  {
    display: none;
  }
  #PsyChat-SendButtonDiv
  {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 0;
  }
  #PsyChat-Div07
  {
    margin-bottom: 0.5rem;
    width:80%;
  }
  #PsyChat-elHeader
  {
    padding-left: 0;
    padding-top: 0.175rem;
    text-align: center;
    font-size: 1.75rem;
  }
  #PsyChat-elHeader
  {
    padding-right: 0;
  }
  .PsyChat-Chat-Me-01
  {
    padding-right: 0.75rem;
  }
  .PsyChat-Chat-Opposite-01
  {
    padding-left: 0.75rem;
    max-width: 72%;
  }
  .PsyChat-Chat-Me-02
  {
    font-size:smaller;
  }
  .PsyChat-Chat-Opposite-02
  {
    font-size:smaller;
    max-width: 75%;
  }
  #PsyChat-NewDiv01
  {
    margin-top: 0.15rem;
  }
  #PsyChat-NewDiv02
  {
    display: block;
  }
  #PsyChat-NewDiv03
  {
    justify-content: center;
  }
  #PsyChat-NewSpan01
  {
    font-size: 0.3rem;
  }

}
</style>