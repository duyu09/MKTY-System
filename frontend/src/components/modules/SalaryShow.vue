<script>
import * as echarts from 'echarts';
import Cookies from "js-cookie";
export default
{
  name: "SalaryShow",
  data()
  {
    return{
      Salary:6000
    }
  },
  methods:{
    showMain()
    {
      let chartDom = this.$refs.mainDiv;
      let myChart = echarts.init(chartDom, null, {
        renderer: 'svg'
      });
      let option;

      option = {
        series: [
          {
            type: 'gauge',
            center: ['50%', '60%'],
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 15000,
            splitNumber: 4,
            itemStyle: {
              color: '#FFAB91'
            },
            progress: {
              show: true,
              width: 30
            },
            pointer: {
              show: false
            },
            axisLine: {
              lineStyle: {
                width: 30
              }
            },
            axisTick: {
              distance: -45,
              splitNumber: 5,
              lineStyle: {
                width: 2,
                color: '#999'
              }
            },
            splitLine: {
              distance: -52,
              length: 14,
              lineStyle: {
                width: 3,
                color: '#999'
              }
            },
            axisLabel: {
              distance: -20,
              color: '#999',
              fontSize: 20
            },
            anchor: {
              show: false
            },
            title: {
              show: false
            },
            detail: {
              valueAnimation: true,
              width: '90%',
              height :'91%',
              lineHeight: 80,
              borderRadius: 8,
              offsetCenter: [0, '-15%'],
              fontSize: 27,
              fontWeight: 'bolder',
              formatter: '￥{value}',
              color: 'inherit'
            },
            data: [
              {
                value: this.Salary
              }
            ]
          }
        ]
      };
      option && myChart.setOption(option);
    }
  },
  mounted() {
    const salary = parseInt(Cookies.get('Salary'));
    this.Salary=salary;
    this.showMain();
  }
}
</script>

<template>
<div ref="mainDiv" style="width: 100%;height: 100%;"></div>
</template>

<style scoped>

</style>