$.ajax({
  url: "../wxstore/hasLogin",
  method: "POST",
  async: false,
  dataType: 'json',
  success: function(data) {
    if(data.ret != 0) {
      window.location.href = "login.html";
    }
  }
});
var classes = ['handle', 'start', 'send'];
var btnValue = ['开始处理', '派送', '完成'];
function flush() {
  $.ajax({
    url: '../wxstore/getFinishedOrder',
    method: 'POST',
    dataType: 'json',
    success: function(data) {
      if(data.ret != 0) {
        alert(data.msg);
        return;
      }

      $('div#order-type-0 > div').remove();
      $('div#order-type-1 > div').remove();
      $('div#order-type-2 > div').remove();
      var orders = data.data, counter = [0, 0, 0];
      var now = new Date();
      var day = now.getDate();
      var m = now.getMonth() + 1;
      var month = m < 10 ? '0' + m : '' + m;
      var wtimestamp = now.setDate(day - now.getDay());
      var ws = new Date(wtimestamp);
      var wm = ws.getMonth() + 1, wd = ws.getDate();
      var wmonth = wm < 10 ? '0'+wm : ''+wm;
      var today = now.getFullYear() + '-' + month + '-' + (day > 9 ? ''+day : '0'+day);
      var week = ws.getFullYear() + '-' + wmonth + '-' + (wd < 10 ? '0'+wd : ''+wd);
      var month = now.getFullYear() + '-' + month + '-01';

      for(var i = 0; i < orders.length; i++) {
        var order = orders[i];
        var innerHtml = 
    "<div class='row clearfix' id='o-"+order.id+"'><div class='col-md-4 column'><table class='table'>" +
    "<caption><strong>订单-"+order.o_no+"</strong></caption><tfoot align='right'><tr><td colspan='3'>" +
    "<strong>总计: ￥</strong><span id='total'>"+order.cost.toFixed(1)+"</span></td></tr></tfoot><tbody>";
        var buy = order.buy;
        for(var j = 0; j < buy.length; j++) {
          var good = buy[j];
          innerHtml += "<tr><td>"+good.name+"</td><td>￥"+good.price.toFixed(1)+"</td><td>"+good.num+"</td></tr>";
        }
        var addr = order.addr;
        innerHtml += "</tbody></table></div><div class='col-md-3 column'><address><strong>"+addr.name+"</strong>" +
          "<br/>"+addr.street+"<br/>"+addr.detail+"<br><abbr title='手机'>"+addr.phone+"</abbr></address>" +
          "</div><div class='col-md-3 column'>下单时间："+order.pub_date+"<br/>要求送达："+order.rt +
          (order.remarks ? ("<br/>买家留言：" + order.remarks) : "") +
          "</div><div class='col-md-2 column'></div></div>";
        if(order.pub_date > month) {
          $('div#order-type-2').append(innerHtml);
          counter[2]++;
        }
        if(order.pub_date > week) {
          $('div#order-type-1').append(innerHtml);
          counter[1]++;
        }
        if(order.pub_date > today) {
          $('div#order-type-0').append(innerHtml);
          counter[0]++;
        }
      }
      for(var i = 0; i < 3; i++) {
        $('span#a-' + i).text(counter[i]);
        $('span#counter-' + i).text(counter[i]);
      }
    }
  });
}
$(function(){
  flush();
});
