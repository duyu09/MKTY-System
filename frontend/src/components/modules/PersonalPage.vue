<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统的个人主页页面Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年02月09日 -->
<!-- 修改日期：2025年03月02日 -->
<script>
import { errHandle, msgHandle, writeImgDataFunc, convertTime, openNewTab } from "@/utils/tools";
import { convertBlobToBase64, removeCookie, removeToken, getCookie, 
  modifyUserInfo, getMailList, getMailList_Reverse, addMailItem, modifyUserAvatar, 
  modifyUserPassword, deleteMailItem, getUserAvatar, getUserInfo } from "@/api/api";
import "@/assets/css/file_input.css";
import { Delete } from '@element-plus/icons-vue'


export default
{
    name: "PersonalPage",
    data()
    {
      return{
        userId:-1, // 当前登录用户的userId（token的userId）
        aimUserId:-1, // 当前主页对应用户的userId
        userName:'正在加载...',
        userType:-1,  // 0=患者，1=医师，2=其他人员
        userSex:-1,
        userSexPermission:-1, // 1=仅自己可见；0=公开；-1=正在加载
        userAge:-1,
        userAgePermission:-1, // 1=仅自己可见；0=公开；-1=正在加载
        userFrom:'正在加载...',
        userFromPermission:-1, // 1=仅自己可见；0=公开；-1=正在加载
        userContact:'正在加载...',
        userContactPermission:-1, // 1=仅自己可见；0=公开；-1=正在加载
        userDescription:'正在加载...',
        userImportantInfo:'正在加载...',
        userImportantInfoPermission:-1, // 1=仅自己可见；0=公开；-1=正在加载
        userAvatar:'/images/mkty_icon.png',
        userRegisterTime:0,
        changeInfoFormVisible:false,  // 修改信息弹窗打开状态
        loading:true,  // 临时先改成未加载状态
        isModifyInfo:false,  // 是否正在提交修改信息表单（决定是否显示加载图标）
        images:[], // 预加载的背景图片数据
        timer:null,  // 背景切换定时器
        passwordFormVisible:false,  // 修改密码弹窗打开状态
        avatarFormVisible:false,  // 修改头像弹窗打开状态
        mailFormVisible:false,  // 查看留言弹窗打开状态
        mailToOtherFormVisible:false,  // 给TA留言弹窗打开状态
        mailFormLoading:false,  // 留言表单加载状态
        mailToLoading:false,  // 给TA留言表单加载状态
        backgroundImageNumber:7,  // 服务器中预设的背景图片总数量
        mailFormArray:[],  // 接收到的留言数据
        mailToArray:[],  // 发送的留言数据
        mailActiveName:'', 
        mailSendContent:'',  // 发送的留言内容
        InfoForm:{  // 待修改信息的各项数据
          // 无需userId
          userName:'',
          userType:-1,
          userSex:-1,
          userSexPermission:true,  // true=仅自己可见；false=公开
          userAge:-1,
          userAgePermission:true,  // true=仅自己可见；false=公开
          userFrom:'',
          userFromPermission:true,  // true=仅自己可见；false=公开
          userContact:'',
          userContactPermission:true,  // true=仅自己可见；false=公开
          userDescription:'',
          userImportantInfo:'',
          userImportantInfoPermission:true,  // true=仅自己可见；false=公开
          userAvatar:'',
          user_input_old_password:'',
          user_input_new_password:'',
          user_input_new_password02:'',
          PersonalPage_el_avatar_01_src:''
          }
        }
    },
    components: 
    {
      "Delete":Delete
    },
    computed: {
      userName_text() {
        if (this.userName === null || this.userName === undefined) {
          return '无效姓名';
        }
        return this.userName;
      },
      userType_text() {
        if (this.userType === -1) {
          return '正在加载...';
        }
        else if(this.userType === 0){
          return '患者';
        }
        else if(this.userType === 1){
          return '医师';
        }
        else {
          return '其他人员';
        }
      },
      userSex_text() {
        if (this.userSex === -1) {
          return '正在加载...';
        }
        if(this.userSexPermission === 1 && this.userId!==this.aimUserId){
          return "<未公开>"
        }
        return this.userSex === 0 ? '男' : '女';
      },
      userAge_text() {
        if (this.userAge === -1) {
          return '正在加载...';
        }
        if(this.userAgePermission === 1 && this.userId!==this.aimUserId){
          return "<未公开>"
        }
        return this.userAge.toString() + ' 周岁';
      },
      userFrom_text() {
        if(this.userFromPermission === 1 && this.userId!==this.aimUserId){
          return "<未公开>"
        }
        return this.userFrom;
      },
      userContact_text() {
        if(this.userContactPermission === 1 && this.userId!==this.aimUserId){
          return "<未公开>"
        }
        return this.userContact;
      },
      userDescription_text() {
        return this.userDescription;
      },
      userImportantInfo_text() {
        if(this.userImportantInfoPermission === 1 && this.userId!==this.aimUserId){
          return "<未公开>"
        }
        return this.userImportantInfo;
      },
      userRegisterTime_text() {
        if (this.userRegisterTime === null || this.userRegisterTime === undefined) {
          return '无效时间';
        }
        const date = new Date(this.userRegisterTime * 1000);
        const year = date.getFullYear();
        const month = ('0' + (date.getMonth() + 1)).slice(-2);
        const day = ('0' + date.getDate()).slice(-2);
        return `${year}年${month}月${day}日`;
      }
    },
    beforeUnmount(){
      clearInterval(this.timer);  // 清除掉切换背景图片的定时器。
    },
    methods:
      {
        ChangeBackground(){
          const randomIndex=parseInt(Math.random() * this.images.length);
          const mainBody=this.$refs.PersonalPageMainDiv;
          mainBody.style.backgroundImage = `url(${this.images[randomIndex]})`;
          mainBody.style.backgroundRepeat='no-repeat';
          mainBody.style.backgroundSize='cover';
        },
        async preloadImages() {
          // console.log('preloadImages');
          this.images = []; // 清空数组，确保每次调用时都是新的数据
          for (let i = 1; i <= this.backgroundImageNumber; i++) {
            try {
              const imageUrl = `../../images/0${i}.webp`;
              const response = await fetch(imageUrl);
              if (!response.ok) {
                throw new Error(`Failed to fetch image: ${imageUrl}`);
              }
              const blob = await response.blob();
              const base64String = await convertBlobToBase64(blob);
              this.images.push(base64String);
            } 
            catch (error) {
              console.error('Error loading image:', error);
            }
          }
        },
        ppRenderPermissionText(value) {
          return value ? '私密' : '公开';
        },
        loadPage(){
          this.preloadImages().then(() => {
            this.ChangeBackground();
            this.timer = setInterval(() => this.ChangeBackground(), 11111);
          });
          this.userId=parseInt(getCookie('userId'));
          const aimUserId=this.$route.query.userId;
          if(aimUserId===null||aimUserId===undefined){
            this.aimUserId=this.userId;
          }
          else{
            this.aimUserId=parseInt(aimUserId);
          }
          
          getUserInfo(this.aimUserId).then(res=>{
            // console.log(res.data);
            if(res.data.code!==0){
              errHandle('警告：读取用户基本信息错误。');
            }
            else {
              this.userName=res.data.userInfo.userName;
              this.userType=parseInt(res.data.userInfo.userType);
              this.userSex=parseInt(res.data.userInfo.userSex);
              this.userAge=parseInt(res.data.userInfo.userAge);
              this.userFrom=res.data.userInfo.userFrom;
              this.userContact=res.data.userInfo.userContact;
              this.userDescription=res.data.userInfo.userDescription;
              if (this.userType===0 || this.userType === "0"){
                // console.log(res.data.userInfo.doctorImportantInfo);
                this.userImportantInfo=res.data.userInfo.doctorImportantInfo;
              }
              else{
                this.userImportantInfo=res.data.userInfo.patientImportantInfo;
              }
              this.userRegisterTime=parseInt(res.data.userInfo.userRegisterTime);
              this.userSexPermission=parseInt(res.data.userInfo.userSexPermission);
              this.userAgePermission=parseInt(res.data.userInfo.userAgePermission);
              this.userFromPermission=parseInt(res.data.userInfo.userFromPermission);
              this.userContactPermission=parseInt(res.data.userInfo.userContactPermission);
              this.userImportantInfoPermission=parseInt(res.data.userInfo.userImportantInfoPermission);
              getUserAvatar(this.aimUserId).then(res=>{
                this.userAvatar=res.data.userAvatar;
                this.InfoForm.userAvatar=this.userAvatar;
                this.InfoForm.PersonalPage_el_avatar_01_src=this.InfoForm.userAvatar;
              });
              this.InfoForm.userName=this.userName;
              this.InfoForm.userType=this.userType;
              this.InfoForm.userSex=this.userSex;
              this.InfoForm.userAge=this.userAge;
              this.InfoForm.userFrom=this.userFrom;
              this.InfoForm.userContact=this.userContact;
              this.InfoForm.userDescription=this.userDescription;
              this.InfoForm.userImportantInfo=this.userImportantInfo;
              this.InfoForm.userSexPermission=this.userSexPermission===1 ? true : false;
              this.InfoForm.userAgePermission=this.userAgePermission===1 ? true : false;
              this.InfoForm.userFromPermission=this.userFromPermission===1 ? true : false;
              this.InfoForm.userContactPermission=this.userContactPermission===1 ? true : false;
              this.InfoForm.userImportantInfoPermission=this.userImportantInfoPermission===1 ? true : false;
              this.loading=false;
            }
          });
        },
        ppChangeImgDataFunc(){
          const imgSelect=this.$refs.PersonalPage_imgSelect_01;
          const imgShow=this.$refs.PersonalPage_el_avatar_01;
          writeImgDataFunc(imgSelect, imgShow).then(res=>{
            this.InfoForm.userAvatar = res;
            console.log('newImgData:', res);
          }).catch(res=>{
            msgHandle(res);
          });
        },
        changeUserInfo()
        {
          this.isModifyInfo=true;
          if(this.InfoForm.userName===''||this.InfoForm.userName==null)
          {
            msgHandle("修改失败：您必须设置姓名");
            return;
          }
          if(this.InfoForm.userType==-1)
          {
            msgHandle("修改失败：请您选择用户类型");
            return;
          }
          if(this.InfoForm.userSex==-1)
          {
            msgHandle("修改失败：请您选择性别");
            return;
          }
          if(isNaN(parseInt(this.InfoForm.userAge))){
            msgHandle('修改失败：年龄必须填写阿拉伯数字');
            return;
          }
          if(this.InfoForm.userAge==='' || this.InfoForm.userAge==null || this.InfoForm.userAge<0)
          {
            msgHandle("修改失败：您必须设置符合条件的年龄");
            return;
          }
          if(this.InfoForm.userFrom===''||this.InfoForm.userFrom==null)
          {
            msgHandle("修改失败：您必须您的来源地");
            return;
          }
          if(this.InfoForm.userContact===''||this.InfoForm.userContact==null)
          {
            msgHandle("修改失败：您必须设置联系方式");
            return;
          }
          if (this.InfoForm.userDescription.length>1024 || this.InfoForm.userDescription==='' || this.InfoForm.userDescription==null)
          {
            msgHandle("修改失败：您未填写自述或您的自述过长");
            return;
          }
          if (this.InfoForm.userImportantInfo.length>1024 || this.InfoForm.userImportantInfo==='' || this.InfoForm.userImportantInfo==null)
          {
            msgHandle("修改失败：您未填写重要信息或您的重要信息过长");
            return;
          }
          const userSexPermission=this.InfoForm.userSexPermission ? 1 : 0;
          const userAgePermission=this.InfoForm.userAgePermission ? 1 : 0;
          const userFromPermission=this.InfoForm.userFromPermission ? 1 : 0;
          const userContactPermission=this.InfoForm.userContactPermission ? 1 : 0;
          const userImportantInfoPermission=this.InfoForm.userImportantInfoPermission ? 1 : 0;
          modifyUserInfo(
            this.InfoForm.userName,
            this.InfoForm.userType,
            this.InfoForm.userSex,
            userSexPermission,
            this.InfoForm.userAge,
            userAgePermission,
            this.InfoForm.userFrom,
            userFromPermission,
            this.InfoForm.userContact,
            userContactPermission,
            this.InfoForm.userDescription,
            this.InfoForm.userImportantInfo,
            userImportantInfoPermission)
            .then(res=>{
              if (res.data.code!==0){
                this.isModifyInfo=false;
                errHandle('修改失败：'+res.data.msg);
                return;
              }
              this.isModifyInfo=false;
              this.changeInfoFormVisible=false;
              msgHandle('成功执行修改操作').then(res=>{
                window.location.reload();
                return;
              });
            }).catch(res=>{
              this.isModifyInfo=false;
              errHandle('修改失败：'+res);
          });

        },
        changeUserAvatar()
        {
          modifyUserAvatar(this.InfoForm.userAvatar).then(res=>{
            if (res.data.code!==0){
              msgHandle('更换头像失败：'+res.data.msg);
              return;
            }
            msgHandle('成功更换头像').then(res=>{
              window.location.reload();
              return;
            });
          }).catch(res=>{
            msgHandle('更换头像失败：'+res);
          });
        },
        changeUserPassword()
        {
          if(this.InfoForm.user_input_old_password===''||this.InfoForm.user_input_old_password==null)
          {
            msgHandle("修改失败：您必须输入原密码");
            return;
          }
          if(this.InfoForm.user_input_new_password===''||this.InfoForm.user_input_new_password==null)
          {
            msgHandle("修改失败：您必须输入新密码");
            return;
          }
          if(this.InfoForm.user_input_new_password02===''||this.InfoForm.user_input_new_password02==null)
          {
            msgHandle("修改失败：请您再次输入新密码");
            return;
          }
          if(this.InfoForm.user_input_new_password!==this.InfoForm.user_input_new_password02)
          {
            msgHandle("修改失败：两次输入的新密码不一致");
            return;
          }
          modifyUserPassword(this.InfoForm.user_input_old_password, this.InfoForm.user_input_new_password).then(res=>{
            if (res.data.code!==0){
                errHandle('操作失败：'+res.data.msg);
                return;
              }
            msgHandle('成功修改密码').then(res=>{
              window.location.reload();
              return;
            });
          }).catch(res=>{
            errHandle('操作失败：'+res);
          });
        },
        conTime(time){
          return convertTime(time);
        }, 
        getMailFromInfo(){
          // 获取发给我的留言
          getMailList().then(async (res)=>{
            if(res.data.code!==0){
              errHandle('警告：读取留言列表错误。');
            }
            else {
              // console.log(res.data);
              const tempArray=res.data.mailList;
              this.mailFormLoading = true;
              for (const tempArray_item of tempArray) {
                const mailFromUserId = parseInt(tempArray_item.mailFromUserId);
                const res2 = await getUserInfo(mailFromUserId);
                  if(res2.data.code!==0){
                    errHandle('警告：读取用户基本信息错误。');
                  }
                  else {
                    getUserAvatar(mailFromUserId).then(res3=>{
                      if(res3.data.code!==0){
                        errHandle('警告：读取用户头像错误。');
                      }
                      else {
                        var mailFromUserAvatar=res3.data.userAvatar;
                        const mailFromUserName=res2.data.userInfo.userName;
                        const mailItemContent=tempArray_item.mailItemContent;
                        const mailItemSendTime=tempArray_item.mailItemSendTime;
                        const mailItemFromUserType_number=res2.data.userInfo.userType;
                        var mailItemFromUserDescription=res2.data.userInfo.userDescription;
                        mailItemFromUserDescription = mailItemFromUserDescription.length > 18 ? `${mailItemFromUserDescription.slice(0, 18)}...` : mailItemFromUserDescription;
                        var mailItemFromUserType = "<未公开>"
                        if (mailItemFromUserType_number == 0){
                          mailItemFromUserType = "患者";
                        }
                        else if (mailItemFromUserType_number == 1){
                          mailItemFromUserType = "医师";
                        }
                        else if (mailItemFromUserType_number == 2){
                          mailItemFromUserType = "其他人员";
                        }
                        this.mailFormArray.push({
                          mailFromUserId:mailFromUserId,
                          mailFromUserName:mailFromUserName,
                          mailFromUserAvatar:mailFromUserAvatar,
                          mailItemContent:mailItemContent,
                          mailItemSendTime:mailItemSendTime,
                          mailItemFromUserType:mailItemFromUserType,
                          mailItemFromUserDescription:mailItemFromUserDescription
                        });
                        this.mailFormArray.sort((a, b) => {
                          return b.mailItemSendTime - a.mailItemSendTime;
                        });
                    }});
                  }
              };
              this.mailFormLoading = false;
            }
          });
        },
        getMailToInfo(){
          // 获取发给我的留言
          this.mailToArray=[];
          getMailList_Reverse().then(async (res)=>{
            if(res.data.code!==0){
              errHandle('警告：读取留言列表错误。');
            }
            else {
              const tempArray=res.data.mailList;
              this.mailToLoading = true;
              for (const tempArray_item of tempArray) {
                const mailFromUserId = parseInt(tempArray_item.mailToUserId); // 注意这里是mailToUserId，只改这一处，其他的都不用改了
                const res2 = await getUserInfo(mailFromUserId)
                  if(res2.data.code!==0){
                    errHandle('警告：读取用户基本信息错误。');
                  }
                  else {
                    getUserAvatar(mailFromUserId).then(res3=>{
                      if(res3.data.code!==0){
                        errHandle('警告：读取用户头像错误。');
                      }
                      else {
                        var mailFromUserAvatar=res3.data.userAvatar;
                        const mailFromUserName=res2.data.userInfo.userName;
                        const mailItemContent=tempArray_item.mailItemContent;
                        const mailItemSendTime=tempArray_item.mailItemSendTime;
                        const mailItemFromUserType_number=res2.data.userInfo.userType;
                        const mailItemId=tempArray_item.mailItemId;
                        var mailItemFromUserDescription=res2.data.userInfo.userDescription;
                        mailItemFromUserDescription = mailItemFromUserDescription.length > 18 ? `${mailItemFromUserDescription.slice(0, 18)}...` : mailItemFromUserDescription;
                        var mailItemFromUserType = "<未公开>"
                        if (mailItemFromUserType_number == 0){
                          mailItemFromUserType = "患者";
                        }
                        else if (mailItemFromUserType_number == 1){
                          mailItemFromUserType = "医师";
                        }
                        else if (mailItemFromUserType_number == 2){
                          mailItemFromUserType = "其他人员";
                        }
                        this.mailToArray.push({
                          mailItemId:mailItemId,
                          mailFromUserId:mailFromUserId,
                          mailFromUserName:mailFromUserName,
                          mailFromUserAvatar:mailFromUserAvatar,
                          mailItemContent:mailItemContent,
                          mailItemSendTime:mailItemSendTime,
                          mailItemFromUserType:mailItemFromUserType,
                          mailItemFromUserDescription:mailItemFromUserDescription
                        });
                        this.mailToArray.sort((a, b) => {
                          return b.mailItemSendTime - a.mailItemSendTime;
                        });
                    }});
                  }
              };
              this.mailToLoading = false;
            }
          });
        },
        pp_openNewTab(url){
          openNewTab(url);
        },
        getMailFromInfo_close(){
          this.mailFormArray=[];  // 关闭留言窗时清空数组
        },
        getMailToInfo_close(){
          this.mailToArray=[];  // 关闭留言窗时清空数组
        },
        LogOut(){
          removeCookie('userId');
          removeToken();
          this.$router.push('/Login');
        },
        mailTabChange(){
          if(this.mailActiveName==='ToMe'){
            this.getMailFromInfo_close();
            this.getMailFromInfo();
            this.getMailToInfo_close();
          }
          else{
            this.getMailToInfo_close();
            this.getMailToInfo();
            this.getMailFromInfo_close();
          }
        },
        deleteMailItem(mailId){
          deleteMailItem(mailId).then(res=>{
            if(res.data.code!==0){
              errHandle('警告：删除留言错误。');
            }
            else {
              msgHandle('成功删除留言').then(res=>{
                this.getMailToInfo_close();
                this.getMailToInfo();
                return;
              });
            }
          });
        },
        sendMailToOther(){
          if(this.mailSendContent===''||this.mailSendContent==null){
            errHandle('发送失败：您必须填写留言内容');
            return;
          }
          addMailItem(this.mailSendContent, this.aimUserId).then(res=>{
            if(res.data.code!==0){
              errHandle('发送失败：'+res.data.msg);
              return;
            }
            msgHandle('成功发送留言').then(res=>{
              this.mailSendContent='';
              return;
            });
          }).catch(res=>{
            errHandle('发送失败：'+res);
          });  
        }
      },
  mounted()
  {
    this.loadPage();
  }
}
</script>
<template>
    <div id="PersonalPage-MainDiv" ref="PersonalPageMainDiv">
        <div id="PersonalPage-Div01">
          <div id="PersonalPage-Div02">
            <!-- <img id="PersonalPage-Image01" :src="userAvatar"> -->
            <el-image id="PersonalPage-Image01" :src="userAvatar" :preview-src-list="[userAvatar]"></el-image>
          </div>
          <div id="PersonalPage-Div03">
            <el-card shadow="always" id="PersonalPage-Card01"> {{ userName }}的个人名片 </el-card>
          </div>
        </div>
        <div id="PersonalPage-Div04">
          <el-card style="font-size: 1rem;border-radius: 15px;" v-loading="loading" element-loading-text="加载中..." element-loading-background="rgba(0, 0, 0, 0.2)">
            <template #header>
              <div class="card-header">
                <span style="font-size: large;"><b>用户个人信息清单</b></span>&nbsp;&nbsp;
                <span style="font-size: small;">注册时间：{{ userRegisterTime_text }}</span>&nbsp;&nbsp;
                <el-button type="primary" plain @click="changeInfoFormVisible = true" v-if="this.userId===this.aimUserId">
                  修改信息
                </el-button>
              </div>
            </template>
          <div style="overflow-y: auto; height: 45vh;">
            <div class="PersonalPage-TableItem">
              <div style="flex-grow: 1;font-weight: bolder;">用户姓名</div>
              <div style="flex-grow: 1;width: 50%;text-align: left;">{{userName_text}}</div>
            </div>
            <div class="PersonalPage-TableItem">
              <div style="flex-grow: 1;font-weight: bolder;">用户类型</div>
              <div style="flex-grow: 1;width: 50%;text-align: left;">{{userType_text}}</div>
            </div>
            <div class="PersonalPage-TableItem">
              <div style="flex-grow: 1;font-weight: bolder;">用户性别</div>
              <div style="flex-grow: 1;width: 50%;text-align: left;">{{userSex_text}}</div>
            </div>
            <div class="PersonalPage-TableItem">
              <div style="flex-grow: 1;font-weight: bolder;">用户年龄</div>
              <div style="flex-grow: 1;width: 50%;text-align: left;">{{userAge_text}}</div>
            </div>
            <div class="PersonalPage-TableItem">
              <div style="flex-grow: 1;font-weight: bolder;">用户来源</div>
              <div style="flex-grow: 1;width: 50%;text-align: left;">{{userFrom_text}}</div>
            </div>
            <div class="PersonalPage-TableItem">
              <div style="flex-grow: 1;font-weight: bolder;">联系方式</div>
              <div style="flex-grow: 1;width: 50%;text-align: left;">{{userContact_text}}</div>
            </div>
            <div class="PersonalPage-TableItem">
              <div style="flex-grow: 1;font-weight: bolder;">用户描述</div>
              <div style="flex-grow: 1;width: 50%;text-align: left;">{{userDescription_text}}</div>
            </div>
            <div class="PersonalPage-TableItem">
              <div style="flex-grow: 1;font-weight: bolder;">重要备注</div>
              <div style="flex-grow: 1;width: 50%;text-align: left; font-weight: bold;">{{userImportantInfo_text}}</div>
            </div>
          </div>

          </el-card>

          <div id="PersonalPage-Div05">
            <el-button type="primary" round @click="this.mailFormVisible=true" v-if="this.userId===this.aimUserId">查看留言</el-button>  <!-- 查看自己主页时显示 -->
            <el-button type="primary" round @click="this.mailToOtherFormVisible=true" v-if="this.userId!==this.aimUserId">给TA留言</el-button>  <!-- 查看别人用户主页时显示 -->
            <el-button type="primary" round @click="this.$router.push('/main/HomePage')">返回首页</el-button>
            <el-button type="danger" round @click="LogOut()" v-if="this.userId===this.aimUserId">退出登录</el-button>
          </div>
        </div>



      <el-dialog v-model="changeInfoFormVisible" title="修改个人信息" style="min-width: 20rem;font-family: font02;font-size: large;">
      <div style="overflow-y: auto; height: 60vh;" v-loading="isModifyInfo" element-loading-text="正在修改用户信息..." element-loading-background="rgba(50, 50, 50, 0.6)">
        <el-form :model="InfoForm">
          <h3>个人基本信息内容修改</h3>
          <div style="width: 100%;display: flex;justify-content: center;padding-top: 0.5rem;">
            <p style="width: 75%;">
              您修改内容后，请单击表单尾部的“确定”按钮以保存生效。
            </p>
          </div>
          <br>
          <el-form-item label="您的姓名">
            <el-input v-model="InfoForm.userName" autocomplete="off" />
          </el-form-item>
          <el-form-item label="您的性别">
            <el-radio-group v-model="InfoForm.userSex">
              <el-radio-button :label="0">男</el-radio-button>
              <el-radio-button :label="1" >女</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="用户类型">
            <el-radio-group v-model="InfoForm.userType">
              <el-radio-button :label="0">患者</el-radio-button>
              <el-radio-button :label="1">医师</el-radio-button>
              <el-radio-button :label="2">其他人员</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="您的年龄">
            <el-input v-model="InfoForm.userAge" autocomplete="off" />
          </el-form-item>
          <el-form-item label="您的来源">
            <el-input v-model="InfoForm.userFrom" autocomplete="off" />
          </el-form-item>
          <el-form-item label="联系方式">
            <el-input v-model="InfoForm.userContact" autocomplete="off" />
          </el-form-item>
          <el-form-item label="用户描述">
            <el-input v-model="InfoForm.userDescription" autocomplete="off" />
          </el-form-item>
          <el-form-item label="重要信息">
            <el-input v-model="InfoForm.userImportantInfo" autocomplete="off" />
          </el-form-item><br>
          <h3>隐私权限设定</h3>
          <div style="width: 100%;display: flex;justify-content: center;padding-top: 0.5rem;">
            <p style="width: 75%;">
              对于下列所有选项，您勾选意味着对应信息只有您自己可见，若取消勾选则可由所有已注册用户查看与检索。
            </p>
          </div>
          <br>
          <div style="display: flex;justify-content: center;">
          <div style="text-align: left; width: 88%; overflow-y: auto;">
            <div class="pp-permission-item-div">
              <el-checkbox v-model="InfoForm.userSexPermission" label="您的性别" size="large" />&nbsp;&nbsp;
              <span>（当前权限：<span class="pp-permission-item-span">{{ ppRenderPermissionText(InfoForm.userSexPermission) }}</span>）</span>
            </div>
            <div class="pp-permission-item-div">
              <el-checkbox v-model="InfoForm.userAgePermission" label="您的年龄" size="large" />&nbsp;&nbsp;
              <span>（当前权限：<span class="pp-permission-item-span">{{ ppRenderPermissionText(InfoForm.userAgePermission) }}</span>）</span>
            </div>
            <div class="pp-permission-item-div">
              <el-checkbox v-model="InfoForm.userFromPermission" label="您的来源地" size="large" />&nbsp;&nbsp;
              <span>（当前权限：<span class="pp-permission-item-span">{{ ppRenderPermissionText(InfoForm.userFromPermission) }}</span>）</span>
            </div>
            <div class="pp-permission-item-div">
              <el-checkbox v-model="InfoForm.userContactPermission" label="联系方式" size="large" />&nbsp;&nbsp;
              <span>（当前权限：<span class="pp-permission-item-span">{{ ppRenderPermissionText(InfoForm.userContactPermission) }}</span>）</span>
            </div>
            <div class="pp-permission-item-div">
              <el-checkbox v-model="InfoForm.userImportantInfoPermission" label="重要信息" size="large" />&nbsp;&nbsp;
              <span>（当前权限：<span class="pp-permission-item-span">{{ ppRenderPermissionText(InfoForm.userImportantInfoPermission) }}</span>）</span>
            </div>
            <br>
          </div>
          </div>
        </el-form>
        <br>
        <div>
          <div style="text-align: right;margin-right: 1.5rem;">
            <el-button type="primary" round @click="this.avatarFormVisible = true">更换头像</el-button>
            <el-button type="warning" round @click="this.passwordFormVisible = true">修改密码</el-button>
          </div>
          <br>
          <span class="dialog-footer">
            <el-button @click="changeInfoFormVisible = false">取消</el-button>
            <el-button type="primary" @click="changeUserInfo()">确定</el-button>
          </span>
        </div>
      </div>
      </el-dialog>

      <el-dialog v-model="avatarFormVisible" title="更换您的头像" style="min-width: 16rem;font-family: font02;font-size: large;">
        <img :src="InfoForm.PersonalPage_el_avatar_01_src" id="PersonalPage-el-avatar-01" ref="PersonalPage_el_avatar_01" style="border-radius: 4px; height: 4rem; width: 4rem; background-size: cover; box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);object-fit: cover;" /><br><br>
        <input type="file" class="file-input" id="imgSelect" @change="ppChangeImgDataFunc()" ref="PersonalPage_imgSelect_01" aria-label="Upload" accept=".jpg,.jpeg,.png,.webp,.bmp,.gif,.ico">
        <br><br>
        <span class="dialog-footer">
            <el-button @click="avatarFormVisible = false">取消</el-button>
            <el-button type="primary" @click="changeUserAvatar();">确定更换</el-button>
        </span>
      </el-dialog>

      <el-dialog v-model="passwordFormVisible" title="密码修改" style="min-width: 16rem;font-family: font02;font-size: large;">
        <el-form-item label="请输入原密码">
          <el-input v-model="InfoForm.user_input_old_password" type="password" placeholder="Please input original password" show-password />
        </el-form-item>
        <el-form-item label="请设置新密码">
          <el-input v-model="InfoForm.user_input_new_password" type="password" placeholder="Please input new password" show-password />
        </el-form-item>
        <el-form-item label="请您再次输入">
          <el-input v-model="InfoForm.user_input_new_password02" type="password" placeholder="Please input new password again" show-password />
        </el-form-item>
        <span class="dialog-footer">
          <el-button @click="passwordFormVisible = false">取消</el-button>
          <el-button type="primary" @click="changeUserPassword();">确定修改</el-button>
        </span>
      </el-dialog>

      <el-drawer v-model="mailFormVisible" title="留言查看" style="min-width: 16rem;font-size: large;font-family: noto;" @opened="this.mailActiveName='ToMe';mailTabChange();">
        <el-tabs v-model="mailActiveName" class="demo-tabs" style="height: 100%;" @tab-change="mailTabChange()">
          <el-tab-pane label="发给我的留言" name="ToMe" v-loading="this.mailToLoading" element-loading-text="加载中..." element-loading-background="rgba(0, 0, 0, 0.2)">
            <div style="display: flex;flex-direction: column;align-items: flex-start;height: 100%;overflow-y: auto; overflow-x: hidden;">
              <div v-for="item in mailFormArray" class="mail-item-subdiv">
                <div style="display: flex;align-items: center; margin-left: 0.25rem;">
                  <el-avatar :src="item.mailFromUserAvatar" size="small" style="cursor: pointer;"></el-avatar>
                  <div style="font-size: medium;margin-left: 0.4rem;font-weight: bold;cursor: pointer;" @click="pp_openNewTab('/main/PersonalPage?userId='+item.mailFromUserId)">
                  
                    <el-popover placement="right" width="auto" trigger="hover">
                      <template #reference>
                        {{item.mailFromUserName}}
                      </template>
                      <div style="display: flex;">
                        <el-avatar :src="item.mailFromUserAvatar" size="medium" style="cursor: pointer;"></el-avatar>
                        <div style="margin-left: 0.5rem;">
                          <div style="font-weight: bold;">{{item.mailFromUserName}}</div>
                          <div>类型：{{item.mailItemFromUserType}}</div>
                        </div>
                      </div>
                      <div style="margin-top: 0.5rem;">
                        用户描述：{{item.mailItemFromUserDescription}}
                      </div>
                    </el-popover>

                  </div>
                </div>
                <div style="margin: 0.75rem 0.25rem 0rem 0.25rem;">
                  {{ item.mailItemContent }}
                </div>
                <div style="text-align: right;">
                  <span style="font-size: small;">🕗{{ this.conTime(item.mailItemSendTime * 1000) }}</span>
                </div>
                <el-divider style="margin: 10px;"></el-divider>           
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="我发送的留言" name="FromMe" v-loading="this.mailFromLoading" element-loading-text="加载中..." element-loading-background="rgba(0, 0, 0, 0.2)">
            <div style="display: flex;flex-direction: column;align-items: flex-start;height: 100%;overflow-y: auto; overflow-x: hidden;">
              <div v-for="item in mailToArray" class="mail-item-subdiv">
                <div style="display: flex;align-items: center; margin-left: 0.25rem;">
                  <el-avatar :src="item.mailFromUserAvatar" size="small" style="cursor: pointer;"></el-avatar>
                  <div style="font-size: medium;margin-left: 0.4rem;font-weight: bold;cursor: pointer;" @click="pp_openNewTab('/main/PersonalPage?userId='+item.mailFromUserId)">
                  
                    <el-popover placement="right" width="auto" trigger="hover">
                      <template #reference>
                        发给：{{ item.mailFromUserName }}
                      </template>
                      <div style="display: flex;">
                        <el-avatar :src="item.mailFromUserAvatar" size="medium" style="cursor: pointer;"></el-avatar>
                        <div style="margin-left: 0.5rem;">
                          <div style="font-weight: bold;">{{ item.mailFromUserName }}</div>
                          <div>类型：{{ item.mailItemFromUserType }}</div>
                        </div>
                      </div>
                      <div style="margin-top: 0.5rem;">
                        用户描述：{{ item.mailItemFromUserDescription }}
                      </div>
                    </el-popover>

                  </div>
                </div>
                <div style="margin: 0.75rem 0.25rem 0rem 0.25rem;">
                  {{ item.mailItemContent }}
                </div>
                <div style="text-align: right;">
                  <span style="font-size: small;">🕗{{ this.conTime(item.mailItemSendTime * 1000) }}</span>&nbsp;
                  <el-popconfirm title="您确定删除吗？" @confirm="deleteMailItem(item.mailItemId)" @cancel="">
                    <template #reference>
                      <el-icon size="small" color="red" style="cursor: pointer; font-weight: bold;">
                        <Delete />
                      </el-icon>
                    </template>
                  </el-popconfirm>
                </div>
                <el-divider style="margin: 10px;"></el-divider>           
              </div>
            </div>

          </el-tab-pane>
        </el-tabs>
      </el-drawer>

      <el-drawer v-model="mailToOtherFormVisible" title="给TA留言" style="min-width: 16rem;font-family: noto;font-size: large;">
        <el-card>
          <template #header>
            <div class="card-header" style="text-align: left;">
              <span>请写下给 <b>{{ userName }}</b> 的留言：</span>
            </div>
          </template>
          <div>
            <el-input v-model="mailSendContent" clearable placeholder="请输入留言" type="textarea" style="font-family: noto;" :rows="4"></el-input>
          </div>
          <div style="margin-top: 1rem;text-align: left;font-size: small;color: brown;">
            请文明用语，不得发送非法言论，不得频繁发送骚扰内容，平台将严查此类行为。
          </div>
        </el-card>
        <div style="margin-top: 1rem; text-align: right; width: 96%;">
          <el-button @click="mailToOtherFormVisible=false;mailSendContent='';">取消</el-button>
          <el-button type="primary" @click="sendMailToOther();">发送</el-button>
        </div>
      </el-drawer>



    </div>
</template>
<style scoped>
@font-face
{
    font-family: font01;
    src: url('/fonts/xinwei.woff');
}
@font-face 
{
    font-family: font02;
    src: url('/fonts/HPHS.woff');
}
@font-face 
{
  font-family: minhnguyen;
  src: url('/fonts/minhnguyen.woff2');
}
@font-face {
  font-family: noto;
  src: url('/fonts/Noto_Serif_CJK.otf');
}
.el-tabs__content > .el-tab-pane {
  height: 100%;
}
.PersonalPage-TableItem
{
  display: flex;
  padding-top: 0.4rem;
  padding-bottom: 0.4rem;
  background-color: rgba(0,0,0,0.05);
  word-wrap: break-word;
  word-break: break-all;
}
.PersonalPage-TableItem:nth-of-type(2n)
{
  background-color: rgba(0,0,0,0.15);
}
.PersonalPage-TableItem:hover
{
  background-color: rgba(0,0,0,0.35);
  transition: background-color 0.22s ease-in-out;
  font-weight: bold;
}
#PersonalPage-MainDiv
{
    width: 100%;
    text-align: center;
    /* background-image: url('../../assets/images/01.jpg'); */
    background-size: cover;
    background-attachment: fixed;
    overflow: auto;
    transition: background-image 1.111s ease-in-out;
    background-color: rgba(0, 0, 0, 0.48); /* 白色背景，透明度为0.5 */
    background-blend-mode: overlay; /* 混合模式 */
}

#PersonalPage-Div01
{
    display: flex;
    margin-top: 4rem;
    margin-left: 12rem;
    margin-right: 12rem;
}
#PersonalPage-Div02
{
    flex-grow: 1;
    padding: 0.4rem;
    align-content: center;
}
#PersonalPage-Image01
{
    border-radius: 4px;
    height: 4rem;
    width: 4rem;
    background-size: cover;
    box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
}
#PersonalPage-Div03
{
    flex-grow: 8;
    padding: 0.4rem;
    font-size: 1.8rem;
    opacity: 0.85;
    font-family: font01;
    text-shadow: #b5b5f5 2px 2px;
}
#PersonalPage-Card01
{
    box-shadow: 0 0.2rem 0.2rem 0 rgba(0,0,0,0.35);
    background-image:  linear-gradient(to right, white, rgb(166, 234, 255));
    font-weight: bolder;
}
#PersonalPage-Div04
{
    margin-left: 12rem;
    margin-right: 12rem;
    font-size: larger;
    opacity: 0.785;
}
#PersonalPage-Table01
{
    border-radius: 10px;
    text-align: center;
    width: 100%;
    box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
    color: black;
}
#PersonalPage-Div05
{
    text-align: right;
    font-size: smaller;
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
}
#PersonalPage-Span01
{
  color: black;
  cursor: pointer;
  font-weight: bolder;
  font-size: 1.25rem;
}
#PersonalPage-el-avatar-01
{
  cursor: pointer; 
  border-style: solid; 
  border-color: grey; 
  border-width: medium;
}
#PersonalPage-el-avatar-01:hover
{
  border-color: #686abc;
  transition: 0.3s ease-in-out;
}
.pp-permission-item-div
{
  display: flex;
  justify-content: flex-start;
  flex-direction: row;
  align-items: center;
}
.pp-permission-item-span
{
  color: red;
}
.mail-item-subdiv
{
  width: 100%;
  text-align: left;
  border-radius: 10px;
}
.mail-item-subdiv:hover
{
  background-color: rgba(0,0,0,0.1);
  transition: background-color 0.3s ease;
}
@media screen and (max-width:40rem)
{
    #PersonalPage-Div01
    {
        display: block;
        margin-left: 3rem;
        margin-right: 3rem;
    }
    #PersonalPage-Div04
    {
        margin-left: 2.25rem;
        margin-right: 2.25rem;
        margin-top: 1.5rem;
    }
    #PersonalPage-Div05
    {
        margin-bottom: 3.5rem;
    }
}
</style>

