<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统重要事项清单页面Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年03月10日 -->
<!-- 修改日期：2025年03月11日 -->
<script>
import ListHeader from "./ListHeader.vue";
import { ChatDotRound, Opportunity, Clock, InfoFilled, Aim, Finished, Delete } from "@element-plus/icons-vue";
import { getCurrentTime } from "@/api/api";
import { convertTime, errHandle, successHandle } from "@/utils/tools";
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
      },
  data()
  {
    return{
      il_currentTime:0,
      il_userId:0,
      il_itemsArr:[
        { "listItemId": 0, "listItemContent": "测试语句", "listItemIsFinished": "未完成", "listItemIsFinished_number": 0, "listItemStartTime": "2025年03月14日 02:43:20", "listItemEndTime": "2025年03月14日 02:43:20", "listItemTimeStatus":"已到时间", "listItemTimeMode": "一次性事项", "listItemPriority": "紧急事项", "listItemTimeWeek": "周一", "listItemPriority_number": 1  },
      ],
      il_loading:false,
      il_timer01Id:0,
      il_addItemDialogVisible:false,
      il_priorityRadio_char:"0",
      il_listItemTimeMode_char:"0",
      il_weekRadio_char:"1",
      il_timeRange:"",
      il_listItemContent:"",
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
      updateCurrentTime(){
        getCurrentTime().then((res) => {
            this.il_currentTime = res.data.currentTime;
        });
        this.il_timer01Id = setInterval(() => {
          getCurrentTime().then((res) => {
            this.il_currentTime = res.data.currentTime;
        });
        }, 59000);
      }
  },
  beforeUnmount()
  {
      clearInterval(this.il_timer01Id);  // 清除掉切换背景图片的定时器。
  },
  mounted()
  {
    this.updateCurrentTime();
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
            我的目标数量：
            {{ il_itemsArr.length }}个目标有待完成。
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
                诊疗事项：
                <span style="font-weight: bolder;" @click="">
                  {{ item.listItemContent }}
                </span>
              </div>
              <div class="Aims-Class-Div17">
                <div style="display: flex;">
                  <div style="margin-right: 1rem;">
                    完成情况:【
                    <span v-if="item.listItemIsFinished_number==0" style="color: red;">{{ item.listItemIsFinished }}</span>
                    <span v-if="item.listItemIsFinished_number==1" style="color: green;">{{ item.listItemIsFinished }}</span>
                    】
                  </div>
                  <div style="margin-right: 1rem;">时间状态:【{{ item.listItemTimeStatus }}】</div>
                  <div style="margin-right: 1rem;">事项类型:【{{ item.listItemTimeMode }}】</div>
                  <div style="margin-right: 1rem;" v-if="item.listItemPriority_number==0">优先级:【{{ item.listItemPriority }}】</div>
                  <div style="margin-right: 1rem; font-weight: bold; color: red;" v-if="item.listItemPriority_number==1">优先级:【{{ item.listItemPriority }}】</div>
                  <div style="margin-right: 1rem;">{{ item.listItemStartTime }} ~ {{ item.listItemEndTime }}</div>
                </div>
                <span class="Aims-Class-Span03">
                  <span class="Aims-Class-Span04" @click=""><el-icon><Finished /></el-icon>&nbsp;标记完成</span>&nbsp;
                  <span class="Aims-Class-Span04" @click=""><el-icon><Delete /></el-icon>&nbsp;删除事项</span>&nbsp;
                </span>
                &nbsp;
              </div>
            </div>

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
      <el-button type="primary" @click="il_addItemDialogVisible=false">添加</el-button>
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