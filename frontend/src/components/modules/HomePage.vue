<script>
import { RouterLink, RouterView } from 'vue-router';
import { Star } from "@element-plus/icons-vue";
import 'element-plus/dist/index.css';
import Cookies from "js-cookie";
import {getUserInfo, readSignInContext, setToken, signIn} from "../../api/api";
import {errHandle, msgHandle} from "../../utils/tools";
export default
{
  name:'HomePage',
  components:
  {
    "Star":Star,
  },
  data()
  {
    var greetContext = '早上好';
    const currentHour = new Date().getHours();
    if(currentHour>=11 && currentHour<=13) greetContext='中午好';
    else if(currentHour>13 && currentHour<=18) greetContext='下午好';
    else if(currentHour>=5 && currentHour<11) greetContext='早上好';
    else greetContext='晚上好';
    return{
        HomePage_Name:'',
        GreetContext:greetContext,
        SignContext:'',
        SignState:0, //0=已打卡，1=未打卡
        HomePage_Div08_Style:'display:flex;',
        HomePage_Div08_Vice_Style:'display:none;',
        dialogFormVisible:false,
    }
  },
  methods:
  {
    isSigned:function ()
    {
        //假设已打卡(=0),别忘设置自我鼓励的文本。
        this.SignState=0;
    },
    ShowContext:function ()
    {
        if(this.SignState===0)
        {
            this.HomePage_Div08_Style='display:none;';
            this.HomePage_Div08_Vice_Style='display:flex;';
        }
        else
        {
            this.HomePage_Div08_Style='display:flex;';
            this.HomePage_Div08_Vice_Style='display:none;';
        }
    },
    signInFunction()
    {
      this.dialogFormVisible = true;
    },
    SureSignIn()
    {
      this.dialogFormVisible = false;
      signIn(Cookies.get('userId'),this.SignContext);
      msgHandle("签到成功！");
      setTimeout(()=>{this.$router.go(0);},1350);
    },
    setNullPersonalPage()
    {
      Cookies.set('PersonalPageAimUserId',0);
    },
  },
  mounted() 
  {
    const userId=Cookies.get('userId');
    let userName='null';
    getUserInformation(userId,userId)
        .then(res=>{
          if(res.data.code===1){errHandle('您的登录状态已过期，请重新登录。');return;}
          userName=res.data.data.userName;this.HomePage_Name=userName;
        })
        .catch(res=>{});
    readSignInContext(userId)
        .then(res=>{
          console.log(res);
          if(res.data.code===2 || res.data.context===0){this.SignState=1;}
          else {
            this.SignState=0;
            this.SignContext=res.data.context;
          }
          this.ShowContext();
        }).catch(res=>{errHandle('读取您的签到状态失败。')})

  },

}
</script>
<template>
    <div id="HomePage-MainDiv">
        <div id="HomePage-BlurDiv"></div>
        <div style="z-index: 10;position: relative;width:100%;">
        <div id="HomePage-Div01">
          <div id="HomePage-Div02">
            <span><nobr>Welcome To&nbsp;</nobr><wbr><nobr>我的青春不迷茫&nbsp;</nobr><wbr><nobr>智能学习大平台</nobr></span>
          </div>
        </div>
        <div id="HomePage-Div03">
          <div id="HomePage-Div04">
            <div id="HomePage-Div05">
                <div id="HomePage-Div06">
                    <span id="HomePage-Span01">{{ HomePage_Name }}</span>&nbsp;同学，{{ GreetContext }}
                </div>
                <div id="HomePage-Div07">
                    <div id="HomePage-Div08" :style="HomePage_Div08_Style">
                        <div id="HomePage-Div09" @click="signInFunction()">打卡签到</div>
                    </div>
                    <div id="HomePage-Div08-Vice" :style="HomePage_Div08_Vice_Style">
                        <div id="HomePage-Div09-Vice">{{ SignContext }}</div>
                    </div>
                </div>
            </div>


            <el-dialog v-model="dialogFormVisible" title="美好的今日鼓励自己的话语">
              <el-form>
                <el-form-item label="写下今天对自己想说的话：" :label-width="200">
                  <el-input v-model="SignContext" autocomplete="off" />
                </el-form-item>
              </el-form>
              <template #footer>
              <span class="dialog-footer">
<!--                 <el-button @click="dialogFormVisible = false">取消</el-button>-->
                 <el-button type="primary" @click="SureSignIn()">确认签到</el-button>
              </span>
              </template>
            </el-dialog>

            <div id="MOBdiv">
            <div class="HomePage-MenuRowDiv">
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell" >
                  <div class="HomePage-ButtonDiv" @click="() => { setNullPersonalPage();this.$router.push('/main/PersonalPage');}"><el-icon><Star /></el-icon>我的主页</div>
                </div>
              </div>
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell" >
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/GuideFuture/JobAndSalary')"><el-icon><Star /></el-icon>我的未来</div>
                </div>
              </div>
            </div>
            <div class="HomePage-MenuRowDiv">
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell">
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/Forum')"><el-icon><Star /></el-icon>论坛社团</div>
                </div>
              </div>
            </div>
            <div class="HomePage-MenuRowDiv">
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell" >
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/PsyChat')"><el-icon><Star /></el-icon>小智同学</div>
                </div>
              </div>
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell">
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/StartStudy')"><el-icon><Star /></el-icon>云上自习</div>
                </div>
              </div>
            </div>
            <div class="HomePage-MenuRowDiv">
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell">
                  <div class="HomePage-ButtonDiv"  @click="() => this.$router.push('/main/Resources')"><el-icon><Star /></el-icon>资源天地</div>
                </div>
              </div>
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell">
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/AimList')"><el-icon><Star /></el-icon>我的目标</div>
                </div>
              </div>
            </div>
            </div>
          </div>
        </div>
        <div id="HomePage-FooterDiv01">
            &copy; 2023 Intelligent Learning Platform Developer Team.
        </div>
        <div id="HomePage-FooterDiv02">
            &copy; 2023 ILP Developer Team.
        </div>
        </div>
    </div>
</template>
<style>
@font-face
{
    font-family: font01;
    src: url('../../assets/fonts/font01.woff');
}
@font-face
{
    font-family: HPHS;
    src: url('../../assets/fonts/HPHS.woff');
}
@font-face
{
    font-family: ubuntu;
    src: url('../../assets/fonts/ubuntu.woff2');
}
#MOBdiv
{
  display: none;
}
#HomePage-MainDiv
{
    width: 100%;
    height: 100%;
    text-align: center;
    /*background-image: url('../../assets/images/02.jpg');*/
    background-color: rgba(242, 223, 187, 0.25);
    background-size: cover;
    background-repeat: no-repeat;
    display: flex;
    flex-direction: row;
    align-content: center;
    flex-wrap: wrap;
}
#HomePage-Div01
{
    display: flex;
    justify-content: center;
}
#HomePage-Div02
{
    margin-top: 2.25rem;
    padding-top: 1.25rem;
    padding-bottom: 1.25rem;
    text-shadow: 1px 1px black;
    /*box-shadow: 0 0 0.8rem 0.4rem rgba(38, 38, 38, 1);*/
    text-align: center;
    width: 70%;
    font-family: font01,serif;
    font-size: 2.75rem;
    color: black;
    border-radius: 14px;
}
#HomePage-Div03
{
    display: flex;
    justify-content: center;
}
#HomePage-Div04
{
    margin-top: 1.85rem;
    padding-top: 1.25rem;
    padding-bottom: 1.25rem;
    font-size: 1rem;
    box-shadow: 0 0 0.8rem 0.4rem rgba(0,0,0,0.5);
    text-align: center;
    width: 70%;
    border-radius: 14px;
}
#HomePage-Div05
{
    margin-bottom: 1rem;
    display: flex;
}
#HomePage-Div06
{
    font-family: HPHS,serif;
    font-size: 1.4rem;
    flex-grow: 1;
    text-shadow: 0.5px 0.5px black;
    color: rgb(0, 0, 80);
}
#HomePage-Span01
{
    font-family: font01,serif;
    font-size: 1.55rem;
}
#HomePage-Div07
{
    flex-grow: 1;
}
#HomePage-Div08
{
    display: flex;
    justify-content: center;
}
#HomePage-Div09
{
    display:flex;
    justify-content: center;
    width: 60%;
    box-shadow: 0 0 0.8rem 0.25rem rgba(0,0,0,0.5);
    background-color: rgba(0,0,255,0.12);
    font-size: 1.35rem;
    font-family: HPHS,serif;
    border-radius: 10px;
    padding-top: 0.175rem;
    padding-bottom: 0.175rem;
    cursor: pointer;
}
#HomePage-Div09:hover
{
    background-color:rgba(0, 0, 255, 0.3);
}
#HomePage-Div09:active
{
    background-color:rgba(0, 0, 255, 0.45);
}
#HomePage-FooterDiv01,#HomePage-FooterDiv02
{
    margin-top: 5rem;
    margin-bottom: 2rem;
    color: #0f2d73;
    font-family: ubuntu,serif;
}
#HomePage-Div08-Vice
{
    display: flex;
    justify-content: center;
}
#HomePage-Div09-Vice
{
    font-family: HPHS,serif;
    font-size: larger;
    width: 80%;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    border-radius: 10px;
    background-color: rgba(255, 140, 0, 0.15);
    color: rgb(120, 0, 0);
}
.HomePage-ButtonDiv-Shell
{
    display: flex;
    justify-content: center;
    margin-top: 0.8rem;
    margin-bottom: 0.8rem;
}
.HomePage-ButtonDiv
{
    display:flex;
    justify-content: center;
    width: 60%;
    box-shadow: 0 0 0.8rem 0.25rem rgba(0,0,0,0.5);
    background-color: rgba(255, 90, 0, 0.2);
    font-size: 1.2rem;
    font-family: HPHS,serif;
    border-radius: 10px;
    padding-top: 0.35rem;
    padding-bottom: 0.35rem;
    cursor: pointer;
}
.HomePage-ButtonDiv:hover
{
    background-color:rgba(255, 90, 0, 0.3);
}
.HomePage-ButtonDiv:active
{
    background-color:rgba(255, 90, 0, 0.45);
}
.HomePage-MenuRowDiv
{
    display: flex;
}
@media screen and (max-width:40rem) 
{
    #HomePage-Div02
    {
        font-size: 2rem;
    }
    #HomePage-Div05
    {
        display: block;
    }
    #HomePage-MainDiv
    {
        background-image: url('../../assets/images/03.jpg');
        background-position-x: right;
        background-attachment: fixed;
        height: 100%;
        position: relative;
        overflow: auto;
    }
    #HomePage-BlurDiv
    {
        position:fixed;
        width: 100%;
        height: 100%;
        top:0;
        left:0;
        -webkit-backdrop-filter: blur(30px);
		backdrop-filter: blur(30px);
        z-index: 0;
    }
    #HomePage-Div07
    {
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    #HomePage-FooterDiv01
    {
        display: none;
    }
    #HomePage-FooterDiv02
    {
        display: block;
    }
    .HomePage-MenuRowDiv
    {
        display: block;
    }
    .HomePage-ButtonDiv-Shell
    {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .HomePage-ButtonDiv
    {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
}
@media screen and (min-width: 40rem)
{
    #HomePage-FooterDiv02
    {
        display: none;
    }
    #HomePage-FooterDiv01
    {
        display: block;
    }
}
@media screen and (max-width: 40rem)
{
  #MOBdiv
  {
    display: block;
  }
  #HomePage-FooterDiv02
  {
    color: white;
    margin-top: 3rem;
  }
}
</style>