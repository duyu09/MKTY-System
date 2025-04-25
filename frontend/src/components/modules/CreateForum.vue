<script>
import { errHandle, successHandle, msgHandle } from "@/utils/tools";
import { addForum } from "@/api/api";

export default
{
  name: "CreateForum",
  data()
  {
    return{
      userId:0,
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
          addForum(this.ForumName, parseInt(this.cf_forumType), parseInt(this.cf_forumPermission)).then(res=>{
            if(res.data.code==0){
              successHandle('创建论坛成功：你创建的论坛编号为'+res.data.forumId+"号，您可前往论坛概览版块查看。");
              setTimeout(()=>{this.$router.go(0);},1234);
            }
            else
            { errHandle('未能成功创建论坛：' + res.data.msg);return; }
          }).catch(res=>{
            errHandle('未能成功创建论坛：'+res);return;
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
      <el-form-item label="请注意：论坛名称与论坛权限，一旦创建成功则不可修改。"></el-form-item>
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