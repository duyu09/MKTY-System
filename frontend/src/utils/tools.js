import { ElNotification } from "element-plus";
import { ElMessage, ElMessageBox } from 'element-plus';

export
{
    convertTime,errHandle,msgHandle,successHandle, openNewTab,
    convertTimeChinese, writeImgDataFunc, getImgDataAsBase64Func
}


function convertTime(unixTime)
{
    const date = new Date(unixTime);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const seconds = date.getSeconds();
    // const ms = date.getMilliseconds();
    function pad(number, length = 2)
    {
        return String(number).padStart(length, '0');
    }
    return `${year}-${pad(month)}-${pad(day)} ${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
}


function errHandle(describe)
{
    ElNotification({
        title: '警告',
        message: describe,
        type: 'warning',
    });
}

function msgHandle(describe)
{
    return ElMessageBox.alert(describe, '系统提示', {
        confirmButtonText: '确定'
    });
}

function successHandle(describe)
{
    ElNotification({
        title: '成功',
        message: describe,
        type: 'success',
    });
}

function convertTimeChinese(unixTime)
{
    const date = new Date(unixTime);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const seconds = date.getSeconds();
    // const ms = date.getMilliseconds();
    function pad(number, length = 2)
    {
        return String(number).padStart(length, '0');
    }
    return `${year}年${pad(month)}月${pad(day)}日 ${pad(hours)}时${pad(minutes)}分${pad(seconds)}秒`;
}

function writeImgDataFunc(imgFileSelectRef, imgShowRef) {
    return new Promise((resolve, reject) => {
      const fileBox = imgFileSelectRef;
      const Img = fileBox.files[0];
      const reader = new FileReader();
  
      reader.onloadend = () => {
        const fileContent = reader.result; // 获取文件内容
        if (fileContent.length > 10 * 1024 * 1024) {
          fileBox.value = '';
          imgShowRef.src = "/images/null_avatar.jpg";
          reject(new Error("您选择的图片过大(大于10MB)，无法处理。"));
          return;
        }
  
        imgShowRef.src = fileContent;
        const imgShowPic = imgShowRef;
        imgShowPic.onload = () => {
          const base64String = getImgDataAsBase64Func(imgShowRef);
          resolve(base64String); // 返回 base64String
        };
      };
  
      try {
        reader.readAsDataURL(Img);
      } catch (e) {
        imgShowRef.src = "/images/null_avatar.jpg";
        reject('读取头像文件失败：' + e); // 返回错误
      }
    });
  }

function getImgDataAsBase64Func(img) 
{
    const canvas = document.createElement('canvas');
    canvas.width = 200;
    canvas.height = 200;
    const ctx = canvas.getContext('2d');
    const imgWidth = img.naturalWidth;
    const imgHeight = img.naturalHeight;
    const size = Math.min(imgWidth, imgHeight); // 取宽高中较小的值作为裁剪区域的边长
    const offsetX = (imgWidth - size) / 2;
    const offsetY = (imgHeight - size) / 2;
    ctx.drawImage(img, offsetX, offsetY, size, size, 0, 0, 200, 200);
    const base64String = canvas.toDataURL('image/webp');
    return base64String;
}

function openNewTab(url)
{
  window.open(url, '_blank');
}
