<script>
import { RouterLink, RouterView } from 'vue-router';
import Cookies from "js-cookie";
import {errHandle} from "../../utils/tools";
import {skillTest} from "../../api/api";
import SalaryShow from "../modules/SalaryShow.vue";

export default
{
    name:'JobAndSalary',
    components:
        {
          'SalaryShow':SalaryShow,
        },
    data()
    {
        return {
            loading:false,
            dialogFormVisible:false,
            userId:0,
            JobAndSalary_Context:'',
            JobAndSalary_City:'',
            JobAndSalary_Job:'快来看看，什么工作适合你 ~ ~',
            JobAndSalary_Salary:0,
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
            if(this.JobAndSalary_City===''||this.JobAndSalary_City===undefined||this.JobAndSalary_City===null)
            {
              errHandle('请填写你期望工作的城市，精确到市级即可。');
              this.loading=false;
              return;
            }
            if(this.JobAndSalary_Context===''||this.JobAndSalary_Context===undefined||this.JobAndSalary_Context===null)
            {
              errHandle('请填写你的语言描述。要不然AI没法预测哦！');
              this.loading=false;
              return;
            }
            skillTest(this.userId,0,0,this.JobAndSalary_City,'',this.JobAndSalary_Context)
            .then(res=>{
              if(res.data.code===0)
              {
                const data = res.data;
                if(data.salary<2000) { this.JobAndSalary_Salary=2000; }
                else if(data.salary>30000){ this.JobAndSalary_Salary=30000; }
                else { this.JobAndSalary_Salary=data.salary; }
                this.JobAndSalary_Job=data.job;
                Cookies.set('Salary',this.JobAndSalary_Salary);
                this.dialogFormVisible=true;
                this.loading=false;
              }
              else
              {
                errHandle('岗位与薪资预测出现了权限错误：您的登录状态已过期。');
                this.loading=false;
                return;
              }
            }).catch(res=>{
              errHandle('岗位与薪资预测出现了错误：'+res);
              this.loading=false;
              return;
            });
          }
        }
}
</script>
<template>
<div id="JobAndSalary-MainDiv"  v-loading="loading" element-loading-text="AI正在为你分析..." element-loading-background="rgba(0, 0, 0, 0.125)">
    <div> </div>
    <el-input
    v-model="JobAndSalary_Context"
    maxlength="500"
    placeholder="填写你现在掌握的知识与学会的技术，工作经验，学历，工作地点，公司规模与公司类型，快来看看什么岗位与薪资适合你!
比如:我掌握了SPSS，了解Python，数据库原理，本科学历，我是应届生，没有工作经验。规模100人位于济南的上市公司提供的工作。"
    show-word-limit
    type="textarea"
    rows="5"
    id="JobAndSalary-textArea01"
    />
    <div id="JobAndSalary-div-01">
      <div id="JobAndSalary-div-02">
        <div id="JobAndSalary-textbox01"><el-input v-model="JobAndSalary_City" placeholder="填写您期望的工作城市" clearable /></div>
        <el-card shadow="always" id="JobAndSalary-label01"> 
            <div style="font-family: font01;font-size: larger;">
                <span>建议你从事：</span>
                <span style="color: blue;">{{ JobAndSalary_Job }}</span>
            </div>
            <el-divider />
            <div  style="font-family: font01;font-size: larger;">
                <span>预测你的月薪：</span>
                <span style="font-family: ubuntu;color: blue;">{{ JobAndSalary_Salary }}</span>
                <span style="color: blue;">&nbsp;元</span>
            </div>
        </el-card>
      </div>
      <div id="JobAndSalary-div-03">
        <el-button type="primary" id="JobAndSalary-Button01" round @click="Analyse();">一键分析</el-button>
      </div>
    </div>

  <el-dialog v-model="dialogFormVisible" title="AI分析结果" destroy-on-close :width="500">
    <el-form>
      <el-form-item label="我们预测了你目前的知识与技术掌握情况可能拿到的薪资">
      </el-form-item>
      <el-form-item>
        目前建议你的岗位是：<b>{{JobAndSalary_Job}}</b>
      </el-form-item>
      <div style="width: 100%;height: 275px;">
        <SalaryShow style="width: 450px;height: 375px;" ></SalaryShow>
      </div>

    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="dialogFormVisible = false;" style="z-index: 0;position: relative;">
          关闭
        </el-button>
      </span>
    </template>
  </el-dialog>

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
#JobAndSalary-textArea01
{
    background-color: white;
}
#JobAndSalary-div-01
{
    padding-top: 1rem;
    display: flex;
}
#JobAndSalary-div-02
{
    flex-grow: 3;
}
#JobAndSalary-div-03
{
    text-align: center;
    margin-left: 1rem;
    border-radius: 10px;
    background-image: linear-gradient(to right, white, rgb(166, 234, 255));
    box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
    flex-grow: 1;
}
#JobAndSalary-textbox01
{
    /* width: 85%; */
    margin-bottom: 1rem;
}
#JobAndSalary-label01
{
    background-color: rgb(224, 248, 255);
    box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
}
#JobAndSalary-Button01
{
    position: relative;
    top:32%;
    height: 40%;
    width: 55%;
    font-size: larger;
}
@media screen and (max-width:40rem)
{
    #JobAndSalary-div-01
    {
        display: block;
    }
    #JobAndSalary-div-03
    {
        margin-top: 1.2rem;
        margin-left: 0;
        background-image: linear-gradient(to right, transparent, transparent);
        box-shadow: none;
    }
    #JobAndSalary-Button01
    {
       height: 4rem;
       position: relative;
       width: 55%;
       font-size: larger;
    }
}
</style>