<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统重要事项清单页面Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年03月10日 -->
<!-- 修改日期：2025年03月11日 -->
<script>
import ListHeader from "./ListHeader.vue";
import { ChatDotRound, Opportunity, Clock, InfoFilled, Aim, Finished, Delete, Flag } from "@element-plus/icons-vue";
import { getCurrentTime, getImportantList, addImportantItem } from "@/api/api";
import { convertTime, errHandle, successHandle, convertTimeChinese } from "@/utils/tools";
import "@/assets/css/colorful_div.css";

export default
{
  name: "ImportantList",
  components:
      {
        "ListHeader":ListHeader,
        "ChatDotRound":ChatDotRound,
        "Clock":Clock,
        "InfoFilled":InfoFilled,
        "Aim":Aim,
        "Opportunity":Opportunity,
        "Finished":Finished,
        "Delete":Delete,
        "Flag": Flag,
      },
  data()
  {
    return{
      il_currentTime:0,
      il_userId:0,
      il_itemsArr:[],
      il_loading:false,
      il_timer01Id:0,
      il_addItemDialogVisible:false,
      il_priorityRadio_char:"0",
      il_listItemTimeMode_char:"0",
      il_weekRadio_char:"1",
      il_timeRange:"",
      il_listItemContent:"",
      il_itemDialogVisible:false,
      il_itemDialogId:0,  // 事项id
      il_itemDialogContent:"",  // 事项内容
      il_itemDialogTimeMode:"",  // 事项类型（“一次性事项”、“周期性事项”）
      il_itemDialogStartTime:"", // 开始时间（例：“2025年3月15日 01:07:42”）
      il_itemDialogEndTime:"",  // 结束时间 （例：“2025年3月15日 01:07:42”）
      il_itemDialogPriority:"",  // 优先级（“一般事项”、“紧急事项”）
      il_itemDialogWeek:"", // 周（“星期一”）
      il_itemIsFinished:"", // 完成情况（“已完成”、“未完成”）
      il_itemTimeStatus:""  // 时间状态（“已到时间”、“未到时间”、“已超时”）
    }
  },
  computed:
  {
    il_priorityRadio(){
      return parseInt(this.il_priorityRadio_char);
    },
    il_listItemTimeMode(){
      return parseInt(this.il_listItemTimeMode_char);
    },
    il_weekRadio(){
      return parseInt(this.il_weekRadio_char);
    },
  },
  methods:
  {   
    getDayOfWeek(unixTimestamp) {
        // 将 Unix 时间戳转换为毫秒
        const date = new Date(unixTimestamp * 1000);
    
        // 获取星期几 (0 表示星期日，1 表示星期一，..., 6 表示星期六)
        const dayOfWeek = date.getDay();
    
        // 将星期日 (0) 转换为 7，其他保持不变
        return dayOfWeek === 0 ? 7 : dayOfWeek;
      },
      updateCurrentTime(){
        getCurrentTime().then((res) => {
            this.il_currentTime = res.data.currentTime;
        });
        this.il_timer01Id = setInterval(() => {
          getCurrentTime().then((res) => {
            this.il_currentTime = res.data.currentTime;
        });
        }, 59000);
      },
      changeItemDialogContent(il_itemDialogId, il_itemDialogContent, il_itemDialogTimeMode, il_itemDialogStartTime, il_itemDialogEndTime, il_itemDialogPriority, il_itemDialogWeek, il_itemIsFinished, il_itemTimeStatus){
        this.il_itemDialogId = il_itemDialogId;
        this.il_itemDialogContent = il_itemDialogContent;
        this.il_itemDialogTimeMode = il_itemDialogTimeMode;
        this.il_itemDialogStartTime = il_itemDialogStartTime;
        this.il_itemDialogEndTime = il_itemDialogEndTime;
        this.il_itemDialogPriority = il_itemDialogPriority;
        this.il_itemDialogWeek = il_itemDialogWeek;
        this.il_itemIsFinished = il_itemIsFinished;
        this.il_itemTimeStatus = il_itemTimeStatus;
        this.il_itemDialogVisible = true;
      },
      il_pageload()
      {
        getImportantList().then((res) => {
          if (res.data.code == 0) {
            const il_itemsArr = res.data.importantList;
            il_itemsArr.forEach((item) => {
              var final_item = {};
              final_item.listItemId = item.listItemId;
              final_item.listItemContent = item.listItemContent;
              final_item.listItemIsFinished_number = item.listItemIsFinished;
              final_item.listItemIsFinished = item.listItemIsFinished == 1 ? "已完成" : "未完成";
              final_item.listItemStartTime = convertTimeChinese(item.listItemStartTime * 1000);
              final_item.listItemEndTime = convertTimeChinese(item.listItemEndTime * 1000);
              if (item.listItemTimeMode == 0){
                final_item.listItemTimeMode = "一次性事项";
              }
              else if (item.listItemTimeMode == 1){
                final_item.listItemTimeMode = "周期性事项";
                final_item.listItemStartTime = "-";
                final_item.listItemEndTime = "-";
              }
              else if (item.listItemTimeMode == 2){
                final_item.listItemTimeMode = "无时间要求"; 
              }
              final_item.listItemTimeMode_number = item.listItemTimeMode;
              final_item.listItemPriority = item.listItemPriority == 0 ? "一般事项" : "紧急事项";
              final_item.listItemPriority_number = item.listItemPriority;
              if (item.listItemTimeWeek == 1){
                final_item.listItemTimeWeek = "周一";
              }
              else if (item.listItemTimeWeek == 2){
                final_item.listItemTimeWeek = "周二";
              }
              else if (item.listItemTimeWeek == 3){
                final_item.listItemTimeWeek = "周三";
              }
              else if (item.listItemTimeWeek == 4){
                final_item.listItemTimeWeek = "周四";
              }
              else if (item.listItemTimeWeek == 5){
                final_item.listItemTimeWeek = "周五";
              }
              else if (item.listItemTimeWeek == 6){
                final_item.listItemTimeWeek = "周六";
              }
              else if (item.listItemTimeWeek == 7){
                final_item.listItemTimeWeek = "周日"; 
              }
              else{
                final_item.listItemTimeWeek = "-"; 
              }
              if (item.listItemTimeMode == 0)
              {
                if (item.listItemStartTime > this.il_currentTime){
                  final_item.listItemTimeStatus = "未到时间";
                }
                else if (item.listItemStartTime <= this.il_currentTime && item.listItemEndTime > this.il_currentTime){
                  final_item.listItemTimeStatus = "已到时间";
                }
                else if (item.listItemEndTime <= this.il_currentTime){
                  final_item.listItemTimeStatus = "已超时"; 
                }
              }
              else if (item.listItemTimeMode == 1)
              {
                const currentWeek = this.getDayOfWeek(this.il_currentTime);
                if (item.listItemTimeWeek == currentWeek){
                  final_item.listItemTimeStatus = "已到时间";
                }
                else{
                  final_item.listItemTimeStatus = "未到时间";
                }
              }

              this.il_itemsArr.push(final_item);
            })
            
          } 
        })
      },
      il_addItem()
      {
        // addImportantItem
        const itemDialogContent = this.il_listItemContent;
        const itemDialogTimeMode = this.il_listItemTimeMode;
        var itemDialogStartTime = 0;
        var itemDialogEndTime = 0;
        const itemDialogPriority = this.il_priorityRadio;
        var itemDialogWeek = 1;
        if(itemDialogTimeMode == 0){
          itemDialogStartTime = Math.floor(this.il_timeRange[0].getTime() / 1000);
          itemDialogEndTime = Math.floor(this.il_timeRange[1].getTime() / 1000);
        }
        else if(itemDialogTimeMode == 1){
          itemDialogWeek = this.il_weekRadio;
        }
        addImportantItem(itemDialogContent, itemDialogTimeMode, itemDialogWeek, itemDialogStartTime, itemDialogEndTime, itemDialogPriority, 0).then((res) => {
          if (res.data.code == 0) {
            successHandle("添加成功！");
            this.il_addItemDialogVisible = false;
            this.il_itemsArr = [];
            this.il_pageload();
          } 
        })

      }
  },
  beforeUnmount()
  {
      clearInterval(this.il_timer01Id);  // 清除掉切换背景图片的定时器。
  },
  mounted()
  {
    this.updateCurrentTime();
    this.il_pageload();
  }
}
</script>

<template>
  <div id="Aims-MainDiv">
    <div id="Aims-HeaderDiv">
      <ListHeader></ListHeader>
    </div>
    <div id="Aims-Div01">
      <div id="Aims-Div02">
        <div id="Aims-Div05">
          <div id="Aims-Div07">
          <span id="Aims-Span01">
            <el-icon><InfoFilled /></el-icon>
            诊疗事项数量：
            共计{{ il_itemsArr.length }}个事项。
          </span>
            <span id="Aims-Span02">
<!--            {{ Aims_Attrib }}-->
<!--            这里可能要写已完成目标数量-->
          </span>
          </div>
        </div>

      </div>
      <div id="Aims-Div03">
        <div id="Aims-ItemsDiv" v-loading="il_loading" element-loading-text="加载中..." element-loading-background="rgba(0, 0, 0, 0.2)">
          <div id="Aims-Div10">

            <div class="Aims-Class-Div11" v-for="item in il_itemsArr">
              <div class="Aims-Class-Div16">
                <!-- 列表排序方式：最高优先级 > 一次性事项已到时间未完成 > 一次性事项已超时未完成 > 周期性事项未完成 > 周期性事项已完成  > 一次性事项未开始未完成 > 一次性事项已完成 -->
                <span style="font-weight: bolder;" @click="changeItemDialogContent(item.listItemId, item.listItemContent, item.listItemTimeMode, item.listItemStartTime, item.listItemEndTime, item.listItemPriority, item.listItemTimeWeek, item.listItemIsFinished, item.listItemTimeStatus)">
                <el-icon><Flag /></el-icon>诊疗事项： {{ item.listItemContent }}
                </span>
              </div>
              <div class="Aims-Class-Div17">
                <div style="display: flex;">
                  <div class="Medical-ItemDiv">
                    完成情况:<br>【<span v-if="item.listItemIsFinished_number==0" style="color: red;">{{ item.listItemIsFinished }}</span>
                    <span v-if="item.listItemIsFinished_number==1" style="color: green;">{{ item.listItemIsFinished }}</span>】
                  </div>
                  <div class="Medical-ItemDiv">时间状态:<br>【{{ item.listItemTimeStatus }}】</div>
                  <div class="Medical-ItemDiv">事项类型:<br>【{{ item.listItemTimeMode }}】</div>
                  <div class="Medical-ItemDiv" v-if="item.listItemPriority_number==0">优先级:<br>【{{ item.listItemPriority }}】</div>
                  <div class="Medical-ItemDiv" style="font-weight: bold; color: red;" v-if="item.listItemPriority_number==1">优先级:<br>【{{ item.listItemPriority }}】</div>
                  <div class="Medical-ItemDiv" v-if="item.listItemTimeMode_number == 0">{{ item.listItemStartTime }} ~ {{ item.listItemEndTime }}</div>
                  <div class="Medical-ItemDiv" v-else-if="item.listItemTimeMode_number == 1">时间：每周<b>{{ item.listItemTimeWeek }}</b></div>
                </div>
                <span class="Aims-Class-Span03">
                  <span class="Aims-Class-Span04" @click=""><el-icon><Finished /></el-icon>&nbsp;标记完成</span>&nbsp;
                  <span class="Aims-Class-Span04" @click=""><el-icon><Delete /></el-icon>&nbsp;删除事项</span>&nbsp;
                </span>
                &nbsp;
              </div>
            </div>
            <el-dialog title="事项内容详细表" v-model="il_itemDialogVisible" width="60%">
              <div>
                <b>诊疗事项ID：</b>{{ il_itemDialogId }}
              </div>
              <div style="margin-top: 1rem;">
                <b>诊疗事项内容：</b>{{ il_itemDialogContent }}
              </div>
              <div style="margin-top: 1rem;">
                <b>诊疗事项类型：</b>{{ il_itemDialogTimeMode }}
              </div>
              <div style="margin-top: 1rem;">
                <b>诊疗事项开始时间：</b>{{ il_itemDialogStartTime }}
              </div>
              <div style="margin-top: 1rem;">
                <b>诊疗事项结束时间：</b>{{ il_itemDialogEndTime }}
              </div>
              <div style="margin-top: 1rem;">
                <b>诊疗事项优先级：</b>{{ il_itemDialogPriority }}
              </div>
              <div style="margin-top: 1rem;">
                <b>诊疗事项周：</b>{{ il_itemDialogWeek }}
              </div>
              <div style="margin-top: 1rem;">
                <b>诊疗事项完成情况：</b>{{ il_itemIsFinished }}
              </div>
              <div style="margin-top: 1rem;">
                <b>诊疗事项时间状态：</b>{{ il_itemTimeStatus }}
              </div>
              <div style="margin-top: 1rem; display: flex; justify-content: flex-end;">
                <el-button @click="il_itemDialogVisible = false" type="primary">关闭</el-button>
              </div>
            </el-dialog>

          </div>
        </div>
      </div>
      <div id="Aims-Div18">
        <div id="Aims-Div19">
          <div id="Aims-Div20">
            <div id="PsyChat-Div06">
              <div id="PsyChat-Div07" style="margin-right: 1rem;">
                <div id="PsyChat-SendButtonDiv" @click="il_addItemDialogVisible=true;">
                  <el-icon><Aim /></el-icon>&nbsp;<span class="PsyChat-Span02">添加事项</span>
                </div>
              </div>
              <div id="PsyChat-Div07" class="colorful-div-common">
                <div id="PsyChat-SendButtonDiv" @click="">
                  <el-icon><Opportunity /></el-icon>&nbsp;<span class="PsyChat-Span02">AI辅助分析</span>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>


    </div>
  </div>

  <el-drawer title="添加诊疗事项" v-model="il_addItemDialogVisible" width="60%">
    <el-form>
      <el-form-item label="事项内容">
        <el-input placeholder="请输入事项内容" v-model="il_listItemContent"></el-input>
      </el-form-item>
      <el-divider></el-divider>
      <el-form-item label="事项类型">
        <el-radio-group v-model="il_listItemTimeMode_char">
          <el-radio value="0" size="large">一次性事项</el-radio>
          <el-radio value="1" size="large">周期性事项</el-radio>
          <el-radio value="2" size="large">无时间要求</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="设定时间">
        <el-date-picker type="datetimerange" start-placeholder="选择开始时间" end-placeholder="选择结束时间" :disabled="il_listItemTimeMode!=0" v-model="il_timeRange"></el-date-picker>
      </el-form-item>
      <el-form-item label="设定星期">
        <el-select v-model="il_weekRadio_char" placeholder="Select" :disabled="il_listItemTimeMode!=1">
          <el-option label="周一" value="1"></el-option>
          <el-option label="周二" value="2"></el-option>
          <el-option label="周三" value="3"></el-option>
          <el-option label="周四" value="4"></el-option>
          <el-option label="周五" value="5"></el-option>
          <el-option label="周六" value="6"></el-option>
          <el-option label="周日" value="7"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="设定优先级">
        <el-radio-group v-model="il_priorityRadio_char">
          <el-radio value="0" size="large">一般优先级</el-radio>
          <el-radio value="1" size="large"><span style="color: brown;">非常紧急/重要</span></el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
    <span style="display: flex;justify-content: center;">
      <el-button @click="il_addItemDialogVisible=false">取消</el-button>
      <el-button type="primary" @click="il_addItem();il_addItemDialogVisible=false">添加</el-button>
    </span>
  </el-drawer>
  
</template>
<style scoped>
@font-face
{
  font-family: HPHS;
  src: url("../../assets/fonts/HPHS.woff");
}
#Aims-HeaderDiv
{
  width: 100%;
}
#Aims-MainDiv
{
  width: 100%;
  display: flex;
  flex-direction: column;
}
#Aims-Div01
{
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  position: relative;
}
#Aims-Div02
{
  font-family: HPHS, serif;
  height: 2rem;
  box-shadow: 0 0 0.8rem 0.25rem rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
}
#Aims-Div03
{
  display: flex;
  justify-content: center;
  height: calc(99.85vh - 9rem);
}
#Aims-Div04
{
  display: flex;
  align-items: center;
  height: 100%;
  margin-left: 1.75rem;
  font-size: 1.25rem;
}
#Aims-Div05
{
  height: 100%;
  margin-left: 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
#Aims-Div06
{
  font-size: 1.25rem;
}
#Aims-Div07
{
  font-size: 1rem;
  margin-top: 0.35rem;
  display: flex;
  align-items: center;
}
#Aims-Div08
{
  flex-grow: 1;
  text-align: right;
  margin-right: 2rem;
}
#Aims-Div09
{

}
#Aims-Div10
{
  display: flex;
  align-items:center;
  flex-direction: column;
}
.Aims-Class-Div11
{
  box-shadow: 0 5px 5px -5px #888888;
  width: 92.5%;
  min-height: 4.5rem;
}
.Aims-Class-Div11:hover
{
  background-color: rgba(240,240,240,1);
}
.Aims-Class-Div12
{
  display: flex;
  margin-top: 0.75rem;
}
.Aims-Class-Div13
{
  background-color: #3d93ff;
  height: 2.75rem;
  width: 2.75rem;
  border-radius: 2rem;
}
.Aims-Class-Div14
{
  margin-left: 1rem;
}
.Aims-Class-Div15
{
  color: #555555;
  font-size: 0.85rem;
  margin-top: 0.1rem;
}
.Aims-Class-Div16
{
  margin-left: 0.25rem;
  margin-top: 0.75rem;
  cursor: pointer;
}
.Aims-Class-Div16:hover
{
  /*font-weight: bolder;*/
  color: darkblue;
}
.Aims-Class-Div17
{
  margin-left: 0.25rem;
  margin-top: 0.5rem;
  font-size: 0.75rem;
}
#Aims-Div18
{
  display: flex;
  justify-content: center;
  position: absolute;
  bottom: 1.5rem;
  width:100%;
}
#Aims-Div19
{
  width: 90%;
}
#Aims-Div20
{

}
#Aims-Span01
{
  display: flex;
  align-items: center;
}
#Aims-Span02
{
  display: flex;
  align-items: center;
  margin-left: 1rem;
}
.Aims-Class-Span02
{
  font-weight: bolder;
  font-size: 1rem;
}
.Aims-Class-Span03
{
  left:90%;
  position: sticky;
  cursor: pointer;
}
.Aims-Class-Span04
{
  cursor: pointer;
  color:darkblue;
}
.Aims-Class-Span04:hover
{
  color: darkblue;
  font-weight: bolder;
}
#Aims-ItemsDiv
{
  background-color:white;
  width: 90%;
  margin-top: 1.25rem;
  border-radius: 20px 20px 0 0;
  overflow: auto;
}
.Medical-ItemDiv
{
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  border-left: double 3px #000;

  
}
#PsyChat-Div06
{
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}
#PsyChat-Div07
{
  box-shadow: 0 0 0.8rem 0.075rem rgba(0,0,0,0.5);
  background-color: rgba(255,255,255,0.8);
  width:7.5rem;
  height: 2.5rem;
  border-radius: 15px;
  padding: 0.15rem 0.05rem;
  display: flex;
  margin-top: 1rem;
  justify-content: center;
}
#Aims-Image01
{
  border-radius: 4px;
  height: 3rem;
  width: 3rem;
  background-size: cover;
  box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
}
.Aims-Class-Image02
{
  height: 100%;
  width:100%;
  border-radius: 10rem;
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
  background-color: rgb(255, 237, 204);
  box-shadow: 0 0 0.35rem 0.05rem rgba(0,0,0,0.4);
  width: 95%;
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
  background-color: rgb(255, 225, 170);
}
#PsyChat-SendButtonDiv:active
{
  background-color: rgb(255, 225, 130);
}
.PsyChat-Span02
{
  cursor: pointer;
}
#Aims-ItemsDiv::-webkit-scrollbar
{
  display: none;
}

@media screen and (max-width: 40rem)
{
  #Aims-Div09
  {
    display: none;
  }

  #PsyChat-SendButtonDiv {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 0;
  }

  #PsyChat-Div07 {
    margin-bottom: 2rem;
  }
}
</style>