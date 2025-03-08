<script>
import Cookies from "js-cookie";
import {errHandle, successHandle} from "../../utils/tools";
import {createOrg} from "../../api/api";

export default
{
  name: "CreateOrg",
  data()
  {
    return{
      userId:0,
      OrgName:'',
      OrgDesc:'',
      OrgRecruitment:'',
      OrgClassify:0,
      OrgOptions:[
        {"value":1,"label":"技术与学术类"},
        {"value":2,"label":"创业类"},
        {"value":3,"label":"文娱兴趣类"},
        {"value":0,"label":"学生会"},
      ],
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
        createO()
        {
          if(this.OrgName===''||this.OrgDesc==='')
          {
            errHandle('组织名称和描述不可以不填哦！');
            return;
          }
          createOrg(this.userId,this.OrgClassify,this.OrgName,this.OrgDesc,this.OrgRecruitment).then(res=>{
            if(res.data.code===0) {
              successHandle('学生组织创建成功！');
              setTimeout(()=>{this.$router.go(0);},1234);
            }
            else {errHandle('未能成功创建组织');return;}
          }).catch(res=>{
            errHandle('未能成功创建组织:'+res);return;
          });

        }
      }
}
</script>

<template>
  <div id="CreateOrg-MainDiv">
    <el-form
        label-position="top"
    >
      <el-form-item label="学生组织名称">
        <el-input v-model="OrgName" placeholder="例如：开发者协会" />
      </el-form-item>
      <el-form-item label="组织简述">
        <el-input v-model="OrgDesc" placeholder="例如：开发者协会是齐工大软件开发技术大佬的聚集地！" />
      </el-form-item>
      <el-form-item label="纳新公告">
        <el-input v-model="OrgRecruitment" placeholder="例如：开发者协会纳新了！5月5日二教JT101不见不散！" />
      </el-form-item>
      <el-form-item label="社团组织分类">
        <el-select v-model="OrgClassify" class="m-2" placeholder="Select">
          <el-option
              v-for="item in OrgOptions"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <el-button type="success" @click="createO()">创建组织</el-button>
  </div>
</template>

<style scoped>
#CreateOrg-MainDiv
{
  width:65%;
}
</style>