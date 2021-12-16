//글쓰기 유효성 검사
function checkWriting(){
    var form = document.writeForm;
    var title = form.title.value;
    var content = form.content.value;

    if(title == ""){
        alert("제목은 필수 입력 항목입니다.");
        form.title.focus();
        return false;
    }
    else if(content == ""){
        alert("글 내용은 필수 입력 항목입니다.");
        form.content.focus();
        return false;
    }
    else{
        form.submit();
    }
}