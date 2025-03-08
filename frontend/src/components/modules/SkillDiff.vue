<script>
import { RouterLink, RouterView } from 'vue-router';
import Cookies from "js-cookie";
import {errHandle, successHandle} from "../../utils/tools";
import {addFlag, skillTest} from "../../api/api";

export default
{
    name:'SkillDiff',
    data()
    {
        return {
            userId:0,
            loading:false,
            SkillDiff_Context:'',
            SkillDiff_City:'',
            SkillDiff_Salary:6000,
            SkillDiff_SkillArr:'快来分析，看看你还欠缺哪些知识和技术 ~ ~',
            addAimDialogTableVisible:false,
        }
    },
    mounted()
    {
      this.userId=Cookies.get('userId');
      if(this.userId===0||this.userId===undefined||this.userId===null)
      {
        errHandle('读取用户信息错误，请重新登录系统。');
        return;
      }

    },
    methods:
        {
          Analyse()
          {
            this.loading=true;
            if(this.SkillDiff_City===''||this.SkillDiff_City===undefined||this.SkillDiff_City===null)
            {
              errHandle('请填写你期望工作的城市，精确到市级即可。');
              this.loading=false;
              return;
            }
            if(this.SkillDiff_Context===''||this.SkillDiff_Context===undefined||this.SkillDiff_Context===null)
            {
              errHandle('请填写你的语言描述。要不然AI没法预测哦！');
              this.loading=false;
              return;
            }
            skillTest(this.userId,1,this.SkillDiff_Salary,this.SkillDiff_City,'null',this.SkillDiff_Context)
                .then(res=>{
                  if(res.data.code===0)
                  {
                    const data = res.data;
                    this.SkillDiff_SkillArr=data.diff;
                    this.loading=false;
                  }
                }).catch(res=>{
              errHandle('知识与技术差距分析出现了错误：'+res);
              this.loading=false;
              return;
            });
          },
          addAim()
          {
            const context="学习有关 "+this.SkillDiff_SkillArr +" 的知识。";
            if(context===''||context===undefined||context===null)
            {
              errHandle('您不能添加一个没有内容地目标哦！');
              return;
            }
            addFlag(this.userId,context).then(res=>{
              if(res.data.code===0)
              {
                successHandle('你已成功添加一个目标，你可以前往‘我的目标’版块中查看你的目标清单。');
                this.addAimDialogTableVisible = false;
                setTimeout(()=>{this.$router.go(0);},1400);
              }
              else
              {
                errHandle('添加目标失败。');
                this.addAimDialogTableVisible = false;
                return;
              }
            }).catch(res=>{
              errHandle('添加目标失败：'+res);
              this.addAimDialogTableVisible = false;
              return;
            });
          }
        }
}
</script>
<template>
    <div id="SkillDiff-MainDiv" v-loading="loading" element-loading-text="AI正在为你分析..." element-loading-background="rgba(0, 0, 0, 0.125)">
      <div id="SkillDiff-Div01">
        <div id="SkillDiff-Div02">
            <el-input
            v-model="SkillDiff_Context"
            maxlength="500"
            placeholder="填写你现在掌握的知识与学会的技术，工作经验，学历，工作地点，公司规模与公司类型，快来看看什么岗位与薪资适合你!

比如:我掌握了SPSS，了解Python，数据库原理，本科学历，我是应届生，没有工作经验。规模100人位于济南的上市公司提供的工作。"
            show-word-limit
            type="textarea"
            :rows="5"
            />
        </div>
        <div id="SkillDiff-Div03">
            <el-card shadow="always">
                <div id="SkillDiff-Div04">
                  <span style="margin-bottom: 0.3rem;"><nobr>设置一个你能够接受的薪资数值：</nobr>&nbsp;</span>
                  <el-input-number v-model="SkillDiff_Salary" :step="500" :min="500" :max="100000" id="SkillDiff-inputNumber01" />
                  &nbsp;元
                </div>
            </el-card>
            <div id="SkillDiff-Div05">
              <el-input v-model="SkillDiff_City" placeholder="请填写你期望的工作城市" clearable />
            </div>
        </div>
      </div>
      <div id="SkillDiff-Div06">
        <div id="SkillDiff-Div07">
            <el-card shadow="always" id="SkillDiff-Label01">
                 你仍需了解或掌握的技术： <br>
                 <span style="color: blue;font-size: larger;margin-top: 0.5rem;">
                    {{ SkillDiff_SkillArr }}
                </span><br>
                <div style="text-align: right;margin-top: 0.75rem;">
                  <el-button type="success" round size="small" @click="this.addAimDialogTableVisible=true;">添加到我的目标库</el-button>
                </div>
            </el-card>
        </div>
        <div id="SkillDiff-Div08">
            <el-button type="primary" id="SkillDiff-Button01" round @click="Analyse();">一键分析</el-button>
        </div>
      </div>

      <el-dialog v-model="addAimDialogTableVisible" title="添加新目标">
        <el-form>
          <el-form-item>
            你要添加的目标内容是：<span style="font-weight: bolder;">
              学习有关&nbsp;{{ this.SkillDiff_SkillArr }}&nbsp;的知识。
            </span>
          </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
              <el-button @click="addAimDialogTableVisible=false;">取消</el-button>
              <el-button type="primary" @click="addAim()">
                添加为目标
              </el-button>
            </span>
        </template>
      </el-dialog>



    </div>
</template>
<style scoped>
/* #SkillDiff-MainDiv
{
    
} */
@font-face
{
    font-family: font01;
    src: url("../../assets/fonts/font01.woff");
}
@font-face 
{
    font-family: ubuntu;
    src: url("../../assets/fonts/ubuntu.woff2");
}
#SkillDiff-Div01
{
    display: flex;
}
#SkillDiff-Div02
{
    padding: 0.5rem;
    flex-grow: 2;
}
#SkillDiff-Div03
{
    padding: 0.5rem;
    flex-grow: 1;
}
#SkillDiff-Div04
{
    font-family: ubuntu;
    font-size: smaller;
}
#SkillDiff-Div05
{
    padding-top: 0.4rem;
}
#SkillDiff-Div06
{
    padding: 0.5rem;
    display: flex;
}
#SkillDiff-Div07
{
    box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
    font-family: font01;
    flex-grow: 2;
}
#SkillDiff-Div08
{
    text-align: center;
    margin-left: 1rem;
    border-radius: 8px;
    background-image: linear-gradient(to right, white, rgb(166, 234, 255));
    box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
    flex-grow: 1;
}
#SkillDiff-Button01
{
    position: relative;
    top:22.5%;
    height: 55%;
    width: 65%;
    font-size: larger;
}
#SkillDiff-Label01
{
    background-color: rgb(224, 248, 255);
}
@media screen and (max-width:40rem) 
{
    #SkillDiff-Div01
    {
        display: block;
    }
    #SkillDiff-Div05
    {
        padding-top: 0.8rem;
    }
    #SkillDiff-inputNumber01
    {
        padding: 0.5rem;
    }
    #SkillDiff-Div06
    {
        display: block;
    }
    #SkillDiff-Div08
    {
        margin: 0;
        margin-top: 1rem;
        height:6rem;
    }
    
}
</style>