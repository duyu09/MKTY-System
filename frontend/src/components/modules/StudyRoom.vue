<script>
import Cookies from "js-cookie";
import {convertTimeChinese, errHandle, msgHandle} from "../../utils/tools";
import { Search } from '@element-plus/icons-vue'
import {getMusicList} from "../../api/api";
export default
{
  name: "StudyRoom",
  data()
  {
    return{
      "userId":0,
      "loading01":false,
      "Search":Search,
      "musicSrc":'',
      "studyStatus":false,
      "buttonText":'休息一会',
      "intervalNumber":0,
      'studyStartTimeUnix':0,
      'studyLengthMin':0,
      'studyLeftTimeUnix':0,
      'studyEncourage':'null',
      'studyContext':'null',
      'musicArr':[],
      'musicSearch':'',
      'timeNowString':'null',
      'studyStartTimeString':'null',
      'studyLeftTimeUnixString':'00:00:00',
      'dialogVisible':false,
    }
  },
  components:
      {
        "Search":Search
      },
  mounted()
  {
    const studyStatus=Cookies.get('studyStatus');
    const studyStartTime=Cookies.get('studyStartTime');
    const studyLength=Cookies.get('studyLength');
    const studyLeftTimeUnix=Cookies.get('studyLeftTimeUnix');
    const studyEncourage=Cookies.get('studyEncourage');
    const studyContext=Cookies.get('studyContext');
    if(studyStatus==='true'||studyStatus===true)
    {
      this.studyStatus=true;
    }
    else
    {
      this.studyStatus=false;
    }
    this.studyStartTimeUnix=studyStartTime;
    this.studyLengthMin=studyLength;
    this.studyLeftTimeUnix=studyLeftTimeUnix;
    this.studyEncourage=studyEncourage;
    this.studyContext=studyContext;
    this.studyStartTimeString = convertTimeChinese(parseInt(this.studyStartTimeUnix));
    if(this.studyStatus===false)
    {
      msgHandle('你已经结束本次自习，系统将马上返回首页');
      this.$router.push('/main/HomePage');
    }
    setInterval(()=>{
      this.timeNowString=convertTimeChinese(Date.now());
    },90);

    const interval01=setInterval(()=>{
      if(this.buttonText==='休息一会')
      {
        this.cutTimePerSec();
      }
      },1000);
    this.intervalNumber=interval01;


  },
  methods:
      {
        MS()
        {
          this.loading01=true;
          const context = this.musicSearch;
          if(context===''||context===undefined||context===null) { return; }
          getMusicList(context).then(res=>{
            if(res.data.code!==200)
            {
              errHandle('获取歌曲信息失败！');
              this.loading01=false;
              return;
            }
            const data = res.data.result.songs;
            let arr=[];
            for (let i in data)
            {
              i=parseInt(i);
              let item={'id':0,'name':'null','artist':'null'};
              const id = data[i].id;
              const name = data[i].name;
              const artist = data[i].artists[0].name;
              item.id=id;
              item.name=name;
              item.artist=artist;
              arr.push(item);
            }
            this.musicArr=arr;
            this.loading01=false;
          }).catch(res=>{
            this.loading01=false;
            errHandle('获取歌曲信息失败:'+res);
            return;
          });
        },
        Play(id)
        {
          const realId = this.musicArr[parseInt(id)].id;
          console.log(realId);
          const s='//music.163.com/outchain/player?type=2&id='+String(realId)+'&auto=1&height=66';
          this.musicSrc=s;
        },
        unixTimeDiffToString(milliseconds)
        {
          // 将总毫秒数转换为总秒数
          let totalSeconds = Math.floor(milliseconds / 1000);

          // 计算小时、分钟和秒数
          let hours = Math.floor(totalSeconds / 3600);
          let minutes = Math.floor((totalSeconds % 3600) / 60);
          let seconds = totalSeconds % 60;

          // 将小时、分钟和秒数格式化为两位数的字符串
          let formattedHours = hours.toString().padStart(2, "0");
          let formattedMinutes = minutes.toString().padStart(2, "0");
          let formattedSeconds = seconds.toString().padStart(2, "0");

          // 将格式化的字符串连接起来，用冒号分隔
          return formattedHours+':'+formattedMinutes+':'+formattedSeconds;
        },
        cutTimePerSec() //每秒调用一次
        {
          const leftTime=parseInt(Cookies.get('studyLeftTimeUnix'));
          if(leftTime<=0)
          {
            //console.log('时间到');
            Cookies.set('studyStatus',false);
            clearInterval(this.intervalNumber);
            msgHandle('您的自习时间已到，系统将自动返回主页。');
            this.$router.push('/main/HomePage');
          } //到时间逻辑
          this.studyLeftTimeUnix=leftTime;
          this.studyLeftTimeUnixString=this.unixTimeDiffToString(this.studyLeftTimeUnix);
          Cookies.set('studyLeftTimeUnix',parseInt(leftTime-1000));
        },
        relaBtnClick()
        {
          if(this.buttonText==='休息一会')
          {
            this.buttonText='继续学习';
          }
          else
          {
            this.buttonText='休息一会';
          }
        },
        stopStudy()
        {
          clearInterval(this.intervalNumber);
          Cookies.set('studyStatus',false);
          this.$router.push('/main/HomePage');
        }


      },
}

</script>

<template>
<div id="StudyRoom-MainDiv">
  <div id="sr-div01">
    <div id="sr-div02">
      <div id="sr-div04" v-loading="loading01" element-loading-text="搜索中..." element-loading-background="rgba(0, 0, 0, 0.2)">
        <div id="sr-div07">
          <div id="sr-div06">
            上个自习，听个音乐！
          </div>
          <div id="sr-div08">
            <el-input v-model="musicSearch" placeholder="从海量音乐中搜索..." @keyup.enter="MS()" />
            <el-button type="primary" :icon="Search" @click="MS()"></el-button>
          </div>
          <div id="sr-div09">
            <el-table :data="musicArr" height="252" style="width: 98.5%">
              <el-table-column prop="name" label="歌名" width="180" />
              <el-table-column prop="artist" label="歌手" width="140" />
              <el-table-column prop="address" label="操作" >
                <template #default="scope">
                  <el-button
                      link
                      type="primary"
                      size="small"
                      @click.prevent="Play(scope.$index)"
                  >
                    播放
                  </el-button>
                </template>

              </el-table-column>
            </el-table>
          </div>
        </div>
        <div id="sr-div10">
          <iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 :src="musicSrc"></iframe>
        </div>
      </div>
    </div>
    <div id="sr-div03">
      <div id="sr-div05">
        <div id="sr-div11">
          当前时间：<nobr>{{ timeNowString }}</nobr>
        </div>
        <div id="sr-div14">
          <nobr><b>开始时间：</b>{{ studyStartTimeString }}</nobr>&nbsp;&nbsp;<wbr><nobr><b>自习时长：</b>{{ studyLengthMin }}分钟</nobr>
        </div>
        <div id="sr-div12">
          剩余时间
          <div id="sr-div13">
            {{ studyLeftTimeUnixString }}
          </div>
        </div>
        <div id="sr-div15">
          自习内容：<span style="color: darkgreen;">{{ studyContext }}</span>
        </div>
        <div id="sr-div16">
          鼓励自我：<br>{{ studyEncourage }}
        </div>
        <div id="sr-div17">
          <el-button type="success" @click="relaBtnClick()">{{ buttonText }}</el-button>
          <el-button type="danger" @click="dialogVisible=true;">结束自习</el-button>
        </div>

        <el-dialog
            v-model="dialogVisible"
            title="确认停止"
            width="30%"
        >
          <span>你真的要停止自习吗，再坚持一下也很好啊！</span>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="dialogVisible = false;">继续自习</el-button>
              <el-button type="danger" @click="stopStudy();dialogVisible = false">确定离开</el-button>
            </span>
          </template>
        </el-dialog>

      </div>
    </div>
  </div>
</div>
</template>

<style scoped>
@font-face
{
  font-family: font01;
  src:url('../src/assets/fonts/font01.woff');
}
#StudyRoom-MainDiv
{
  width:100%;
  height:100%;
  background-image: url("../src/assets/images/10.jpg");
  background-attachment: fixed;
  overflow: auto;
}
#sr-div01
{
  display: flex;
  height: 100%;
}
#sr-div02
{
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
#sr-div03
{
  flex-grow: 3;
  display: flex;
  justify-content: center;
  align-items: center;
}
#sr-div04
{
  background-color: rgba(160,160,255,0.55);
  height: calc(100vh * 0.825);
  width: 80%;
  border-radius: 15px;
  box-shadow: 0 0 0.8rem 0.2rem rgba(0,0,0,0.5);

}
#sr-div05
{
  background-color: rgba(160,160,255,0.55);
  height: calc(100vh * 0.825);
  width: 90%;
  border-radius: 15px;
  box-shadow: 0 0 0.8rem 0.2rem rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  flex-direction: column;
}
#sr-div07
{
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
#sr-div06
{
  background-color: rgba(255, 165, 0, 0.20);
  text-align: center;
  font-size: 1.75rem;
  font-family: font01, serif;
  font-weight: 500;
  width: 92.5%;
  margin-top: 1rem;
  border-radius: 10px;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  box-shadow: 0 0 0.8rem 0.2rem rgba(0,0,0,0.5);


}
#sr-div08
{
  display: flex;
  width: 85%;
  margin-top: 1rem;
}
#sr-div09
{
  padding-top: 0.5rem;
  display: flex;
  justify-content: center;
  width:90%;
}
#sr-div10
{
  display: flex;
  justify-content: center;
  align-items: center;
}
#sr-div11
{
  font-family: HPHS, serif;
  margin-top: 1rem;
  font-size: 1.2rem;
}
#sr-div12
{
  font-size: 1.2rem;
  margin-top: 1.25rem;
  text-align: center;
}
#sr-div13
{
  font-size: 4.75rem;
  font-family: HPHS, serif;
}
#sr-div14
{
  margin-top: 0.75rem;
}
#sr-div15
{
  margin-top: 0.75rem;
  font-weight: bolder;
  font-size: 1.5rem;
}
#sr-div16
{
  margin-top: 0.75rem;
  font-size: 1.2rem;
}
#sr-div17
{
  margin-top: 1rem;
}
@media screen and (max-width: 40rem)
{
  #sr-div01
  {
    display: block;
  }
  #sr-div02
  {
    padding-top: 2rem;
  }
  #sr-div03
  {
    padding-top: 2rem;
    padding-bottom: 2.5rem;
  }

  #sr-div11
  {
    text-align: center;
  }
  #sr-div14
  {
    text-align: center;
  }
}
</style>