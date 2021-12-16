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

//시계
setInterval(mywatch,1000);
function mywatch(){
    var data = new Date();
    var now = data.toLocaleString();
    document.getElementById("demo").innerHTML = now;
}
