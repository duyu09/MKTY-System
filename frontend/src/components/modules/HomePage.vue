<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统登录欢迎页面Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年03月29日 -->
<!-- 修改日期：2025年03月30日 -->
<script>
import { Star } from "@element-plus/icons-vue";
import 'element-plus/dist/index.css';
import { getCookie, getUserInfo, getImportantList } from "@/api/api";
import { errHandle, msgHandle, convertTimeChinese, openNewTab } from "@/utils/tools";
import "@/assets/css/rainbow_text.css";
export default
{
  name:'HomePage',
  components:
  {
    "Star":Star,
  },
  data()
  {
    var greetContext = '早上好';
    const currentHour = new Date().getHours();
    if(currentHour>=11 && currentHour<=13) greetContext='中午好';
    else if(currentHour>13 && currentHour<=18) greetContext='下午好';
    else if(currentHour>=5 && currentHour<11) greetContext='早上好';
    else greetContext='晚上好';
    return {
        hp_userId:-1,
        hp_userName:"",
        GreetContext:greetContext,
        hp_importantItemArray:[],
        hp_dialogFormVisible:false,
    }
  },
  methods:
  {
    getDayOfWeek(unixTimestamp) {
      // 将 Unix 时间戳转换为毫秒
      const date = new Date(unixTimestamp * 1000);
      // 获取星期几 (0 表示星期日，1 表示星期一，..., 6 表示星期六)
      const dayOfWeek = date.getDay();
      // 将星期日 (0) 转换为 7，其他保持不变
      return dayOfWeek === 0 ? 7 : dayOfWeek;
    },
    hp_loadPage()
    {
      this.hp_userId = parseInt(getCookie('userId'));
      getUserInfo(this.hp_userId).then((res) => {
        this.hp_userName = res.data.userInfo.userName;
      });
      getImportantList().then((res) => {
          if (res.data.code == 0) {
            var hp_arrTemp01 = [];
            const il_itemsArr = res.data.importantList;
            il_itemsArr.forEach((item) => {
              var final_item = {};
              final_item.listItemId = item.listItemId;
              final_item.listItemContent = item.listItemContent;
              final_item.listItemIsFinished_number = item.listItemIsFinished;
              final_item.listItemIsFinished = item.listItemIsFinished == 1 ? "已完成" : "未完成";
              final_item.listItemStartTime = convertTimeChinese(item.listItemStartTime * 1000);
              final_item.listItemEndTime = convertTimeChinese(item.listItemEndTime * 1000);
              if (item.listItemTimeMode == 0){
                final_item.listItemTimeMode = "一次性事项";
              }
              else if (item.listItemTimeMode == 1){
                final_item.listItemTimeMode = "周期性事项";
                final_item.listItemStartTime = "-";
                final_item.listItemEndTime = "-";
              }
              else if (item.listItemTimeMode == 2){
                final_item.listItemTimeMode = "无时间要求"; 
              }
              final_item.listItemTimeMode_number = item.listItemTimeMode;
              final_item.listItemPriority = item.listItemPriority == 0 ? "一般事项" : "紧急事项";
              final_item.listItemPriority_number = item.listItemPriority;
              if (item.listItemTimeWeek == 1){
                final_item.listItemTimeWeek = "周一";
              }
              else if (item.listItemTimeWeek == 2){
                final_item.listItemTimeWeek = "周二";
              }
              else if (item.listItemTimeWeek == 3){
                final_item.listItemTimeWeek = "周三";
              }
              else if (item.listItemTimeWeek == 4){
                final_item.listItemTimeWeek = "周四";
              }
              else if (item.listItemTimeWeek == 5){
                final_item.listItemTimeWeek = "周五";
              }
              else if (item.listItemTimeWeek == 6){
                final_item.listItemTimeWeek = "周六";
              }
              else if (item.listItemTimeWeek == 7){
                final_item.listItemTimeWeek = "周日"; 
              }
              else{
                final_item.listItemTimeWeek = "-"; 
              }
              if (item.listItemTimeMode == 0)
              {
                if (item.listItemStartTime > this.il_currentTime){
                  final_item.listItemTimeStatus = "未到时间";
                }
                else if (item.listItemStartTime <= this.il_currentTime && item.listItemEndTime > this.il_currentTime){
                  final_item.listItemTimeStatus = "已到时间";
                }
                else if (item.listItemEndTime <= this.il_currentTime){
                  final_item.listItemTimeStatus = "已超时"; 
                }
              }
              else if (item.listItemTimeMode == 1)
              {
                const currentWeek = this.getDayOfWeek(this.il_currentTime);
                if (item.listItemTimeWeek == currentWeek){
                  final_item.listItemTimeStatus = "已到时间";
                }
                else{
                  final_item.listItemTimeStatus = "未到时间";
                }
              }

              hp_arrTemp01.push(final_item);
            });
            hp_arrTemp01.forEach((item) => {
              console.log(item);
              if ((item.listItemTimeStatus == "已到时间" && item.listItemIsFinished_number == 0) || item.listItemPriority_number == 1){
                this.hp_importantItemArray.push(item);
              }
            });
          } 
        })
    },
    openNewTab(route) {
      openNewTab(route);
    }
  },
  mounted() 
  {
    this.hp_loadPage();
  },
}
</script>
<template>
    <div id="HomePage-MainDiv">
        <div id="HomePage-BlurDiv"></div>
        <div style="z-index: 10;position: relative;width:100%;">
        <div id="HomePage-Div01">
          <div id="HomePage-Div02">
            <!-- <div style="margin-bottom: 1rem;">
              <img src="/images/mkty_cn_light.svg" style="width: 30vw;" />
            </div> -->
            <div style="padding-bottom: 3rem;">
              <el-carousel motion-blur height="40vh" interval="3456" style="border-radius: 20px; background-color: rgb(207, 202, 194);">
                <el-carousel-item v-for="item in 4" :key="item">
                  <!-- <h3 class="small justify-center" text="2xl">{{ item }}</h3> -->
                  <el-image style="width: 100%; height: 100%" :src="`/images/homepage_carousel/0${item}.jpg`" fit="cover"></el-image>
                </el-carousel-item>
              </el-carousel>
            </div>
            <span><nobr>
              <span style="text-shadow: 2px 2px grey;">
                Welcome To&nbsp;
              </span></nobr><wbr><nobr>
              <span class="rainbow_text">明康慧医</span>
            </nobr><wbr>
            <span style="text-shadow: 2px 2px grey;"><nobr>
              智慧医疗系统
            </nobr></span>
            </span>
          </div>
        </div>
        <div id="HomePage-Div03">
          <div id="HomePage-Div04">
            <div id="HomePage-Div05">
                <div id="HomePage-Div06">
                    尊敬的&nbsp;<span id="HomePage-Span01">{{ hp_userName }}</span>&nbsp;用户，{{ GreetContext }}！
                </div>
                <div id="HomePage-Div07">
                    <div id="HomePage-Div08" :style="HomePage_Div08_Style">
                        <div id="HomePage-Div09" @click="hp_dialogFormVisible=true;">
                          查看
                          <span style="color: brown; font-weight: bold;">{{ this.hp_importantItemArray.length }}</span>
                          项未完成或紧急事项
                        </div>
                    </div>
                </div>
            </div>


            <el-dialog v-model="hp_dialogFormVisible" title="速览未完成事项以及紧急事项">
              <div style="height: 40vh;">
                <el-scrollbar max-height="100%">
                  <el-card style="text-align: left; margin-top: 0.5rem;" v-for="item in hp_importantItemArray">
                    <el-icon><Star></Star></el-icon> <b>事项：</b>{{ item.listItemContent }}
                    <span style="color: brown;">
                      <span v-if="item.listItemPriority_number==1">【紧急事项】</span>
                      <span v-else-if="item.listItemIsFinished_number==0">【已到时间但未完成】</span>
                    </span>
                  </el-card>
                </el-scrollbar>
              </div>
              
              <template #footer>
              <span class="dialog-footer">
                 <el-button type="primary" @click="openNewTab('/main/ImportantList')">前往完成</el-button>
                 <el-button type="primary" @click="hp_dialogFormVisible=false">关闭</el-button>
              </span>
              </template>
            </el-dialog>

            <div id="MOBdiv">
            <div class="HomePage-MenuRowDiv">
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell" >
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/PersonalPage')"><el-icon><Star /></el-icon>我的主页</div>
                </div>
              </div>
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell" >
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/GuideFuture/JobAndSalary')"><el-icon><Star /></el-icon>我的未来</div>
                </div>
              </div>
            </div>
            <div class="HomePage-MenuRowDiv">
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell">
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/Forum')"><el-icon><Star /></el-icon>论坛社团</div>
                </div>
              </div>
            </div>
            <div class="HomePage-MenuRowDiv">
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell" >
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/PsyChat')"><el-icon><Star /></el-icon>小智同学</div>
                </div>
              </div>
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell">
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/StartStudy')"><el-icon><Star /></el-icon>云上自习</div>
                </div>
              </div>
            </div>
            <div class="HomePage-MenuRowDiv">
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell">
                  <div class="HomePage-ButtonDiv"  @click="() => this.$router.push('/main/Resources')"><el-icon><Star /></el-icon>资源天地</div>
                </div>
              </div>
              <div style="flex-grow: 1;">
                <div class="HomePage-ButtonDiv-Shell">
                  <div class="HomePage-ButtonDiv" @click="() => this.$router.push('/main/AimList')"><el-icon><Star /></el-icon>我的目标</div>
                </div>
              </div>
            </div>
            </div>
          </div>
        </div>
        <div id="HomePage-FooterDiv01">
            &copy; 2023~2025 DuYu, Faculty of Computer Science and Technology, QLU(SDAS).
        </div>
        <div id="HomePage-FooterDiv02">
            &copy; 2025 DuYu, QLU(SDAS).
        </div>
        </div>
    </div>
</template>
<style>
@font-face
{
    font-family: font01;
    src: url('/fonts/font01.woff');
}
@font-face
{
    font-family: HPHS;
    src: url('/fonts/HPHS.woff');
}
@font-face
{
    font-family: ubuntu;
    src: url('/fonts/ubuntu.woff2');
}
@font-face {
  font-family: xinwei;
  src: url('/fonts/xinwei.woff');
}
#MOBdiv
{
  display: none;
}
#HomePage-MainDiv
{
    width: 100%;
    height: 100%;
    text-align: center;
    background-color: rgba(242, 223, 187, 0.25);
    background-size: cover;
    background-repeat: no-repeat;
    display: flex;
    flex-direction: row;
    align-content: center;
    flex-wrap: wrap;
}
#HomePage-Div01
{
    display: flex;
    justify-content: center;
}
#HomePage-Div02
{
    /* margin-top: 2.25rem;
    padding-top: 1.25rem; */
    /* padding-bottom: 1rem; */
    font-weight: 500;
    text-align: center;
    width: 93%;
    font-family: xinwei, serif;
    font-size: 2.75rem;
    color: black;
    border-radius: 14px;
}
#HomePage-Div03
{
    display: flex;
    justify-content: center;
}
#HomePage-Div04
{
    margin-top: 1.85rem;
    padding-top: 1.25rem;
    padding-bottom: 1.25rem;
    font-size: 1rem;
    box-shadow: 0 0 0.8rem 0.4rem rgba(0,0,0,0.5);
    text-align: center;
    width: 70%;
    border-radius: 14px;
}
#HomePage-Div05
{
    display: flex;
}
#HomePage-Div06
{
    font-family: HPHS,serif;
    font-size: 1.4rem;
    flex-grow: 1;
    text-shadow: 0.5px 0.5px black;
    color: rgb(0, 0, 80);
}
#HomePage-Span01
{
    font-family: font01,serif;
    font-size: 1.55rem;
}
#HomePage-Div07
{
    flex-grow: 1;
}
#HomePage-Div08
{
    display: flex;
    justify-content: center;
}
#HomePage-Div09
{
    display:flex;
    justify-content: center;
    width: 86%;
    box-shadow: 0 0 0.8rem 0.25rem rgba(0,0,0,0.5);
    background-color: rgba(0,0,255,0.12);
    font-size: 1.35rem;
    font-family: HPHS,serif;
    border-radius: 10px;
    padding-top: 0.175rem;
    padding-bottom: 0.175rem;
    cursor: pointer;
}
#HomePage-Div09:hover
{
    background-color:rgba(0, 0, 255, 0.3);
}
#HomePage-Div09:active
{
    background-color:rgba(0, 0, 255, 0.45);
}
#HomePage-FooterDiv01,#HomePage-FooterDiv02
{
    margin-top: 5rem;
    margin-bottom: 2rem;
    color: #0f2d73;
    font-family: ubuntu,serif;
}
#HomePage-Div08-Vice
{
    display: flex;
    justify-content: center;
}
#HomePage-Div09-Vice
{
    font-family: HPHS,serif;
    font-size: larger;
    width: 80%;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    border-radius: 10px;
    background-color: rgba(255, 140, 0, 0.15);
    color: rgb(120, 0, 0);
}
.HomePage-ButtonDiv-Shell
{
    display: flex;
    justify-content: center;
    margin-top: 0.8rem;
    margin-bottom: 0.8rem;
}
.HomePage-ButtonDiv
{
    display:flex;
    justify-content: center;
    width: 60%;
    box-shadow: 0 0 0.8rem 0.25rem rgba(0,0,0,0.5);
    background-color: rgba(255, 90, 0, 0.2);
    font-size: 1.2rem;
    font-family: HPHS, serif;
    border-radius: 10px;
    padding-top: 0.35rem;
    padding-bottom: 0.35rem;
    cursor: pointer;
}
.HomePage-ButtonDiv:hover
{
    background-color:rgba(255, 90, 0, 0.3);
}
.HomePage-ButtonDiv:active
{
    background-color:rgba(255, 90, 0, 0.45);
}
.HomePage-MenuRowDiv
{
    display: flex;
}
@media screen and (max-width:40rem) 
{
    #HomePage-Div02
    {
        font-size: 2rem;
    }
    #HomePage-Div05
    {
        display: block;
    }
    #HomePage-MainDiv
    {
        background-image: url('/images/03.jpg');
        background-position-x: right;
        background-attachment: fixed;
        height: 100%;
        position: relative;
        overflow: auto;
    }
    #HomePage-BlurDiv
    {
        position:fixed;
        width: 100%;
        height: 100%;
        top:0;
        left:0;
        -webkit-backdrop-filter: blur(30px);
		backdrop-filter: blur(30px);
        z-index: 0;
    }
    #HomePage-Div07
    {
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    #HomePage-FooterDiv01
    {
        display: none;
    }
    #HomePage-FooterDiv02
    {
        display: block;
    }
    .HomePage-MenuRowDiv
    {
        display: block;
    }
    .HomePage-ButtonDiv-Shell
    {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .HomePage-ButtonDiv
    {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
}
@media screen and (min-width: 40rem)
{
    #HomePage-FooterDiv02
    {
        display: none;
    }
    #HomePage-FooterDiv01
    {
        display: block;
    }
}
@media screen and (max-width: 40rem)
{
  #MOBdiv
  {
    display: block;
  }
  #HomePage-FooterDiv02
  {
    color: white;
    margin-top: 3rem;
  }
}
</style>