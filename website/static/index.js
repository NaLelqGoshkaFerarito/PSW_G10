var a=0;
var b=0;
var c=0;
function changeBackground() {
     var x=document.getElementById('bg');
     x.style.backgroundColor='rgb('+a+', '+b+', '+c+')';
     a+=100;
     b+=a+50;
     c+=b+70;
     if(a>255) a=a-b;
     if(b>255) b=a;
     if(c>255) c=b;