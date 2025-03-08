<script>
import Cookies from "js-cookie";
import {errHandle, successHandle} from "../../utils/tools";
import {creatForum} from "../../api/api";

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
      ForumOptions:[
        {"value":1,"label":"学术类论坛"},
        {"value":2,"label":"技术类论坛"},
        {"value":3,"label":"生活类论坛"},
        {"value":0,"label":"其他类论坛"},
      ],
      ForumClassify:0,
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
        createF()
        {
          creatForum(this.userId,this.ForumName,this.ForumClassify).then(res=>{
            if(res.data.code===0)
            {
              successHandle('创建论坛成功：你创建的论坛编号为'+res.data.id+"号，请前往论坛概览版块查看。");
              setTimeout(()=>{this.$router.go(0);},1234);
            }
            else
            { errHandle('未能成功创建论坛。可能是您的登录状态已过期。');return; }
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
      <el-form-item label="论坛名称">
        <el-input v-model="ForumName" placeholder="例如：齐工大生活圈" />
      </el-form-item>
      <el-form-item label="论坛性质">
        <el-select v-model="ForumClassify" class="m-2" placeholder="Select">
          <el-option
              v-for="item in ForumOptions"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
      </el-form-item>
<!--      <el-form-item label="论坛简述">-->
<!--        <el-input v-model="ForumDesc" placeholder="例如：齐工大生活圈是工大学子温馨的家，大家可以共同讨论学习生活的问题。" />-->
<!--      </el-form-item>-->
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