<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统“MKTY大模型讨论机制”页面Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年03月10日 -->
<!-- 修改日期：2025年04月06日 -->
<script>
import { Promotion, Avatar, Delete, ChatDotSquare, Setting, CaretRight, Loading, Clock, Notebook } from '@element-plus/icons-vue';
import { marked }  from "marked";
import DOMPurify from "dompurify";
import 'highlight.js/styles/rainbow.css';
import hljs from 'highlight.js';
import { errHandle, successHandle, convertTime } from "@/utils/tools";
import { getCookie, getUserAvatar, llmInferenceGetStatus, llmInferenceSubmitTask, saveLlmSession, 
  getLlmSessionList, getLlmSession, deleteLlmSession, tsbbModelSubmitTask, tsbbInferenceGetStatus } from "@/api/api";


export default
{
    name:'PsyChatDM',
    components:
    {
      'Promotion': Promotion,
      'Avatar': Avatar,
      'Delete': Delete,
      'ChatDotSquare': ChatDotSquare,
      'Setting': Setting,
      'CaretRight': CaretRight,
      'Loading': Loading,
      'Clock': Clock,
      'Notebook': Notebook
    },
    data()
    {
      return {
        PsyChat_userAvatar: '',
        PsyChat_Context: '',
        PsyChat_HistoryDialog: false, // 历史对话会话框是否显示。
        PsyChat_Generating: false, // 页面状态，回答是否在生成中。
        PsyChat_SessionId: -1, // 会话ID号。默认是-1（新会话为-1）。

        PsyChat_LlmSessionList:[],
        PsyChat_LlmSessionListLoading: false, // 历史对话会话框加载中。
        PsyChatDM_StepList:[  // 讨论步骤列表。
          // { "title":"第1轮", "desc": "智能体A讨论" }, 
          // { "title":"第1轮", "desc": "智能体B讨论"}, 
          // { "title":"第1轮", "desc": "主持人总结"}, 
          // { "title":"第2轮", "desc": "智能体A讨论"}, 
          // { "title":"第2轮", "desc": "智能体B讨论"}, 
          // { "title":"第2轮", "desc": "主持人总结"}, 
          // { "title":"第3轮", "desc": "智能体A讨论"}, 
          // { "title":"第3轮", "desc": "智能体B讨论"},
          // { "title":"第3轮", "desc": "主持人总结"},
          // { "title":"判敛", "desc": "计算共识度"},
        ], 
        PsyChatDM_StepResultList:[
          // { "title":"第1轮 智能体1讨论", "content": "具体讨论内容......" },
        ], // 讨论步骤结果列表。
        PsyChatDM_CurrentStep: 0, // 当前讨论步骤。
        PsyChatDM_Context_AgentN:[[], [], [], []],
        PsyChatDM_HyperParametersAdjustmentDialog: false, // 超参数调整对话框是否显示。
        PsyChatDM_HyperParameters_AgentNumber: 3, // 参与讨论智能体数量。
        PsyChatDM_HyperParameters_Epoch: 3, // 讨论回合数。
        PsyChatDM_HyperParameters_ConvergenceThreshold: 0.80, // 收敛阈值。
      }
    },
    computed:
    {
      PsyChatContextDisplay(){
        if(this.PsyChat_Context===''){
          return '用户暂未输入';
        }
        else {
          return this.PsyChat_Context; 
        }
      }
    },
    methods:
      {
        async PsyChat_Send(){
          this.pc_clear();
          if(this.PsyChat_Context === ''){
           errHandle('待探讨问题不可为空'); 
           return;
          }
          this.PsyChat_Generating=true; // 开始生成
          this.PsyChatDM_Context_AgentN=[[], [], [], []]; // 清空上下文。
          this.PsyChatDM_StepList=[]; // 清空步骤列表。
          this.PsyChatDM_CurrentStep=0; // 重置当前步骤。
          for(let i=0;i<this.PsyChatDM_HyperParameters_Epoch;i++){
            for(let j=0;j<this.PsyChatDM_HyperParameters_AgentNumber;j++){
              this.PsyChatDM_StepList.push({ "title":"第"+(i+1)+"轮", "desc": "智能体"+(j+1)+"讨论"});
            }
            this.PsyChatDM_StepList.push({ "title":"第"+(i+1)+"轮", "desc": "主持人总结"});
          }
          this.PsyChatDM_StepList.push({ "title":"判敛", "desc": "计算共识度"});
          // 开始讨论
          var moderator_opinion = "暂无"  // 上轮主持人意见
          for(let i=0;i<this.PsyChatDM_HyperParameters_Epoch;i++){ // 讨论轮次
            var result_summary = "";
            for(let j=0;j<this.PsyChatDM_HyperParameters_AgentNumber;j++){ // 智能体
              var prompt_per_round = "- 问题：\n" + this.PsyChat_Context + "\n\n - 上轮讨论主持人意见：\n" + moderator_opinion + "\n\n - 请你结合主持人意见，对上述医疗或医学专业的问题发表详细观点，可以质疑并说明理由。\n";
              const result=await this.PsyChatDM_LlmInference(this.PsyChatDM_Context_AgentN[j], this.PsyChat_Context);
              if(!result){
                errHandle('智能体' + (j + 1) + '生成出现错误，系统暂停讨论。');
                this.PsyChat_Generating=false;
                return;
              }
              this.PsyChatDM_Context_AgentN[j].push({ "role": "user", "content": prompt_per_round }); // 加入用户问题。
              this.PsyChatDM_Context_AgentN[j].push({ "role": "assistant", "content": result }); // 加入智能体回答。
              const result_html = DOMPurify.sanitize(marked(result));
              this.PsyChatDM_StepResultList.push({ "title":"第" + (i + 1) + "轮 智能体" + (j + 1) + "讨论", "content": result_html }); // 加入讨论步骤结果。
              result_summary += "- LLM " + (j + 1) + "观点：\n" + result + "\n\n"; // 加入总结。
              this.PsyChatDM_CurrentStep++; // 增加当前步骤。
            }
            var moderator_prompt = "- 问题：\n" + this.PsyChat_Context + "\n\n" + result_summary + "对于给定的医疗相关问题，请综合各LLM观点，结合自身知识，得出你自己的判断，尽可能详尽，全部都分析到位，还要充分说明理由。\n";
            const moderator_result=await this.PsyChatDM_LlmInference([], moderator_prompt); // 主持人
            if(!moderator_result){
              errHandle('主持人智能体生成出现错误，系统暂停讨论。');
              this.PsyChat_Generating=false;
              return;
            }
            this.PsyChatDM_CurrentStep++; // 增加当前步骤。
            moderator_opinion = moderator_result; // 保存主持人意见。
            this.PsyChatDM_StepResultList.push({ "title":"第"+(i+1)+"轮 主持人总结", "content": moderator_opinion }); // 加入讨论步骤结果。
          }
          // 判敛
          // 任务类型=1；任务语言=“zh”
          var s001 = this.PsyChatDM_StepResultList;
          s001 = s001.slice(-(this.PsyChatDM_HyperParameters_AgentNumber + 1));
          var textList = s001.map(item => item.content);
          //tsbbModelSubmitTask(1, "zh", textList);
          const convergence_score = await this.PsyChatDM_ttbsInference(textList, 2567);
          const convergence_score_percentage = (convergence_score * 100).toFixed(2) + '%';
          if(convergence_score < this.PsyChatDM_HyperParameters_ConvergenceThreshold) {
            this.PsyChatDM_StepResultList.push({ "title": "判敛结果：讨论不收敛（" + convergence_score_percentage + "）", "content": "智能体讨论结束，若干智能体未达成共识，最后一轮收敛指标：" + convergence_score + "（约为" + convergence_score_percentage + "）" + "，小于您设置的阈值。" });
          }
          else {
            this.PsyChatDM_StepResultList.push({ "title": "判敛结果：讨论收敛（" + convergence_score_percentage + "）", "content": "智能体讨论结束，若干智能体已达成共识，最后一轮收敛指标：" + convergence_score + "（约为" + convergence_score_percentage + "）" + "，不小于您设置的阈值。" });
          }
          this.PsyChatDM_CurrentStep++;
          var s002 = this.PsyChatDM_StepResultList.slice();
          s002.unshift(this.PsyChat_Context);
          saveLlmSession(-1, s002, 1).then((res3) => {
            if(res3.data.code!= 0) { 
              errHandle("未成功保存聊天记录：" + res3.data.msg); 
            }
            else {
              console.log("保存聊天记录成功。");
              // res3.data.sessionId; // 更新会话ID号。
            }
          });
          this.PsyChat_Generating=false;
          successHandle("智能体讨论已完成。");
        },
        async PsyChatDM_LlmInference(history_ChatArr, content, interval=2555){
          const submit_result = await llmInferenceSubmitTask(history_ChatArr, content); // 提交任务。
          if(submit_result.data.code!==0){
            errHandle('提交任务失败：'+submit_result.data.msg);
            return new Promise((resolve) => {
              resolve(false);
            });
          }
          const task_id = submit_result.data.taskId;
          return new Promise((resolve) => {
            const timer = setInterval(async () => {
              const result = await llmInferenceGetStatus(task_id);
              if(result.data.code !== 0) {
                errHandle('获取任务状态失败，暂停讨论：' + result.data.msg);
                clearInterval(timer);
                resolve(false);
              }
              if (result.data.taskStatus == 0) {
                clearInterval(timer);
                resolve(result.data.taskResult);
              }
            }, interval);
          });
        },
        async PsyChatDM_ttbsInference(textList, interval=2555)
        {
          const submit_result = await tsbbModelSubmitTask(1, "zh", textList); // 提交任务。
          if(submit_result.data.code!==0) {
            errHandle('提交任务失败：' + submit_result.data.msg);
            return new Promise((resolve) => {
              resolve(false);
            });
          }
          const task_id = submit_result.data.taskId;
          return new Promise((resolve) => {
            const timer = setInterval(async () => {
              const result = await tsbbInferenceGetStatus(task_id);
              if(result.data.code !== 0) {
                errHandle('获取任务状态失败，暂停讨论：' + result.data.msg);
                clearInterval(timer);
                resolve(false);
              }
              if (result.data.taskStatus == 0) {
                clearInterval(timer);
                resolve(result.data.taskResult);
              }
            }, interval);
          });
        },
        pc_loadPage(){
          const userId=parseInt(getCookie('userId'));
          if(userId!==undefined && userId!==0 && userId!==null){
            getUserAvatar(userId).then(res=>{
              if(res.data.code!==0){
                errHandle('授权错误，未能获取您的头像。');
                return;
              }
              else {
                this.PsyChat_userAvatar=res.data.userAvatar; 
              }
            }).catch(res=>{
              errHandle('未能获取您的头像：'+res);
            });
          }
        },
        pc_getLlmSessionList(){
          this.PsyChat_LlmSessionListLoading=true;
          this.PsyChat_LlmSessionList=[];
          getLlmSessionList(1).then(res=>{
            if(res.data.code!==0){
              errHandle('获取会话列表失败：'+res.data.msg);
              this.PsyChat_LlmSessionListLoading=false;
              return;
            }
            else {
              this.PsyChat_LlmSessionList=res.data.sessionList;
              this.PsyChat_LlmSessionListLoading=false;
              console.log("this.PsyChat_LlmSessionList", this.PsyChat_LlmSessionList);
            }
          })

        },
        pc_newSession(){
        },
        pc_conTime(unixTime){
          return convertTime(unixTime);
        },
        pc_loadSession(sessionId){
          getLlmSession(sessionId).then(res=>{
            if(res.data.code!==0){
              errHandle('获取会话记录失败：'+res.data.msg);
              return;
            }
            else {
              const arr = JSON.parse(res.data.sessionContent); // 加载聊天记录。
              this.PsyChat_Context = arr[0];
              this.PsyChatDM_StepResultList = arr.slice(1);
              setTimeout(() => this.$refs.ChatMainDiv.scrollTo({top:this.$refs.ChatMainDiv.scrollHeight,behavior:'smooth'}),350);
              this.PsyChat_HistoryDialog=false; // 关闭历史对话会话框。
              successHandle('已加载会话记录');
            }  
          });
        },
        pc_deleteSession(sessionId){
          deleteLlmSession(sessionId).then(res=>{
            if(res.data.code!==0){
              errHandle('删除会话记录失败：'+res.data.msg);
              return;
            }
            else {
              this.PsyChat_LlmSessionList=[]; // 清空会话列表。
              this.pc_getLlmSessionList(); // 重新加载会话列表。
              successHandle('已删除会话记录'); 
            }
          }) 
        },
        pc_clear()
        {
          this.PsyChat_Generating = false;
          this.PsyChat_SessionId = -1;
          this.PsyChatDM_StepList = [];
          this.PsyChatDM_StepResultList = [];
          this.PsyChatDM_CurrentStep = 0;
          this.PsyChatDM_Context_AgentN = [[], [], [], []];
        }
      },
  mounted()
  {
    this.pc_loadPage();
  }
}

</script>
<template>
   <div id="PsyChat-MainDiv">
      <el-container>
        <el-header id="PsyChat-elHeader">
          <nobr>明康慧医 智能体深度分析</nobr>
          <div id="PsyChat-Span01">
            <div><nobr>MKTY医疗大模型 智能体医师讨论机制</nobr></div>
            <div><span style="font-size: small;">AI Agent Physician Discussion Mechanism for Deep Analyzing Based on MKTY Medical LLM</span></div>
          </div>
        </el-header>
      </el-container>

      <div id="PsyChat-NewDiv01">
       <div id="PsyChat-NewDiv02">
         <div id="PsyChat-NewDiv03">
            <el-button type="primary" @click="pc_clear()" :disabled="PsyChat_Generating">清空会话</el-button>
            <el-button type="primary" @click="PsyChat_HistoryDialog=true" :disabled="PsyChat_Generating">会话记录</el-button>
            <!-- <el-button type="primary" @click="" :disabled="PsyChat_Generating">选择RAG知识库</el-button> -->
            <el-button type="warning" @click="this.$router.push('/main/PsyChat')" :disabled="PsyChat_Generating">智慧问答模式</el-button>
         </div>
         <div id="PsyChat-NewDiv04">
            <span id="PsyChat-NewSpan01">
             “明康慧医智能体深度分析”基于MKTY-3B-Chat大语言模型，该LLM发表的言论仅供参考，不具有绝对的真实性与可靠性。
           </span>
         </div>
       </div>
     </div>

      <div id="PsyChat-Div04" style="margin-top: 1rem;">
        <div id="PsyChat-Div05" ref="ChatMainDiv">
          <div style="margin-top: 1rem; margin-left: 1rem; justify-content: left;">
            <div style="background-color: rgb(230,230,230); padding: 0.5rem 0.5rem 0.5rem 0.8rem; border-radius: 18px; width: 95%;">
              <div style="display: flex;">
                <div style="align-items: center; display: flex; flex-direction: row;">
                  <b>
                    📒待研究问题：
                  </b>
                </div>
                <div style="margin-left: 0.5rem;">
                  {{ PsyChatContextDisplay }}
                </div>
              </div>
              <b>🤖Agent数量：</b>{{ PsyChatDM_HyperParameters_AgentNumber }}个&nbsp;
              <b>💭讨论回合数：</b>{{ PsyChatDM_HyperParameters_Epoch }}回合&nbsp;
              <b>🎚️收敛阈值：</b>{{ PsyChatDM_HyperParameters_ConvergenceThreshold }}&nbsp;
              <b>📺状态：</b>
              <span style="color: darkgreen; font-weight: bold;" v-if="this.PsyChat_Generating">
                <el-icon class="is-loading"><Loading /></el-icon>
                正在分析，请稍候...
              </span>
              <span style="color: brown; font-weight: bold;" v-else>
                空闲状态
              </span>
            </div>
          </div>

          <div style="margin-top: 1rem; margin-left: 1rem;">
          <el-steps
          style="width: 100%; font-family: HPHS; font-weight: bold;"
          :active="PsyChatDM_CurrentStep"
          finish-status="success"
          >
            <el-step v-for="(item, index) in PsyChatDM_StepList" :title="item.title" :description="item.desc" />
          </el-steps>
          </div>

          <div style="display: flex; justify-content: center; margin-top: 2rem;">
            <div style="width: 88%; background-color: rgb(230,230,230); padding: 1rem 1rem 1rem 1rem; border-radius: 18px;">
              <div style="margin-bottom: 0.25rem; font-weight: bold;">
                分析结果实时展示：
              </div>
              <div style="width: 100%; text-align: center;" v-if="PsyChatDM_StepResultList.length==0">
                <span style="font-weight: bold; color: brown;">---&nbsp;结果暂为空&nbsp;---</span>
              </div>
              <el-collapse style="font-family: HPHS;">
                <el-collapse-item :title="'&nbsp;&nbsp;'+item.title" :name="index+1" v-for="(item, index) in PsyChatDM_StepResultList">
                  <div style="margin-left: 1rem;" v-html="item.content"></div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
          <br>

        </div>
      </div>
      <div id="PsyChat-Div06">
        <div id="PsyChat-Div07" v-loading="PsyChat_Generating" element-loading-background="rgba(0, 0, 0, 0.75)">
          <input id="PsyChat-InputBox01" placeholder="请输入需要深度研究分析的医学问题" v-model="PsyChat_Context" @keyup.enter="PsyChat_Send()" />
          <div class="PsyChat-SendButtonDiv" @click="this.PsyChatDM_HyperParametersAdjustmentDialog=true;">
            <el-icon><Setting /></el-icon>&nbsp;<span class="PsyChat-Span02">设参数</span>
          </div>
          <div class="PsyChat-SendButtonDiv" @click="PsyChat_Send()">
            <el-icon><Promotion /></el-icon>&nbsp;<span class="PsyChat-Span02">提交</span>
          </div>
        </div>
      </div>


      <el-drawer v-model="PsyChat_HistoryDialog" title="会话历史" direction="ltr" @open="pc_getLlmSessionList()">
        <el-scrollbar height="100%" style="font-size: large;" v-loading="PsyChat_LlmSessionListLoading" element-loading-text="加载中..." element-loading-background="rgba(0, 0, 0, 0.2)">
          <div v-for="item in PsyChat_LlmSessionList" class="PsyChat-SessionListItem-BG-Div">
                <div class="PsyChat-SessionListItem" @click="pc_loadSession(item.sessionId)">
                  <el-icon><ChatDotSquare /></el-icon>
                  {{ item.sessionTitle }}
                </div>
                <div style="text-align: right;">
                  <span style="font-size: small;">
                    🕗{{ pc_conTime(item.sessionSaveTime * 1000) }}
                  </span>&nbsp;
                  <el-popconfirm title="您确定删除吗？" @confirm="pc_deleteSession(item.sessionId)" @cancel="">
                    <template #reference>
                      <span style="font-size: small; color: red; cursor: pointer; font-weight: bold;">
                      <el-icon size="small" color="red">
                        <Delete />
                      </el-icon>删除
                    </span>
                    </template>
                  </el-popconfirm>
                  &nbsp;&nbsp;
                </div>
                <el-divider style="margin: 10px;"></el-divider>           
              </div>
        </el-scrollbar>
      </el-drawer>

      <el-dialog title="MKTY大模型讨论机制 超参数设置面板" v-model="this.PsyChatDM_HyperParametersAdjustmentDialog">
        <div style="">
          <div>
            <div class="PsyChat-HP-Setting-items-label">
              <b><el-icon><CaretRight /></el-icon>智能体个数：</b>{{ PsyChatDM_HyperParameters_AgentNumber  }} 个
            </div>
            <div style="width: 70%; margin-left: 1.5rem;">
              <el-slider v-model="PsyChatDM_HyperParameters_AgentNumber" :step="1" show-stops :max="4" :min="1" :marks="{1:'1',2:'2',3:'3',4:'4'}" :show-tooltip="false" />
            </div>
          </div>
          <div style="padding-top: 1.5rem;">
            <div class="PsyChat-HP-Setting-items-label">
              <b><el-icon><CaretRight /></el-icon>讨论回合数：</b>{{ PsyChatDM_HyperParameters_Epoch }} 轮
            </div>
            <div style="width: 70%; margin-left: 1.5rem;">
              <el-slider v-model="PsyChatDM_HyperParameters_Epoch" :step="1" show-stops :max="4" :min="1" :marks="{1:'1',2:'2',3:'3',4:'4'}" :show-tooltip="false" />
            </div>
          </div>
          <div style="padding-top: 1.5rem;">
            <div class="PsyChat-HP-Setting-items-label">
              <b><el-icon><CaretRight /></el-icon>余弦相似度 判敛阈值：</b>{{ PsyChatDM_HyperParameters_ConvergenceThreshold.toFixed(2) }}
            </div>
            <div style="width: 70%; margin-left: 1.5rem; margin-bottom: 1.5rem;">
              <el-slider v-model="PsyChatDM_HyperParameters_ConvergenceThreshold" :step="0.01" :max="1.00" :min="0.20" :marks="{0.2:'0.20',0.4:'0.40',0.6:'0.60',0.8:'0.80',1:'1.00'}" :show-tooltip="false" />
            </div>
          </div>
          <div style="display: flex; justify-content: right;">
            <el-button type="primary" @click="this.PsyChatDM_HyperParametersAdjustmentDialog=false">确定</el-button>
          </div>
        </div>
      </el-dialog>

      
     
    </div>
</template>
<style scoped>
@font-face 
{
    font-family: xinwei;
    src: url('/fonts/xinwei.woff');
}
@font-face
{
  font-family: font01;
  src: url("/font01.woff2");
}
@font-face
{
  font-family: HPHS;
  src: url("/fonts/HPHS.woff");
}
.PsyChat-HP-Setting-items-label
{
  background-color: rgb(230,230,230); 
  padding: 0.5rem 0.5rem 0.5rem 0.8rem; 
  border-radius: 18px;
}
.PsyChat-SessionListItem
{
  margin: 0.75rem 0.25rem 0rem 0.25rem;
  cursor: pointer;
}
.PsyChat-SessionListItem:hover
{
  color: darkblue;
  font-weight: bold;
}
.PsyChat-SessionListItem-BG-Div
{
  width: 100%;
  text-align: left;
  border-radius: 10px;
}
.PsyChat-SessionListItem-BG-Div:hover
{
  transition: background-color 0.7s ease;
  background-color: rgba(0, 0, 0, 0.2);
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
  max-width: 40rem;
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
  display: flex;
}
#PsyChat-Span01
{
  font-size: 1.25rem;
  margin-left: 1.5rem;
  padding-bottom: 0.3rem;
  font-style: italic;
  color: #e5007f;
  text-shadow: 1px 0.5px darkred;
  font-family: HPHS;
}
.PsyChat-Span02
{
  font-weight: bold;
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
  /* text-align: center; */
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
  width:72%;
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
.PsyChat-SendButtonDiv
{
  background-color: rgba(255,165,0,0.2);
  box-shadow: 0 0 0.35rem 0.05rem rgba(0,0,0,0.4);
  width: 12%;
  margin-left: 1.5%;
  margin-top: auto;
  margin-bottom: auto;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80%;
}
.PsyChat-SendButtonDiv:hover
{
  background-color: rgba(255,165,0,0.333);
}
.PsyChat-SendButtonDiv:active
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