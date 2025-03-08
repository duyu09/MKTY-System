<script>
import ForumInnerHeader from "./ForumInnerHeader.vue";
import { ChatDotRound } from "@element-plus/icons-vue";
import { Clock } from "@element-plus/icons-vue";
import { InfoFilled } from "@element-plus/icons-vue";
import { Promotion } from "@element-plus/icons-vue";
import Cookies from "js-cookie";
import { successHandle } from "../../utils/tools";

import { convertTime,errHandle } from "../../utils/tools";
import {getAvatar, getUserInformation, releaseItem, showForum, showItem, upvote} from "../../api/api";

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
      },
  data()
  {
    return{
      userId:0,
      loading:true,
      ForumName:"智能学习大平台测试论坛",
      ForumImgData:'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      ForumInner_CreateTime:'2023-05-02',
      ForumInner_Attrib:"学术类论坛",
      ForumInner_Id:1,
      ForumInner_Context:'',
      ForumInner_Arr:[],
    }
  },
  methods:
      {
        DZUP(id,userNickname)
        {
          console.log(id);
          upvote(this.userId,id).then(res=>{
            if(res.data.code===0)  { successHandle('给'+userNickname+'点赞成功！'); }
            else  { errHandle('给'+userNickname+'点赞失败'); }
          }).catch(res => { errHandle('给'+userNickname+'点赞失败：'+res); });
        },
        ReplayUP(name,floor)
        {
          console.log(name);
          this.ForumInner_Context="回复 "+floor+"楼：@"+name+" ";
        },
        PublishItem()
        {
          // 发表帖子
          // errHandle('测试');
          const context=this.ForumInner_Context;
          if(context===''||context===undefined||context===null)
          {
            errHandle('不能发表内容为空的帖子哦！');
            return;
          }
          releaseItem(this.userId,this.ForumInner_Id,context).then(res=>{
            if(res.data.code===0)
            {
              successHandle('发表帖子成功！');
              setTimeout(()=>{this.$router.go(0);},1000);
            }
            else { errHandle('发表帖子失败'); }
            this.ForumInner_Context='';
          }).catch(res =>{
            errHandle('发表帖子失败：'+res);
            this.ForumInner_Context='';
          });

        },
        JumpToPerPage(aimUserId)
        {
          Cookies.set('PersonalPageAimUserId',parseInt(aimUserId));
          this.$router.push('/main/PersonalPage');
        },
      },
  mounted()
  {
    const FId=Cookies.get('ForumId');
    const userId=Cookies.get('userId');

    showForum(userId).then(res =>{
      const x=res.data.data;
      for(const i in x)
      {
        if(x[i].id===parseInt(FId))
        {
          this.ForumName=x[i].name;
          //论坛性质，0=其他，1=学术类，2=技术类，3=生活类，-1=学生组织
          if(x[i].attrib===0) { this.ForumInner_Attrib='其他类论坛'; }
          else if(x[i].attrib===1) { this.ForumInner_Attrib='学术类论坛'; }
          else if(x[i].attrib===2) { this.ForumInner_Attrib='技术类论坛'; }
          else { this.ForumInner_Attrib='其他类论坛'; }
          break;
        }
      }
    }).catch(res =>{
      errHandle('未能正确加载论坛帖子：'+res);
    });


    this.userId=userId;
    if(FId===undefined || FId===null)
    {
      errHandle('进入论坛出错，请退出并重新访问。');
      return;
    }
    else { this.ForumInner_Id=FId; }

    async function getData(Forum_Id)
    {
      let res;
      try
      {
        res = await showItem(Forum_Id);
        const code = res.data.code;
        const data = res.data.data;
        //console.log(data);
        if(code!==0) throw Error;
        let rtn=[];
        for(const key in data)
        {
          let tempItem = {
            "id":0,
            "userId":0,
            "userName":"",
            "userNickname":"",
            "userSchool":"",
            "userAvatar":"https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
            "context":"",
            "DZ":0,
            "time":"",
            "floor":1,
          }
          tempItem.id=data[key].id;
          tempItem.userName='加载中...';
          tempItem.userSchool='加载中...';
          tempItem.userAvatar='https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg';
          tempItem.userId=data[key].publishUser;
          tempItem.context=data[key].context;
          tempItem.DZ=data[key].upvote;
          tempItem.time=convertTime(parseInt(data[key].time));
          tempItem.floor=data[key].floor;
          const resUserInfo = await getUserInformation(userId,data[key].publishUser);
          const resUserAvatar = await getAvatar(userId,data[key].publishUser);
          tempItem.userSchool=resUserInfo.data.data.userSchool;
          tempItem.userName=resUserInfo.data.data.userName;
          tempItem.userNickname=resUserInfo.data.data.userNickName;
          tempItem.userAvatar=resUserAvatar.data.imgData;


          rtn.push(tempItem);
          rtn.sort((a,b)=>{return b.id-a.id});
        }
        return rtn;
      }
      catch (e)
      {
        // 报错逻辑
        errHandle("获取数据失败");
      }
    }


    getData(this.ForumInner_Id).then(res => {
      this.ForumInner_Arr = res;
      this.loading=false;
    }).catch(res => {
      errHandle("数据渲染失败。");
      this.loading=false;
    });
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
                    :title="item.userNickname"
                    :width="200"
                    trigger="hover"
                    :content="item.userName"
                >
                  <template #reference>
                    <span class="ForumInner-Class-Span02" @click="JumpToPerPage(item.userId)">{{item.userNickname}}</span>
                  </template>
                </el-popover>
                <div class="ForumInner-Class-Div15">{{item.userSchool}}</div>
              </div>
            </div>
            <div class="ForumInner-Class-Div16">
              &nbsp;{{item.context}}
            </div>
            <div class="ForumInner-Class-Div17">
              点赞量&nbsp;{{item.DZ}}&nbsp;&nbsp;{{ item.time }}
              <span class="ForumInner-Class-Span03">
                <span>第{{ item.floor }}层&nbsp;</span>
                <span @click="item.DZ=item.DZ+1;DZUP(item.id,item.userNickname)" class="ForumInner-Upvote-Btn">点赞</span>&nbsp;
                <span @click="ReplayUP(item.userNickname,item.floor)" class="ForumInner-Reply-Btn">回复</span>
              </span>
            </div>
          </div>
         </div>
        </div>
    </div>

    <div id="ForumInner-Div18">
      <div id="ForumInner-Div19">
        <div id="ForumInner-Div20">
          <div id="PsyChat-Div06">
            <div id="PsyChat-Div07">
              <input id="PsyChat-InputBox01" placeholder="讨论技术，分享生活，请文明用语" v-model="ForumInner_Context" @keyup.enter="PublishItem()" />
              <div id="PsyChat-SendButtonDiv" @click="PublishItem();">
                <el-icon><Promotion /></el-icon><span id="PsyChat-Span02">Send</span>
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
  src: url("../../assets/fonts/HPHS.woff");
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
#ForumInner-Div20
{

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
  margin-top: 1rem;
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
#PsyChat-SendButtonDiv
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
}
#PsyChat-SendButtonDiv:hover
{
  background-color: rgba(255,165,0,0.333);
}
#PsyChat-SendButtonDiv:active
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


  #PsyChat-Span02 {
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