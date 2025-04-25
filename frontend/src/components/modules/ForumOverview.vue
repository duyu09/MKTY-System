<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统“MKTY专属医学与诊疗论坛平台 论坛概览”页面Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年04月12日 -->
<!-- 修改日期：2025年04月24日 -->
<script>
import { Position, Search } from "@element-plus/icons-vue";
import { getForumList, modifyForumType, deleteForum, getUserInfo, getUserAvatar, getCookie } from "@/api/api";
import { convertTimeChinese, errHandle, openNewTab, successHandle } from "@/utils/tools";

export default
{
  name: "ForumOverview.vue",
  components:
      {
        'Position':Position,
        'Search':Search,
      },
  data()
  {
    return{
      fo_userId:getCookie("userId"),
      Search:Search,
      ForumData:[{"forumCreateTime": "2025年", "forumCreator": 1, "forumId": 2, "forumName": "测试论坛", "forumType": "医学知识论坛","forumPermission": "不限人员", "forumCreatorName":"加载中...","forumCreatorAvatar":"","forumCreatorType":"加载中","forumCreatorDescription":"加载中..."}],
      SearchBoxContext:'',
      currentPage:1,
      pageSize:3,
      fo_select_forumPermission:"3",
      fo_select_forumType:"2",
      fo_modify_forumId:null,
      fo_modify_forumName:"正在加载...",
      fo_modify_dialogVisible:false,
      fo_modify_dialogSelect_forumType:"2",
    }
  },
  mounted()
  {
    this.fo_loadForumList();
  },
  methods:
      {
        fo_loadForumList()
        {
          this.ForumData=[];
          getForumList(parseInt(this.fo_select_forumType), parseInt(this.fo_select_forumPermission)).then((res)=>{
            if(res.data.code!=0){
              errHandle("未成功拉取论坛列表");
              return;
            }
            const fd = res.data.forumList;
            fd.forEach((item)=>{
              const forumCreateTime = convertTimeChinese(item.forumCreateTime * 1000);
              const forumCreator = item.forumCreator;
              const forumId = item.forumId;
              const forumName = item.forumName;
              var forumType = null;
              if(item.forumType == 0){
                forumType = "医学知识论坛";
              }else if(item.forumType == 1){
                forumType = "病情讨论区";
              }else if(item.forumType == 2){
                forumType = "所有论坛";
              }
              var forumPermission = null;
              if(item.forumPermission == 0){
                forumPermission = "不限人员";
              }
              else if(item.forumPermission == 1){
                forumPermission = "仅医师参与"; 
              }
              else if(item.forumPermission == 2){
                forumPermission = "仅病患参与";
              }
              else if(item.forumPermission == 3){
                forumPermission = "所有论坛"; 
              }
              if(this.SearchBoxContext==""||item.forumName.includes(this.SearchBoxContext))
              {
                this.ForumData.push({"forumCreateTime":forumCreateTime,"forumCreator":forumCreator,"forumId":forumId,"forumName":forumName,"forumType":forumType,"forumPermission":forumPermission,"forumCreatorName":"加载中...","forumCreatorAvatar":"","forumCreatorType":"加载中","forumCreatorDescription":"加载中..."});
              }
            });
            this.ForumData.forEach((item)=>{
              const forumCreator = item.forumCreator;
              getUserInfo(forumCreator).then((res)=>{
                if(res.data.code!=0){
                  errHandle("未成功获取id：" + forumCreator+ "的用户信息");
                  return;
                }
                const userInfo = res.data.userInfo;
                const forumCreatorName = userInfo.userName;
                var forumCreatorDescription = userInfo.userDescription;
                if(forumCreatorDescription.length>12){
                  forumCreatorDescription = forumCreatorDescription.substring(0,12)+"...";
                }
                var forumCreatorType = null;userInfo.userType;
                if(userInfo.userType == 0){
                 forumCreatorType = "患者"; 
                }
                else if(userInfo.userType == 1){
                  forumCreatorType = "医师"; 
                }
                else if(userInfo.userType == 2){
                  forumCreatorType = "其他类型人员";  
                }
                item.forumCreatorType = forumCreatorType;
                item.forumCreatorName = forumCreatorName;
                item.forumCreatorDescription = forumCreatorDescription;
              });
              getUserAvatar(forumCreator).then((res)=>{
                if(res.data.code!=0){
                  errHandle("未成功获取id：" + forumCreator+ "的用户信息");
                  return;
                }
                const userAvatar = res.data.userAvatar;
                item.forumCreatorAvatar = userAvatar;
              })
            })
          })
        },
        fo_openModifyForumDialog(item)
        {
          this.fo_modify_dialogVisible=true;
          this.fo_modify_forumId=item.forumId;
          this.fo_modify_forumName=item.forumName;
          this.fo_modify_dialogSelect_forumType=item.forumType;
        },
        fo_search()
        {
          this.currentPage=1;
          this.fo_loadForumList();
        },
        ClickForum()
        {
          const id=this.SelectId;
          Cookies.set('ForumId',id);
          this.$router.push("/main/ForumInner"); //跳转到论坛内部页面，并读取cookie.
        },
        openNewTab(url) {
          openNewTab(url); 
        },
        fo_modifyForum()
        {
          modifyForumType(this.fo_modify_forumId, parseInt(this.fo_modify_dialogSelect_forumType)).then((res)=>{
            if(res.data.code!=0){
              errHandle("修改论坛类型失败: " + res.data.msg);
              return;
            }
            this.fo_modify_dialogVisible=false;
            this.fo_loadForumList();
            successHandle("已执行修改论坛元数据。");
          });
        },
        fo_deleteForum()
        {
          deleteForum(this.fo_modify_forumId).then((res)=>{
            if(res.data.code!=0){
              errHandle("删除论坛失败: " + res.data.msg);
              return;
            }
            this.fo_modify_dialogVisible=false;
            this.fo_loadForumList();
            successHandle("已执行删除论坛。");
          });
        }

      }
}
</script>

<template>
<div id="ForumOverview-MainDiv">
  <div id="ForumOverview-SearchBoxDiv" style="display: flex;">
    <el-input
        v-model="SearchBoxContext"
        class="w-50 m-2"
        placeholder="搜索您参与的论坛"
        :suffix-icon="Search"
        input-style="background-color: rgb(240,240,240);"
    />
    <el-select v-model="fo_select_forumType" placeholder="限定论坛类别" style="margin-left: 0.5rem; color: black;">
      <el-option label="医学知识论坛" value="0"></el-option>
      <el-option label="病情讨论区" value="1"></el-option>
      <el-option label="请限定论坛类别" value="2"></el-option>
    </el-select>
    <el-select v-model="fo_select_forumPermission" placeholder="限定论坛权限" style="margin-left: 0.5rem; color: black;">
      <el-option label="不限人员类型" value="0"></el-option>
      <el-option label="仅医师可参与" value="1"></el-option>
      <el-option label="仅病患可参与" value="2"></el-option>
      <el-option label="请限定论坛权限" value="3"></el-option>
    </el-select>
    <el-button type="primary" style="margin-left: 0.5rem;" @click="fo_search();">检索</el-button>
  </div>
  <div style="overflow: auto;">
  <div class="ForumOverview-TableItem"
       v-for="item in ForumData.slice((currentPage-1)*pageSize, currentPage*pageSize)"
  >
    <div class="ForumOverview-TableItemLeft">
      <div class="ForumOverview-TableItemNameLabel">
        论坛名称:<el-icon id="ForumOverview-Pos02"><Position /></el-icon>
      </div>
      <div class="ForumOverview-TableItemName" @click="()=>{this.SelectId=item.id;this.ClickForum();}">
        <el-icon id="ForumOverview-Pos01"><Position /></el-icon>{{ item.forumName }}
      </div>
      <div style="margin-top: 0.6rem;">
        <div class="ForumOverview-TableItemRight" style="display: flex;align-items: center;">
          <span style="font-weight: bolder;">论坛创建者：</span>
          <br class="ForumOverview-Br01">
          <el-popover placement="right" width="auto" trigger="hover">
            <template #reference>
              <div style="display: flex;align-items: center; cursor: pointer;" @click="openNewTab('/main/PersonalPage?userId='+item.forumCreator)">
                <el-avatar :src="item.forumCreatorAvatar" size="small" style="cursor: pointer;"></el-avatar>
                <span style="margin-left: 0.3rem;">{{ item.forumCreatorName }}</span>
              </div>
            </template>
            <div style="display: flex;">
              <el-avatar :src="item.forumCreatorAvatar" size="default" style="cursor: pointer;"></el-avatar>
              <div style="margin-left: 0.5rem;">
                <div style="font-weight: bold;">{{ item.forumCreatorName }}</div>
                <div>类型：{{ item.forumCreatorType }}</div>
              </div>
            </div>
            <div style="margin-top: 0.5rem;">
              用户描述：{{ item.forumCreatorDescription }}
            </div>
          </el-popover>
          <el-button style="margin-left: 0.5rem;" type="primary" size="small" plain @click="fo_openModifyForumDialog(item)" v-if="item.forumCreator==fo_userId">
            修改论坛
          </el-button>

        </div>
      </div>
    </div>
    <div class="ForumOverview-TableItemRight">
      <div><span style="font-weight: bolder;">论坛编号：</span><br class="ForumOverview-Br01">{{ item.forumId }}</div>
      <div><span style="font-weight: bolder;">隶属类别：</span><br class="ForumOverview-Br01">{{ item.forumType }}</div>
      <div><span style="font-weight: bolder;">创建时间：</span><br class="ForumOverview-Br01">{{ item.forumCreateTime }}</div>
      <div><span style="font-weight: bolder;">论坛权限：</span><br class="ForumOverview-Br01">{{ item.forumPermission }}</div>
    </div>
  </div>
  </div>


  <div style="margin-top: 0.5rem;text-align: right;margin-left: 1rem;padding-bottom: 2.25rem;">
    <el-pagination background layout="prev, pager, next"
                   :total=this.ForumData.length
                   v-model:page-size="pageSize"
                   v-model:current-page="currentPage"
    />
  </div>
</div>

<el-dialog title="论坛元数据更改" v-model="fo_modify_dialogVisible">
  <div>
    <div style="margin: 0.5rem;">
      论坛名称：<span style="font-weight: bold;">{{ fo_modify_forumName }}</span>
    </div>
    <div style="margin: 0.5rem;">
      论坛编号：<span style="font-weight: bold;">{{ fo_modify_forumId }}</span>
    </div>
  </div>
  <el-divider />
  <el-form>
    <el-form-item label="论坛类型修改">
      <el-select v-model="fo_modify_dialogSelect_forumType" placeholder="限定论坛类型" style="margin-left: 0.5rem; color: black;">
        <el-option label="医学知识论坛" value="0"></el-option>
        <el-option label="病情讨论区" value="1"></el-option>
    </el-select>
    </el-form-item>
    <el-form-item  label="删除论坛操作">
      <el-popconfirm title="您确定删除吗？" @confirm="fo_deleteForum();" @cancel="">
        <template #reference>
          <el-button type="danger" style="margin-left: 0.5rem;">删除论坛</el-button>
        </template>
      </el-popconfirm>
    </el-form-item>
    <el-form-item label="论坛名称、论坛参与权限等暂不支持修改。"></el-form-item>
  </el-form>
  <div slot="footer" style="display: flex; justify-content: right;">
    <el-button @click="fo_modify_dialogVisible = false">取消</el-button>
    <el-button type="primary" @click="fo_modifyForum()">确定</el-button>
  </div>
</el-dialog>
</template>

<style scoped>
@font-face
{
  font-family: ubuntu;
  src: url("/fonts/ubuntu.woff2");
}
@font-face
{
  font-family: HPHS;
  src: url("/fonts/HPHS.woff2");
}
@font-face
{
  font-family: font01;
  src: url("/fonts/font01.woff2");
}
#ForumOverview-MainDiv
{
  font-family: none,sans-serif;
}
#ForumOverview-SearchBoxDiv
{
  width: 90%;
}
#ForumOverview-Pos01
{
  display: inline;
}
#ForumOverview-Pos02
{
  display: none;
}
.ForumOverview-Br01
{
  display: none;
}
.ForumOverview-TableItem
{
  display: flex;
  font-size: 1rem;
  padding-left: 1rem;
  padding-top: 1rem;
  padding-bottom: 0.75rem;
  box-shadow: 0 4px 7px rgba(0, 0, 0, 0.2);
}
.ForumOverview-TableItem:hover
{
  background-color: rgb(243,243,243);
}
.ForumOverview-TableItemLeft
{
  width: 60%;
}
.ForumOverview-TableItemRight
{
  color: #555555;
  font-family: ubuntu;
  font-size: 0.875rem;
}
.ForumOverview-TableItemNameLabel
{
  padding-bottom: 0.25rem;
  font-family: HPHS, serif;
  color: #555555;
}
.ForumOverview-TableItemName
{
  font-size: 1.5rem;
  display: flex;
  justify-content: left;
  align-items: center;
  font-family: font01, serif;
}
.ForumOverview-TableItemName:hover
{
  color: blue;
  font-style: italic;
  cursor: pointer;
}
@media screen and (max-width: 40rem)
{
  #ForumOverview-SearchBoxDiv
  {
    width: 85%;
  }
  #ForumOverview-Pos01
  {
    display: none;
  }
  #ForumOverview-Pos02
  {
    display: inline;
  }
  .ForumOverview-TableItemName
  {
    font-size: 1.25rem;
  }
  .ForumOverview-TableItemNameLabel
  {
    display: flex;
    justify-content: left;
    align-items: center;
  }
  .ForumOverview-TableItemRight
  {
    font-size: 0.5rem;
  }
  .ForumOverview-Br01
  {
    display: inline;
  }
}
</style>