<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统创建论坛组件Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年04月24日 -->
<script>
import { errHandle, successHandle, msgHandle } from "@/utils/tools";
import { addForum, getCookie, getUserInfo } from "@/api/api";

export default
{
  name: "CreateForum",
  data()
  {
    return{
      cf_userId:parseInt(getCookie("userId")),
      ForumName:'',
      ForumAttr:'',
      ForumDesc:'',
      cf_forumType:"0",
      cf_forumPermission:"0",
    }
  },
  mounted()
  {

  },
  methods:
      {
        createF()
        {
          if(this.ForumName===''){ 
            msgHandle('请输入论坛名称。');
            return; 
          }
          getUserInfo(this.cf_userId).then(res=>{
            if(res.data.code!=0){ 
              errHandle('未能成功获取用户信息：' + res.data.msg);return;  
            }
            
            const userTypeNumber = res.data.userInfo.userType;
            var userType = null;
            switch (userTypeNumber) {
              case 0: userType = "患者"; break;
              case 1: userType = "医师"; break;
              case 2: userType = "其他"; break;
            }
            if(userType!="医师" && this.cf_forumPermission=="1"){
              errHandle('对不起，您不是医师，无法创建仅医师可参与的论坛。');return;
            }
            if(userType!="患者" && this.cf_forumPermission=="2"){
              errHandle('对不起，您不是患者，无法创建仅患者可参与的论坛。');return;
            }
            addForum(this.ForumName, parseInt(this.cf_forumType), parseInt(this.cf_forumPermission)).then(res=>{
              if(res.data.code==0){
                successHandle('创建论坛成功：你创建的论坛编号为'+res.data.forumId+"号，您可前往论坛概览版块查看。");
                setTimeout(()=>{this.$router.go(0);},1234);
              }
              else{ 
                errHandle('未能成功创建论坛：' + res.data.msg);return; 
              }
            }).catch(res=>{
              errHandle('未能成功创建论坛：'+res);return;
            });
          });
        },
      }
}
</script>

<template>
  <div id="CreateForum-MainDiv">
    <el-form
        label-position="top"
    >
      <div style="font-size: medium;padding: 0.8rem; margin-bottom: 0.5rem; border-radius: 9px; background-color: rgb(238,238,238);">
        请注意：论坛名称与论坛权限，一旦创建成功则不可修改。
      </div>
      <el-form-item label="论坛名称">
        <el-input v-model="ForumName" placeholder="例如：高血压预防探讨" />
      </el-form-item>
      <el-form-item label="论坛类型">
        <el-select v-model="cf_forumType" class="m-2" placeholder="限定论坛性质">
          <el-option label="医学知识论坛" value="0"></el-option>
          <el-option label="病情讨论区" value="1"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="论坛权限设定">
        <el-select v-model="cf_forumPermission" placeholder="限定论坛权限">
          <el-option label="不限人员类型" value="0"></el-option>
          <el-option label="仅医师可参与" value="1"></el-option>
          <el-option label="仅病患可参与" value="2"></el-option>
    </el-select>
      </el-form-item>
    </el-form>
    <el-button type="success" @click="createF()">创建论坛</el-button>
  </div>
</template>

<style scoped>
#CreateForum-MainDiv
{
  width:65%;
}
@media screen and (max-width: 40rem)
{
  #CreateForum-MainDiv
  {
    width:87.5%;
  }
}
</style>
