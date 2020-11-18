Date.prototype.format =function(format)
{
var o = {
"M+" : this.getMonth()+1, //month
"d+" : this.getDate(), //day
"h+" : this.getHours(), //hour
"m+" : this.getMinutes(), //minute
"s+" : this.getSeconds(), //second
"q+" : Math.floor((this.getMonth()+3)/3), //quarter
"S" : this.getMilliseconds() //millisecond
}
if(/(y+)/.test(format)) format=format.replace(RegExp.$1,
(this.getFullYear()+"").substr(4- RegExp.$1.length));
for(var k in o)if(new RegExp("("+ k +")").test(format))
format = format.replace(RegExp.$1,
RegExp.$1.length==1? o[k] :
("00"+ o[k]).substr((""+ o[k]).length));
return format;
};

function PrefixZero(num, n) {
    return (Array(n).join(0) + num).slice(-n);
}

function to_m(d, is_ms=true) {
    let s = d % 60;
    let m = parseInt(d / 60);
    let res = PrefixZero(m, 2) + ":" + PrefixZero(parseInt(s), 2);
    if (is_ms){
        res += s.toFixed("2").slice(-3);
    }
    return res;
}
