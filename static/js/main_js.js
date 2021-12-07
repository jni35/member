//마우스 이벤트
var pic=document.getElementById('pic');
pic.onmouseover = changePic;
pic.onmouseout = originPic;

function changePic(){
    pic.src = "../static/images/healing.jpg";
}

function originPic(){
    pic.src = "../static/images/activity.jpg";
}
