<script>
import "../../../public/dsc.css"
import Cookies from "js-cookie";
import {errHandle, msgHandle} from "../../utils/tools";
import {upload} from "../../api/api";
export default
{
  name: "ShareRes",
  data()
  {
    return{
      userId:0,
      ShareRes_major:'',
      ShareRes_name:'',
      ShareRes_attrib:0,
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
        RealShareRes()
        {
          let formData=new FormData();
          formData.append('userId',this.userId);
          formData.append('fileName',this.ShareRes_name);
          formData.append('major',this.ShareRes_major);
          console.log(formData);
          const SRFile=this.$refs.ShareResFile;
          formData.append('file',SRFile.files[0]);
          //console.log(formData);
          upload(formData).then(res=>{
            if(res.data.code===0)
            {
              msgHandle('您已成功分享资源，资源编号是:'+res.data.id);
            }
            else
            {
              errHandle('分享资源失败。');
            }
          }).catch(res=>{
            errHandle('分享资源失败：'+res);
          })


        }
      }
}
</script>

<template>
<div>
  <form>
    <el-input v-model="ShareRes_major" placeholder="设置资源的专业">
      <template #prepend>资源所属专业</template>
    </el-input>
    <br><br>
    <el-input v-model="ShareRes_name" placeholder="设置资源的名称">
      <template #prepend>资源名称</template>
    </el-input>
    <br><br>
    <input type="file" class="dsc-input" ref="ShareResFile">&nbsp;&nbsp;
    <el-button type="primary" @click="RealShareRes()">分享资源</el-button>

  </form>
</div>
</template>

<style scoped>

</style>