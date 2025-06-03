<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统“MKTY专属医学与诊疗论坛平台 论坛内部”页面Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年04月24日 -->
<!-- 修改日期：2025年04月26日 -->
<script>
import ForumInnerHeader from "@/components/modules/ForumInnerHeader.vue";
import { ChatDotRound, Clock, InfoFilled, Promotion, PictureFilled, 
  Delete, Pointer, ChatLineRound, Star } from "@element-plus/icons-vue";
import { convertTime, convertTimeChinese, errHandle, msgHandle, openNewTab, successHandle } from "@/utils/tools";
import { getCookie, getPostContent, getPostList, getUserAvatar, getUserInfo, getForumInfo, praisePost, deletePost, sendPost } from "@/api/api";

export default
{
  name: "ForumInner",
  components:
  {
    "ForumInnerHeader":ForumInnerHeader,
    "ChatDotRound":ChatDotRound,
    "Clock":Clock,
    "InfoFilled":InfoFilled,
    "Promotion":Promotion,
    "PictureFilled":PictureFilled,
    "Delete":Delete,
    "Pointer":Pointer,
    "ChatLineRound":ChatLineRound,
    "Star":Star
  },
  data()
  {
    return{
      fo_userId:parseInt(getCookie('userId')),
      loading:false,
      ForumName:"正在加载...",
      ForumImgData:'/images/mkty_icon.png',
      ForumInner_CreateTime:'正在加载...',
      ForumInner_Attrib:"正在加载...",
      ForumInner_Id:-1,
      ForumInner_Context:'',
      ForumInner_ContextImage:[],
      ForumInner_PostList:[],
      ForumInner_Arr:[{"userAvatar":"", "userName":"加载中...", "userFrom": "加载中...", "userType": "加载中...", "postTextContent": "加载中...", "postImageContent": [], "postPraiseNumber": 0, "postCreateTime": "加载中...","floor": 0, "postPosterId": 8, "userDescription": "加载中...", "postId":0, "postCreateTimeNumber": 0}],
    }
  },
  methods:
  {
    fi_loadPage()
    {
      getForumInfo(parseInt(this.$route.query.forumId)).then(res=>{
        if(res.data.code!=0){
          errHandle(res.data.msg);
          return;
        }
        this.ForumName = res.data.forumInfo.forumName;
        this.ForumInner_CreateTime = convertTimeChinese(res.data.forumInfo.forumCreateTime * 1000);
        const forumType = parseInt(res.data.forumInfo.forumType);
        if (forumType == 0) {
          this.ForumInner_Attrib = "医学知识论坛";
        } else if (forumType == 1) {
          this.ForumInner_Attrib = "病情讨论区";
        } else {
          this.ForumInner_Attrib = "其它论坛"; 
        }
      }).catch(err=>{
        errHandle(err);
      })

      this.loading = true;
      this.ForumInner_Arr = [];
      const forum_id = parseInt(this.ForumInner_Id);
      getPostList(this.ForumInner_Id).then(async (res)=>{
        if(res.data.code!=0){
          errHandle(res.data.msg);
          return;
        }
        this.ForumInner_PostList = res.data.postList;
        for (const item of this.ForumInner_PostList) {
          const res02 = await getPostContent(parseInt(item));
            if(res02.data.code!=0){
              errHandle(res02.data.msg);
            }
            getUserInfo(parseInt(res02.data.postPosterId)).then(res03=>{
              if(res03.data.code!=0){
                errHandle(res03.data.msg);
              }
              getUserAvatar(parseInt(res02.data.postPosterId)).then(res04=>{
                if(res04.data.code!=0){
                  errHandle(res04.data.msg);
                }

                var userFrom = res03.data.userInfo.userFrom;
                var userType = res03.data.userInfo.userType;
                var userDescription = res03.data.userInfo.userDescription;
                if (userFrom.length > 20) {
                  userFrom = userFrom.substring(0, 20) + "...";
                }
                userDescription = userDescription.substring(0, 12) + "...";
                if(parseInt(userType) == 0){
                  userType = "患者";
                }
                else if(parseInt(userType) == 1){
                  userType = "医师"; 
                }
                else if(parseInt(userType) == 2){
                  userType = "其他人员"; 
                }
                this.ForumInner_Arr.push({
                  "userAvatar": res04.data.userAvatar,
                  "userName": res03.data.userInfo.userName,
                  "userFrom": userFrom,
                  "userType": userType,
                  "userDescription": userDescription,
                  "postTextContent": res02.data.postContent.content,
                  "postImageContent": res02.data.postContent.images,
                  "postPraiseNumber": res02.data.postPraiseNumber,
                  "postId": res02.data.postId,
                  "postCreateTime": convertTimeChinese(res02.data.postCreateTime * 1000),
                  "postCreateTimeNumber": res02.data.postCreateTime,
                  "floor": 0,
                  "postPosterId": res02.data.postPosterId,
                });
                this.ForumInner_Arr.sort((b, a) => parseInt(a.postCreateTimeNumber) - parseInt(b.postCreateTimeNumber));
              });
            });
          
        };
      });
      this.loading = false;

// this.loading = true;
// this.ForumInner_Arr = [];
// const forum_id = parseInt(this.$route.query.forumId);
// if (forum_id == undefined) {
//   errHandle("出错：无法获取论坛编号！");
//   this.loading = false;
//   return;
// }

// this.ForumInner_Id = forum_id;

// // 创建一个数组来收集所有嵌套的Promise
// const allPromises = [];

// getPostList(this.ForumInner_Id).then(res => {
//   if (res.data.code != 0) {
//     errHandle(res.data.msg);
//     this.loading = false;
//     return;
//   }

//   this.ForumInner_PostList = res.data.postList;
  
//   // 收集每个帖子的Promise
//   const postPromises = this.ForumInner_PostList.map(item => {
//     return getPostContent(parseInt(item)).then(res02 => {
//       if (res02.data.code != 0) {
//         errHandle(res02.data.msg);
//         return; // 继续执行其他帖子
//       }
      
//       // 收集用户信息和头像的Promise
//       return Promise.all([
//         getUserInfo(parseInt(res02.data.postPosterId)),
//         getUserAvatar(parseInt(res02.data.postPosterId))
//       ]).then(([res03, res04]) => {
//         if (res03.data.code != 0) {
//           errHandle(res03.data.msg);
//         }
//         if (res04.data.code != 0) {
//           errHandle(res04.data.msg);
//         }
//         var userFrom = res03.data.userInfo.userFrom;
//         var userType = res03.data.userInfo.userType;
//         var userDescription = res03.data.userInfo.userDescription;
//         if (userFrom.length > 20) {
//           userFrom = userFrom.substring(0, 20) + "...";
//         }
//         userDescription = userDescription.substring(0, 12) + "...";
//         if(parseInt(userType) == 0){
//           userType = "患者";
//         }
//         else if(parseInt(userType) == 1){
//           userType = "医师"; 
//         }
//         else if(parseInt(userType) == 2){
//           userType = "其他人员"; 
//         }
//         this.ForumInner_Arr.push({
//           "userAvatar": res04.data.userAvatar,
//           "userName": res03.data.userInfo.userName,
//           "userFrom": userFrom,
//           "userType": userType,
//           "userDescription": userDescription,
//           "postTextContent": res02.data.postContent.content,
//           "postImageContent": res02.data.postContent.images,
//           "postPraiseNumber": res02.data.postPraiseNumber,
//           "postId": res02.data.postId,
//           "postCreateTime": convertTimeChinese(res02.data.postCreateTime * 1000),
//           "postCreateTimeNumber": res02.data.postCreateTime,
//           "floor": 0,
//           "postPosterId": res02.data.postPosterId,
//         });
//         this.ForumInner_Arr.sort((b, a) => parseInt(a.postCreateTimeNumber) - parseInt(b.postCreateTimeNumber));
//       });
//     });
//   });

//   // 将帖子Promise添加到总Promise数组
//   allPromises.push(Promise.all(postPromises));
// }).catch(err => {
//   errHandle(err);
//   this.loading = false;
// });

// // 等待所有Promise完成
// Promise.all(allPromises)
//   .then(() => {
//     var floorCount = 0;
//     this.ForumInner_Arr.forEach(item => {
//       floorCount++;
//       item.floor = floorCount;
//     });
//     this.loading = false;
//   })
//   .catch(err => {
//     errHandle(err);
//     this.loading = false;
//   });
    },
    openNewTab(url)
    {
      openNewTab(url);
    },
    reply(userName)
    {
      this.ForumInner_Context = "回复：@" + userName + "：";
    },
    praise(item)
    {
      const postId = item.postId;
      item.postPraiseNumber++;
      praisePost(parseInt(postId)).then(res=>{
        if(res.data.code!=0){
          errHandle("点赞未成功："+res.data.msg);
          return;
        }
        successHandle("点赞成功！");
      }).catch(err=>{
        errHandle("点赞未成功："+err);
      })
    },
    addImage()
    {
      if(this.ForumInner_ContextImage.length == 3){
        errHandle("最多只能添加三张图片！");
        return;
      }
      // 辅助函数：将文件读取为DataURL
      function readFileAsDataURL(file) {
        return new Promise((resolve) => {
          const reader = new FileReader();
          reader.onload = (e) => resolve(e.target.result);
          reader.readAsDataURL(file);
        });
      }

      // 辅助函数：处理图片（缩放和转换格式）
      function processImage(dataUrl) {
        return new Promise((resolve) => {
          const img = new Image();
          img.onload = () => {
            // 计算缩放比例
            const maxSize = 550;
            let width = img.width;
            let height = img.height;
            if (width > height && width > maxSize) {
              height *= maxSize / width;
              width = maxSize;
            } else if (height > maxSize) {
            width *= maxSize / height;
            height = maxSize;
            }
            // 创建canvas进行缩放和格式转换
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            // 转换为webp格式的base64
            const webpDataUrl = canvas.toDataURL('image/webp', 0.8);
            resolve(webpDataUrl);
          };
          img.src = dataUrl;
        });
      }

      // 创建文件输入元素
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/jpeg, image/jpg, image/png, image/webp';
      input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        try {
          // 读取文件为DataURL
          const originalDataUrl = await readFileAsDataURL(file);
          // 加载图片并处理
          const processedDataUrl = await processImage(originalDataUrl);
          // 添加到数组
          if (processedDataUrl) {
            if (!this.ForumInner_ContextImage) {
              this.ForumInner_ContextImage = [];
            }
            this.ForumInner_ContextImage.push(processedDataUrl);
            console.log('图片已添加到数组:', this.ForumInner_ContextImage);
          }
        } catch (error) {
          console.error('图片处理失败:', error);
        }
      };
      
      // 触发文件选择对话框
      input.click();
    },
    clearImage() {
      this.ForumInner_ContextImage = [];
    },
    deletePost(postId) {
      deletePost(parseInt(postId)).then(res => {
        if (res.data.code != 0) {
          errHandle(res.data.msg);
          return;
        }
        successHandle("删除成功！");
        this.ForumInner_Arr = this.ForumInner_Arr.filter(item => item.postId !== postId);
      }).catch(err => {
        errHandle(err);
      });
    },
    fo_sendPost() {
      if (this.ForumInner_Context.trim() === "") {
        errHandle("请输入内容再发布！");
        return;
      }
      sendPost(parseInt(this.ForumInner_Id), this.ForumInner_Context, (this.ForumInner_ContextImage.join('$^') || '')).then(res => {
        if (res.data.code!= 0) {
          errHandle("未成功发布："+res.data.msg);
          return; 
        }
        this.ForumInner_Context = '';
        this.ForumInner_ContextImage = [];
        this.fi_loadPage();
        successHandle("发布成功！");
      })
    },
    checkPermission() {
      getForumInfo(parseInt(this.ForumInner_Id)).then(res => {
        const forumPermission = parseInt(res.data.forumInfo.forumPermission);
        getUserInfo(parseInt(this.fo_userId)).then(res01=>{
          if(res01.data.code!=0){
            errHandle("用户信息读取错误："+res01.data.msg);
            return "error";
          }
          const userTypeNumber = parseInt(res01.data.userInfo.userType);
          var userType = null;
          switch (userTypeNumber) {
            case 0: userType = "患者"; break;
            case 1: userType = "医师"; break;
            case 2: userType = "其他"; break;
          }
          console.log("用户类型："+userType);
          console.log("论坛权限："+forumPermission);
          if(userType!="医师" && forumPermission==1){
            errHandle('对不起，您不是医师，无权访问仅医师可参与的论坛。');
            msgHandle("对不起，您不是医师，无权访问仅医师可参与的论坛。您将被重定向至论坛概览页面。");
            setTimeout(()=>{this.$router.push({path:"/main/Forum"});},1234);
            return "error";
          }
          if(userType!="患者" && forumPermission==2){
            errHandle('对不起，您不是患者，无权访问仅患者可参与的论坛。');  
            msgHandle("对不起，您不是患者，无权访问仅患者可参与的论坛。您将被重定向至论坛概览页面。");
            setTimeout(()=>{this.$router.push({path:"/main/Forum"});},1234);
            return "error";
          }
        });
      });
    }
  },
  mounted()
  {
    const forum_id = parseInt(this.$route.query.forumId);
    if(forum_id!=undefined){ 
      this.ForumInner_Id = forum_id;
    }
    else{
      errHandle("出错：无法获取论坛编号！");
      return; 
    }
    const result = this.checkPermission();
    if(result != "error"){
      this.fi_loadPage();
    }
  }
}
</script>

<template>
<div id="ForumInner-MainDiv">
  <div id="ForumInner-HeaderDiv">
    <ForumInnerHeader></ForumInnerHeader>
  </div>
  <div id="ForumInner-Div01">
    <div id="ForumInner-Div02">
      <div id="ForumInner-Div04">
        <img id="ForumInner-Image01" :src="ForumImgData" alt="FORUM ICON">&nbsp;&nbsp;
      </div>
      <div id="ForumInner-Div05">
        <div id="ForumInner-Div06">
          {{ ForumName }}
        </div>
        <div id="ForumInner-Div07">
          <span id="ForumInner-Span01">
            <el-icon><ChatDotRound /></el-icon>
            帖子数:{{ ForumInner_Arr.length }}
          </span>
          <span id="ForumInner-Span02">
            <el-icon><InfoFilled /></el-icon>
            {{ ForumInner_Attrib }}
          </span>
        </div>
      </div>
      <div id="ForumInner-Div08">
        <div id="ForumInner-Div09">
          <div>论坛编号：No.{{ ForumInner_Id }}</div>
          <div>创建时间：{{ ForumInner_CreateTime }}</div>
        </div>
      </div>
    </div>
    <div id="ForumInner-Div03">
        <div id="ForumInner-ItemsDiv" v-loading="loading" element-loading-text="加载中..." element-loading-background="rgba(0, 0, 0, 0.2)">
         <div id="ForumInner-Div10">
          <div class="ForumInner-Class-Div11" v-for="item in ForumInner_Arr">
            <div class="ForumInner-Class-Div12">
              <div class="ForumInner-Class-Div13">
                <!-- <img :src="item.userAvatar" class="ForumInner-Class-Image02"> -->
                <el-image :src="item.userAvatar" class="ForumInner-Class-Image02" :preview-src-list="[item.userAvatar]"></el-image>
              </div>
              <div class="ForumInner-Class-Div14">
                <el-popover placement="right" width="auto" trigger="hover">
                  <template #reference>
                    <span class="ForumInner-Class-Span02" @click="openNewTab('/main/PersonalPage?userId=' + item.postPosterId)">{{ item.userName }}</span>
                  </template>
                  <div style="display: flex;">
                    <el-avatar :src="item.userAvatar" size="default" style="cursor: pointer;"></el-avatar>
                    <div style="margin-left: 0.5rem;">
                      <div style="font-weight: bold;">{{ item.userName }}</div>
                      <div>类型：{{ item.userType }}</div>
                    </div>
                  </div>
                  <div style="margin-top: 0.5rem;">
                    用户描述：{{ item.userDescription }}
                  </div>
                </el-popover>
                <div class="ForumInner-Class-Div15">{{ item.userType }} | {{ item.userFrom }}</div>
              </div>
            </div>
            <div class="ForumInner-Class-Div16" style="display: flex;" v-if="item.postImageContent.length!=0">
              <div style="margin-right: 0.75rem;" v-for="(image, index) in item.postImageContent">
                <el-image style="width: 50px; height: 50px; border-radius: 4px;" :src="image" :preview-src-list="item.postImageContent" :initial-index="index" fit="cover" />
              </div>
            </div>
            <div class="ForumInner-Class-Div16">
              &nbsp;{{ item.postTextContent }}
            </div>
            <div class="ForumInner-Class-Div17">
              <el-icon><Star /></el-icon>点赞量&nbsp;{{ item.postPraiseNumber }}&nbsp;&nbsp;
              <el-icon><Clock /></el-icon>{{ item.postCreateTime }}
              <span class="ForumInner-Class-Span03">
                <!-- <span>第{{ item.floor }}层&nbsp;</span> -->
                <span>操作：</span>
                <span @click="praise(item)" class="ForumInner-Upvote-Btn" style="text-decoration: underline;"><el-icon><Pointer /></el-icon>点赞</span>&nbsp;&nbsp;
                <span @click="reply(item.userName);" class="ForumInner-Reply-Btn" style="text-decoration: underline;"><el-icon><ChatLineRound /></el-icon>回复</span>&nbsp;&nbsp;
                <el-popconfirm title="您确定删除吗？" @confirm="deletePost(item.postId);" @cancel="" v-if="item.postPosterId==this.fo_userId">
                  <template #reference>
                    <span>
                      <el-icon size="small" color="red" style="cursor: pointer; font-weight: bold;"><Delete /></el-icon>
                      <span style="color: red; font-weight: bold;">
                        删除
                      </span>
                    </span>
                  </template>
                </el-popconfirm>&nbsp;&nbsp;
              </span>
            </div>
          </div>
          <div style="height: 33.3vh;" class="ForumInner-Class-Div11"></div>
         </div>
        </div>
    </div>

    <div id="ForumInner-Div18">
      <div id="ForumInner-Div19">
        <div id="ForumInner-Div20">

        <div>
          <div id="PsyChat-Div06">
            <div style="display: flex; box-shadow: 0 0 0.8rem 0.075rem rgba(0,0,0,0.5); padding: 0.5rem 0.3rem 0.3rem 0.8rem; margin-bottom: 0.4rem; border-radius: 12px;" v-if="ForumInner_ContextImage.length!=0">
              <div style="margin-right: 0.75rem; align-content:center;font-family: HPHS;">
                <span>添加图片</span>
              </div>
              <div style="margin-right: 0.75rem;" v-for="(image, index) in ForumInner_ContextImage">
                <el-image style="width: 37px; height: 37px; border-radius: 2px;" :src="image" fit="cover" :preview-src-list="ForumInner_ContextImage" :initial-index="index" />
              </div>
              <div style="margin-right: 0.75rem; align-content:center;font-family: HPHS;">
                <el-button type="danger" circle @click="clearImage();"><el-icon><Delete /></el-icon></el-button>
              </div>
            </div>
            <div id="PsyChat-Div07">
              <input id="PsyChat-InputBox01" placeholder="讨论学术，分享病情，请文明用语" v-model="ForumInner_Context" @keyup.enter="" />
              <div class="PsyChat-SendButtonDiv" @click="addImage();">
                <el-icon><PictureFilled /></el-icon><span class="PsyChat-Span02">添图</span>
              </div>
              <div class="PsyChat-SendButtonDiv" @click="fo_sendPost();">
                <el-icon><Promotion /></el-icon><span class="PsyChat-Span02">发布</span>
              </div>
            </div>
          </div>
        </div>


        </div>
      </div>
    </div>

  </div>
</div>
</template>

<style scoped>
@font-face
{
  font-family: HPHS;
  src: url("/fonts/HPHS.woff");
}
#ForumInner-HeaderDiv
{
  width: 100%;
}
#ForumInner-MainDiv
{
  width: 100%;
  display: flex;
  flex-direction: column;
}
#ForumInner-Div01
{
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  position: relative;
}
#ForumInner-Div02
{
  font-family: HPHS, serif;
  height: 4rem;
  box-shadow: 0 0 0.8rem 0.25rem rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
}
#ForumInner-Div03
{
  display: flex;
  justify-content: center;
  height: calc(99.85vh - 9rem);
}
#ForumInner-Div04
{
  display: flex;
  align-items: center;
  height: 100%;
  margin-left: 1.75rem;
  font-size: 1.25rem;
}
#ForumInner-Div05
{
  height: 100%;
  margin-left: 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
#ForumInner-Div06
{
  font-size: 1.25rem;
}
#ForumInner-Div07
{
  font-size: 0.875rem;
  margin-top: 0.35rem;
  display: flex;
  align-items: center;
}
#ForumInner-Div08
{
  flex-grow: 1;
  text-align: right;
  margin-right: 2rem;
}
#ForumInner-Div09
{

}
#ForumInner-Div10
{
  display: flex;
  align-items:center;
  flex-direction: column;
}
.ForumInner-Class-Div11
{
  box-shadow: 0 5px 5px -5px #888888;
  width: 92.5%;
  min-height: 8.25rem;
}
.ForumInner-Class-Div11:hover
{
  background-color: rgb(245,245,245);
}
.ForumInner-Class-Div12
{
  display: flex;
  margin-top: 0.75rem;
}
.ForumInner-Class-Div13
{
  background-color: #3d93ff;
  height: 2.75rem;
  width: 2.75rem;
  border-radius: 2rem;
}
.ForumInner-Class-Div14
{
  margin-left: 1rem;
}
.ForumInner-Class-Div15
{
  color: #555555;
  font-size: 0.85rem;
  margin-top: 0.1rem;
}
.ForumInner-Class-Div16
{
  margin-left: 0.25rem;
  margin-top: 0.75rem;
}
.ForumInner-Class-Div17
{
  margin-left: 0.25rem;
  margin-top: 0.5rem;
  font-size: 0.75rem;
}
#ForumInner-Div18
{
  display: flex;
  justify-content: center;
  position: absolute;
  bottom: 1.5rem;
  width:100%;
}
#ForumInner-Div19
{
  width: 90%;
}
#ForumInner-Span01
{
  display: flex;
  align-items: center;
}
#ForumInner-Span02
{
  display: flex;
  align-items: center;
  margin-left: 1rem;
}
.ForumInner-Class-Span02
{
  font-weight: bolder;
  font-size: 1rem;
  cursor: pointer;
}
.ForumInner-Class-Span03
{
  left:90%;
  position: sticky;
}
.ForumInner-Upvote-Btn:hover
{
  color: darkblue;
  font-weight: bolder;
  cursor: pointer;
}
.ForumInner-Reply-Btn:hover
{
  color: darkblue;
  font-weight: bolder;
  cursor: pointer;
}
#ForumInner-ItemsDiv
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
  flex-direction: column; 
  align-items: center;
}
#PsyChat-Div07
{
  box-shadow: 0 0 0.8rem 0.075rem rgba(0,0,0,0.5);
  background-color: rgba(255,255,255,0.8);
  width:70%;
  height: 2.5rem;
  border-radius: 15px;
  padding: 0.15rem 0.05rem;
  display: flex;
  margin-top: 0.2rem;
  padding-right: 0.75rem; 
  align-items: center;
}
#ForumInner-Image01
{
  border-radius: 4px;
  height: 3rem;
  width: 3rem;
  background-size: cover;
  box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
}
.ForumInner-Class-Image02
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
.PsyChat-SendButtonDiv
{
  background-color: rgba(255,165,0,0.2);
  box-shadow: 0 0 0.35rem 0.05rem rgba(0,0,0,0.4);
  width: 12%;
  margin-left: 1.5%;
  margin-top: 0.1rem;
  margin-bottom: 0.1rem;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 82%
}
.PsyChat-SendButtonDiv:hover
{
  background-color: rgba(255,165,0,0.333);
}
.PsyChat-SendButtonDiv:active
{
  background-color: rgba(255,165,0,0.45);
}
#ForumInner-ItemsDiv::-webkit-scrollbar
{
  display: none;
}

@media screen and (max-width: 40rem)
{
  #ForumInner-Div09
  {
    display: none;
  }


  .PsyChat-Span02 {
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
    width: 87.5%;
  }
}
</style>