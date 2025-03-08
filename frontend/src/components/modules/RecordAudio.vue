<template>
    <div>
      <button @click="toggleRecording">{{ isRecording ? '停止录音' : '开始录音' }}</button>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';

  
  export default {
    name: 'RecordAudio',
    setup() {
      const isRecording = ref(false); // 是否正在录音
      const audioChunks = ref([]); // 存储录音的音频数据
      let mediaRecorder = null; // MediaRecorder 实例
      let audioBlob = null;
      let audioUrl = null;
      let audio = null;
  
      // 获取音频设备并初始化 MediaRecorder
      const initRecorder = () => {
        navigator.mediaDevices.getUserMedia({ audio: true })
          .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            console.log(mediaRecorder.mimeType)
  
            mediaRecorder.ondataavailable = event => {
              audioChunks.value.push(event.data);
            };
  
            mediaRecorder.onstop = async () => {
              audioBlob = new Blob(audioChunks.value, { type: 'audio/ogg; codecs=opus' });
              audioUrl = URL.createObjectURL(audioBlob);
              audio = new Audio(audioUrl);
  
              // 生成 GUID
              const guid = generateGUID();
  
  
              // 上传 wav 格式的音频
              uploadAudio(guid, audioBlob);
            };
          })
          .catch(error => {
            console.error("无法获取音频设备:", error);
          });
      };
  
      // 按钮点击事件：开始或停止录音
      const toggleRecording = () => {
        console.log('isRecording:', isRecording.value);
        if (isRecording.value) {
          // 停止录音
          mediaRecorder.stop();
          isRecording.value = false;
        } else {
          // 开始录音
          audioChunks.value = [];
          mediaRecorder.start();
          isRecording.value = true;
  
          // 设置 60 秒超时自动停止
          setTimeout(() => {
            if (isRecording.value) {
              mediaRecorder.stop();
              isRecording.value = false;
            }
          }, 10000);
        }
      };
  
      // 生成 GUID
      const generateGUID = () => {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
          var r = Math.random() * 16 | 0,
              v = c === 'x' ? r : (r & 0x3 | 0x8);
          return v.toString(16);
        });
      };
  
      // 使用 ffmpeg.js 将 WAV 转换为 MP3
      // const convertWavToMp3 = async (wavBlob) => {
      //   console.log("1")
      //   const arrayBuffer = await wavBlob.arrayBuffer();
      //   console.log("2")
      //   const fileData = new Uint8Array(arrayBuffer);
      //   console.log("3")
      //   const ffmpeg = new FFmpeg();
      //   console.log("4")
      //   await ffmpeg.load({
      //     coreURL: '/public/esm/ffmpeg-core.js',
      //     wasmURL: '/public/esm/ffmpeg-core.wasm'
      //   });
      //   console.log("5")
      //   ffmpeg.writeFile('input.wav', fileData);
      //   console.log("6")
      //   await ffmpeg.exec(['-i', 'input.wav', 'output.mp3']);
      //   console.log("7")
      //   const mp3Data = ffmpeg.readFile('output.mp3');
      //   console.log("8")
      //   const mp3Blob = new Blob([mp3Data], { type: 'audio/mp3' });
      //   console.log("9")
      //   return mp3Blob;
      // };
  
      // 上传音频文件到服务器
      const uploadAudio = (guid, audioBlob) => {
        console.log("upload")
        const formData = new FormData();
        formData.append('audio', audioBlob, `${guid}.ogg`);
        formData.append('guid', guid);
  
        fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          console.log('上传成功:', data);
        })
        .catch(error => {
          console.error('上传失败:', error);
        });
      };
  
      // 初始化录音功能
      initRecorder();
  
      return {
        isRecording,
        toggleRecording
      };
    }
  };
  </script>
  
  <style scoped>
  button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    background-color: #007BFF;
    color: white;
    border-radius: 5px;
  }
  
  button:focus {
    outline: none;
  }
  </style>
  