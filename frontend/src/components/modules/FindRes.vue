<script>
import { Search } from '@element-plus/icons-vue';
import Cookies from "js-cookie";
import {errHandle} from "../../utils/tools";
import {downloadFile, getUserInformation, showFile} from "../../api/api";
export default
{
  name: "FindRes",
  data()
  {
    return{
      userId:0,
      currentPage:1,
      loading:true,
      pageSize:4,
      SelectId:0,
      Search:Search,
      FindRes_SearchBoxContext:'',
      ResArr_Temp:[],
      ResArr:[],
    }
  },
  mounted()
  {
    this.userId=Cookies.get('userId');
    if(this.userId===0||this.userId===undefined||this.userId===null)
    {
      errHandle('读取用户信息错误，请重新登录系统。');
      this.loading=false;
      return;
    }
    let FindRes_Cache= [
      // {"context":"资源01号","attrib":0,"major":"软件工程","downloadVolume":35,"time":123123},
    ];
    setTimeout(()=>{
        this.getFileInfo().then(res => {
        //console.log(res);
        FindRes_Cache = res;
        this.ResArr_Temp=FindRes_Cache;
        this.ResArr=this.ResArr_Temp;
        this.loading=false;
      });
    },800);


  },
  methods:
      {
        downLoad(id)
        {
          downloadFile(id);
        },
        SearchBoxChange()
        {
          var fd_temp=[];
          this.currentPage=1;
          this.ResArr_Temp.forEach((item) =>
              {
                if(item.major.includes(this.FindRes_SearchBoxContext)||item.context.includes(this.FindRes_SearchBoxContext))
                {
                  fd_temp.push(item);
                }
              }
          );
          this.ResArr=fd_temp;
        },
        async getFileInfo()
        {
          let arr=[];
          const res = await showFile(this.userId);
          const d = res.data.data;
          for(const i in d)
          {
              let item = {"context":"null","major":"null","publishUserNickname":'null','id':-1};
              item.context=d[i].fileName;
              item.major=d[i].major;
              item.id=d[i].id;
              const ui = await getUserInformation(this.userId,this.userId);
              const publishUserNickname = ui.data.data.userNickName;
              item.publishUserNickname=publishUserNickname;
              arr.push(item);
          }
          return arr;
        },
      }

}
</script>

<template>
  <div v-loading="loading" element-loading-text="加载中..." element-loading-background="rgba(0, 0, 0, 0.2)">
    <el-input
        v-model="FindRes_SearchBoxContext"
        class="w-50 m-2"
        placeholder="搜索您想要的资源"
        :prefix-icon="Search"
        id="FindRes-elInput01"
        @keyup="SearchBoxChange()"
    />
    <el-row>
      <el-col
          v-for="item in ResArr.slice((currentPage-1)*pageSize,currentPage*pageSize)"
          :key="item"
          :span="6"
          style="max-width:22.5%;margin-left:1rem;margin-top: 1rem;"
      >
        <el-card :body-style="{ padding: '0px' }">
          <img
              src="../../assets/images/08.jpg"
              class="image"
          />
          <div style="padding: 14px" id="resItemDiv">
            <span>{{ item.context }}<br>({{ item.major }}类)</span>
            <div class="bottom">
              <time class="time">星级资源</time>
              <time class="time">{{ item.time }}</time>
              <el-button text class="button" @click="downLoad(item.id)">下载学习</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <div id="FindRes-el-pagination01">
      <el-pagination background layout="prev, pager, next"
                     :total=this.ResArr.length
                     v-model:page-size="pageSize"
                     v-model:current-page="currentPage"
      />
    </div>
  </div>
</template>

<style scoped>
.time {
  font-size: 12px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}

.image {
  width: 100%;
  display: block;
}
#FindRes-elInput01
{
  width:80%;
  margin-bottom: 1rem;
}
#FindRes-el-pagination01
{
  margin-top: 2rem;
  text-align: right;
  margin-left: 1rem;
  padding-bottom: 2.25rem;
}
@media screen and (max-width: 40rem)
{
  #resItemDiv
  {
    font-size: 0.2rem;
  }

}
</style>