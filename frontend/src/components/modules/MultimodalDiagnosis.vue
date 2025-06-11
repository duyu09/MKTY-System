<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统多模态辅助诊断功能模块Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年02月01日 -->
<!-- 修改日期：2025年03月09日 -->
<script>
import { Star, Opportunity, Promotion, Document, Setting } from "@element-plus/icons-vue";
import 'element-plus/dist/index.css';
import "@/assets/css/file_input.css";
import "@/assets/css/colorful_div.css";
import { getUserInfo, getCookie, multimodalDiagnosisGetStatus, multimodalDiagnosisSubmitTask } from '@/api/api';
import { errHandle } from  "@/utils/tools";
import * as echarts from 'echarts/core';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components';
import { PieChart } from 'echarts/charts';
import { LabelLayout } from 'echarts/features';
import { SVGRenderer } from 'echarts/renderers';

echarts.use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  PieChart,
  SVGRenderer,
  LabelLayout
]);

export default
{
    name:'MultimodalDiagnosis',
    compilerOptions: 
    {
      isCustomElement: tag => tag === 'nobr'
    },
    components:
    {
      "Star":Star,
      "Opportunity":Opportunity,
      "Promotion":Promotion,
      "Document":Document,
      "Setting":Setting
    },
    data()
    {
      return{
        md_userId:'',
        md_userType:-1,  // 0=患者，1=医师，2=其他人员，-1=正在加载
        md_userTypeText:'',  // 字符串“患者”、“医师”、“其他人员”、“正在加载”
        md_input:'',
        md_resultFormVisible:false,
        md_resultTableFormVisible:false,
        md_img_base64String:'',
        md_showDataArr: [],
        md_showDataTable:[],
        md_conclusion:'',
        md_el_avatar_01_src:'/images/null_avatar.jpg',
        md_text_language:'zh',
        text_table: [],  // 元素格式：{ text: '严重的肺气肿' }, 
        md_analyzing: false,
      }
    },
    methods: 
    {
      md_pageLoad()
      {
        this.md_userId = parseInt(getCookie('userId'));
        // console.log(this.md_userId);
        getUserInfo(this.md_userId).then((res) => {
          this.md_userType = res.data.userInfo.userType;
          if (this.md_userType == 0) this.md_userTypeText = '患者';
          else if (this.md_userType == 1) this.md_userTypeText = '医师';
          else if (this.md_userType == 2) this.md_userTypeText = '其他人员';
          else this.md_userTypeText = '正在加载...';
        });
      },
      deleteRow(index){
        this.text_table.splice(index, 1);
      },
      addRow(){
        if (this.md_input == '') return;
        this.text_table.push({text: this.md_input});
        this.md_input = '';
      },
      showResult(){
        var chartDom = document.getElementById('md_resultShowDiv');
        var myChart = echarts.init(chartDom, null, {
          renderer: 'svg'
        });
        var option;
        option = {
          title: {
            text: '多模态AI辅助分析结果',
            subtext: '计算机分析仅供参考',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: 'Access From',
              type: 'pie',
              radius: '50%',
              data: this.md_showDataArr,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        };
        option && myChart.setOption(option);
      },
      encodeFileToBase64(file, callback){
        const reader = new FileReader();
        reader.onload = (event) => {
          const base64 = event.target.result;
          callback(base64);
        };
        reader.readAsDataURL(file); // 读取文件为 Data URL
      },
      handleFileChange(){
        const file = this.$refs.md_imgShow.files[0];
        if (file) {
          this.encodeFileToBase64(file, (result) => {
            this.md_img_base64String = result;
            this.md_el_avatar_01_src = result;
            // console.log(this.md_img_base64String);
          });
        } else {
          this.md_img_base64String = ''; // 清空结果
        }
      },
      getResult(){
        this.md_analyzing = true;
        this.md_showDataTable = [];
        this.md_showDataArr = [];
        var text_arr = [];
        for (var i = 0; i < this.text_table.length; i++){
          text_arr.push(this.text_table[i].text);
        }
        multimodalDiagnosisSubmitTask(this.md_text_language, text_arr, this.md_img_base64String).then((res) => {
          if(res.data.code != 0) { 
            errHandle("未成功发送数据：" + res.data.msg);
            this.md_analyzing = false;
            return;
          }
          const task_id = res.data.taskId;

          const interval_id = setInterval(() => {
            multimodalDiagnosisGetStatus(task_id).then((res2) => {
              if(res2.data.code != 0) { 
                clearInterval(interval_id);
                errHandle("未成功获取响应：" + res2.data.msg);
                this.md_analyzing = false;
                return;
              }
              if (res2.data.taskStatus == 0){
                clearInterval(interval_id);
                const task_result = res2.data.taskResult;
                const labels = task_result.labels;
                const logits = task_result.logits;
                for (var i = 0; i < labels.length; i++){
                  this.md_showDataTable.push({english_text: labels[i], rate: (logits[i] * 100).toFixed(3) + '%'});
                  this.md_showDataArr.push({value: logits[i], name: this.text_table[i].text});
                }
                const logits_max_index = logits.reduce((maxIdx, currentValue, currentIndex, arr) => {
                  return currentValue > arr[maxIdx] ? currentIndex : maxIdx;
                }, 0);
                this.md_conclusion = this.text_table[logits_max_index].text;
                this.md_resultFormVisible = true;
                this.md_analyzing = false;
              }
            });
          }, 3210);

        });

        
        
      }
    },
    mounted()
    {
      this.md_pageLoad();
      
    }
};
</script>
<template>
    <div class="common-layout" id="MultimodalDiagnosis-common-layout">
    <el-container style="height: 100%;">
      <el-container style="height: 100%;">
        <el-header id="MultimodalDiagnosis-elHeader">
            <div id="MultimodalDiagnosis-elHeader-title01">
              <div id="MultimodalDiagnosis-elHeader-title03">
                <nobr>智能多模态诊断</nobr>
              </div>
              <div id="MultimodalDiagnosis-elHeader-title02">
                <nobr>基于BiomedCLIP的计算机智能多模态辅诊</nobr><br>
                <span id="MultimodalDiagnosis-elHeader-title04">
                  <nobr>Multimodal Intelligent Computer Auxiliary Diagnosis Based on BiomedCLIP</nobr>
                </span>
              </div>
            </div>
        </el-header>
        <el-main>
          <div style="display: flex; flex-direction: column;height: 100%;">
          <div style="font-family: HPHS;">
            <el-card shadow="always" style="width: 100%;box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);"> 
              <div id="MultimodalDiagnosis-Label01">
                <div style="padding-bottom: 0.2rem;">
                  <el-icon><Star /></el-icon>
                  使用方法：请您上传一张关于病情的图片，可以是CT、MRI、X光片等各类医学影像。
                  然后请您输入多个针对该图像的诊断描述文本，系统将展示一个概率分布，表明您各个描述的相对正确的概率，从而辅助您决策。
                  <b>注意，概率值大不代表对应描述一定正确，仅代表该描述与其他描述相比之下相对正确的概率。</b>
                </div>
                <div style="padding-bottom: 0.3rem;">
                  <el-icon><Star /></el-icon>
                  BiomedCLIP模型仅支持英文，若您选择以中文的方式输入，则系统后台会先将中文翻译成英文，再进行模型推理。
                  若您为专业医师，建议您使用英文描述，以获得更好的推理效果。
                </div>
                <div style="padding-bottom: 0.3rem;" v-if="md_userType == 1">
                  <el-icon><Star /></el-icon>
                  您的身份为<b>医师</b>，可结合您的专业知识使用此功能，结果由AI推断，仅供参考。
                </div>
                <div style="padding-bottom: 0.3rem;" v-else>
                  <el-icon><Star /></el-icon>
                  您的身份为<b>{{ md_userTypeText }}</b>，建议您在专业医师的指导下使用该功能。其结果由AI推断，仅供参考。
                </div>
              </div>
            </el-card>
            <br>
          </div>
          <div style="flex: 1;display: flex;" v-loading="md_analyzing" element-loading-text="正在分析，请稍候" element-loading-background="rgba(0, 0, 0, 0.75)">
            <div style="width: 100%;height: 100%;">
              <el-card style="max-height: 100%;height: 100%;">
                <div style="color: darkblue; font-weight: bold; display: flex; align-items: center;">
                  <el-icon><Document /></el-icon><span>待分析的诊断内容表</span>
                </div>
                <el-scrollbar height="calc(99vh - 21rem)">
                <el-table :data="text_table">
                  <el-table-column type="index" label="序号" width="60%"/>
                  <el-table-column prop="text" label="待分析的诊断内容" />
                  <el-table-column prop="operation" label="操作" width="75%">
                    <template #default="scope">
                      <el-button link type="primary" size="small" @click.prevent="deleteRow(scope.$index)">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                </el-scrollbar>
              </el-card>
            </div>
            <div style="width: 100%; background-color: rgb(200,200,200); padding: 1rem; margin-left: 1rem; border-radius: 10px;">
            <div style="color: darkblue; font-weight: bold; display: flex; align-items: center;">
              <el-icon><Setting /></el-icon><span>待分析诊断内容设置</span>
            </div>
            <div style="margin-left: 1rem;">
              <div style="font-family: HPHS;margin: 0.5rem;">
                添加待分析的诊断内容
              </div>
              <div style="width: 100%;">
                <el-input v-model="md_input" placeholder="请您输入" style="width: 60%;" />&nbsp;
                <el-button type="primary" @click="addRow()">添加</el-button>
              </div>
            </div>
            <div style="margin-left: 1rem;">
              <div style="font-family: HPHS;margin: 0.5rem;">
                语言类型：
                <el-radio-group v-model="md_text_language">
                  <el-radio value="zh">中文</el-radio>
                  <el-radio value="en">英文</el-radio>
                </el-radio-group>
              </div>
            </div>
            <div style="display: flex;">
            <div style="margin-left: 1rem;">
              <div style="font-family: HPHS;margin: 0.5rem;">
                请选择图片
              </div>
              <div style="width: 100%;">
                <input type="file" class="file-input" id="imgSelect" @change="handleFileChange()" ref="md_imgShow" aria-label="Upload" accept=".jpg,.jpeg,.png,.webp,.bmp,.gif,.ico">
                <div style="margin-top: 2rem;text-align: center;">
                  <div style="width: 100%;" class="colorful-div">
                    <el-button type="primary" size="large" @click="getResult()" style="width: 100%;">
                      <el-icon><Promotion /></el-icon>&nbsp;
                      <b>一键分析</b>
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
            <div style="margin-left: 3rem; display: flex; align-items: center;">
              <el-image :src="md_el_avatar_01_src" id="md-el-avatar-01" ref="md_el_avatar_01" style="border-radius: 4px; max-height: 8.5rem; max-width: 8.5rem; background-size: cover; box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);object-fit: cover;" :preview-src-list="[md_el_avatar_01_src]"/><br>
            </div>
            </div>
            </div>
          </div>
          </div>
          
        </el-main>
        
      </el-container>
    </el-container>
    <el-dialog v-model="md_resultFormVisible" title="AI分析结果" style="min-width: 16rem;font-family: font02;font-size: large;" @open="showResult()">
      <div id="md_resultShowDiv" style="width: 100%;height: 46vh;"></div>
      <div style="font-size: large;font-family: HPHS;margin-top: 0.5rem;text-align: center;">
        <span>AI辅诊结论：</span><span>{{ md_conclusion }}</span>
      </div>
      <div style="margin-top: 0.5rem;">
        <el-button type="primary" @click="this.md_resultTableFormVisible=true">查看详细信息</el-button>
      </div>
    </el-dialog>
    <el-dialog v-model="md_resultTableFormVisible" title="详细分析结果" style="min-width: 16rem;font-family: font02;font-size: large;">
      <el-scrollbar height="52vh">
        <el-table :data="md_showDataTable">
          <el-table-column type="index" label="序号" width="60%"/>
          <el-table-column prop="english_text" label="英文" />
          <el-table-column prop="rate" label="概率值" width="100%"/> 
        </el-table>
      </el-scrollbar>
    </el-dialog>
  </div>
</template>
<style scoped>
@font-face 
{
  font-family: font01;
  src: url("/fonts/font01.woff");
}
@font-face {
  font-family: HPHS;
  src: url("/fonts/HPHS.woff");
}
@font-face
{
  font-family: ubuntu;
  src:url("/fonts/ubuntu.woff2");
}
@font-face {
  font-family: xinwei;
  src: url("/fonts/xinwei.woff");
}
#MultimodalDiagnosis-elHeader
{
  height: 5rem;
  color: white;
  background-image:linear-gradient(to right, rgb(0, 135, 255), rgb(0, 0, 108));
  box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
  border-radius: 0 0 10px 10px;
}
#MultimodalDiagnosis-elHeader-title01
{
  font-family: xinwei ,serif;
  padding-top: 0.75rem;
  padding-left: 1.5rem;
  font-size: 2.7rem;
  display: flex;
}
#MultimodalDiagnosis-elHeader-title02
{
  font-family: HPHS,serif;
  font-size: 1.3rem;
  padding-top: 0.3rem;
  padding-left: 1.35rem;
  font-style: italic;
  color: rgb(180, 255, 255);
  text-shadow: 1px 1px black;
  flex-grow: 14;
}
#MultimodalDiagnosis-elHeader-title03
{
  flex-grow: 1;
  text-shadow: 2px 2px black;
  display: flex;
  align-items: center;
}
#MultimodalDiagnosis-elHeader-title04
{
  font-size: 0.9rem;
  font-family: ubuntu,serif;
  color: rgb(100, 255, 255);
  text-shadow: 1px 1px black;
}
#MultimodalDiagnosis-common-layout
{
  width:100%;
  height: 100%;
}
#MultimodalDiagnosis-Label01
{
  font-size: 0.8rem;
}
@media screen and (max-width:40rem)
{
  #MultimodalDiagnosis-elHeader
  {
    height: 5rem;
  }
  #MultimodalDiagnosis-elHeader-title01
  {
    padding-top: 0.4rem;
    font-size: 1.85rem;
    padding-left: 0;
    display: block;
  }
  #MultimodalDiagnosis-elHeader-title02
  {
    font-size: 1rem;
    padding-top: 0.2rem;
    text-align: center;
  }
  #MultimodalDiagnosis-elHeader-title03
  {
    text-align: center;
    display: block;
  }
  #MultimodalDiagnosis-elHeader-title04
  {
    display: none;
  }
}
</style>