<script>
import ForumInnerHeader from "@/components/modules/ForumInnerHeader.vue";
import { ChatDotRound, Clock, InfoFilled, Promotion, PictureFilled, 
  Delete, Pointer, ChatLineRound, Star } from "@element-plus/icons-vue";
import { convertTime, convertTimeChinese, errHandle, successHandle } from "@/utils/tools";
import { getCookie, getPostContent, getPostList, getUserAvatar, getUserInfo } from "@/api/api";

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
      loading:false,
      ForumName:"正在加载...",
      ForumImgData:'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      ForumInner_CreateTime:'正在加载...',
      ForumInner_Attrib:"正在加载...",
      ForumInner_Id:-1,
      ForumInner_Context:'',
      ForumInner_PostList:[],
      ForumInner_Arr:[{"userAvatar":"", "userName":"加载中...", "userFrom": "加载中...", "userType": "加载中...", "postTextContent": "加载中...", "postImageContent": [], "postPraiseNumber": 0, "postCreateTime": "加载中...","floor": 0, "postPosterId": 8}],
    }
  },
  methods:
  {
    fi_loadPage()
    {
      this.loading = true;
      this.ForumInner_Arr = [];
      const forum_id = parseInt(this.$route.query.forumId);
      if(forum_id!=undefined){ 
        this.ForumInner_Id = forum_id;
      }
      else{
        errHandle("出错：无法获取论坛编号！");
        return; 
      }
      getPostList(this.ForumInner_Id).then(res=>{
        if(res.data.code!=0){
          errHandle(res.data.msg);
          return;
        }
        this.ForumInner_PostList = res.data.postList;
        var floorCount = 0;
        this.ForumInner_PostList.forEach(item=>{
          floorCount++;
          getPostContent(parseInt(item)).then(res02=>{
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
                this.ForumInner_Arr.push({
                  "userAvatar":res04.data.userAvatar,
                  "userName":res03.data.userInfo.userName,
                  "userFrom":res03.data.userInfo.userFrom,
                  "userType":res03.data.userInfo.userType,
                  "postTextContent":res02.data.postContent.content,
                  "postImageContent":res02.data.postContent.images,
                  "postPraiseNumber":res02.data.postPraiseNumber,
                  "postCreateTime":convertTimeChinese(res02.data.postCreateTime * 1000),
                  "floor":floorCount,
                  "postPosterId":res02.data.postPosterId,
                });
              });
            });
          });
        });
      });
      this.loading = false;
    }
  },
  mounted()
  {
    this.fi_loadPage();
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
            {{ ForumInner_Arr.length }}
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
                <img :src="item.userAvatar" class="ForumInner-Class-Image02">
              </div>
              <div class="ForumInner-Class-Div14">
                <el-popover
                    placement="top-start"
                    :title="item.userName"
                    :width="200"
                    trigger="hover"
                    :content="item.userName"
                >
                  <template #reference>
                    <span class="ForumInner-Class-Span02" @click="">{{ item.userName }}</span>
                  </template>
                </el-popover>
                <div class="ForumInner-Class-Div15">{{ item.userType }} | {{ item.userFrom }}</div>
              </div>
            </div>
            <div class="ForumInner-Class-Div16" style="display: flex;">
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
                <span>第{{ item.floor }}层&nbsp;</span>
                <span @click="" class="ForumInner-Upvote-Btn"><el-icon><Pointer /></el-icon>点赞</span>&nbsp;
                <span @click="" class="ForumInner-Reply-Btn"><el-icon><ChatLineRound /></el-icon>回复</span>
              </span>
            </div>
          </div>
         </div>
        </div>
    </div>

    <div id="ForumInner-Div18">
      <div id="ForumInner-Div19">
        <div id="ForumInner-Div20">

        <div>
          <div id="PsyChat-Div06">
            <div style="display: flex; box-shadow: 0 0 0.8rem 0.075rem rgba(0,0,0,0.5); padding: 0.5rem 0.3rem 0.3rem 0.8rem; margin-bottom: 0.4rem; border-radius: 12px;">
              <div style="margin-right: 0.75rem; align-content:center;font-family: HPHS;">
                <span>添加图片</span>
              </div>
              <div style="margin-right: 0.75rem;">
                <el-image style="width: 37px; height: 37px; border-radius: 2px;" src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg" fit="cover" />
              </div>
              <div style="margin-right: 0.75rem;">
                <el-image style="width: 37px; height: 37px; border-radius: 2px;" src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg" fit="cover" />
              </div>
              <div style="margin-right: 0.75rem; align-content:center;font-family: HPHS;">
                <el-button type="danger" circle ><el-icon><Delete /></el-icon></el-button>
              </div>
            </div>
            <div id="PsyChat-Div07">
              <input id="PsyChat-InputBox01" placeholder="讨论学术，分享病情，请文明用语" v-model="ForumInner_Context" @keyup.enter="" />
              <div class="PsyChat-SendButtonDiv" @click="">
                <el-icon><PictureFilled /></el-icon><span class="PsyChat-Span02">添图</span>
              </div>
              <div class="PsyChat-SendButtonDiv" @click="">
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