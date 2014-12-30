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
    url: '../wxstore/getUnfinishedOrder',
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
      $('div#order-type-3 > div').remove();
      var orders = data.data, counter = [0, 0, 0];
      for(var i = 0; i < orders.length; i++) {
        var order = orders[i];
        counter[order.status] ++;
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
          "</div><div class='col-md-3 column'>下单时间："+order.pub_date+"<br/>要求送达："+order.rt+
          (order.remarks ? ("<br/>买家留言：" + order.remarks) : "") +
          "</div><div class='col-md-2 column'><button class='btn btn-primary btn-block "+classes[order.status]+
          "' type='button'>" + btnValue[order.status] + "</button></div></div>";
        $('div#order-type-' + order.status).append(innerHtml);
      }
      for(var i = 0; i < 3; i++) {
        $('span#a-' + i).text(counter[i]);
        $('span#counter-' + i).text(counter[i]);
      }
      if(counter[0] > 0) {
        document.getElementById('hint').play();
      }
      $('button.'+classes[0]).on('click', function(){
        var oid = $(this).parents('div.row').attr('id').slice(2);
        $.ajax({
          url: "../wxstore/handleOrder",
          method: "POST",
          data: {oid: oid},
          dataType: 'json',
          success: function(data, e) {
            if(data.ret != 0) {
              alert(data.msg);
              return;
            }
            $("div#o-"+oid).remove();
          }
        });
      });
      $('button.'+classes[1]).on('click', function(){
        var oid = $(this).parents('div.row').attr('id').slice(2);
        $.ajax({
          url: "../wxstore/sendOrder",
          method: "POST",
          data: {oid: oid},
          dataType: 'json',
          success: function(data, e) {
            if(data.ret != 0) {
              alert(data.msg);
              return;
            }
            $("div#o-"+oid).remove();
          }
        });
      });
      $('button.'+classes[2]).on('click', function(){
        var oid = $(this).parents('div.row').attr('id').slice(2);
        $.ajax({
          url: "../wxstore/finishOrder",
          method: "POST",
          data: {oid: oid},
          dataType: 'json',
          success: function(data, e) {
            if(data.ret != 0) {
              alert(data.msg);
              return;
            }
            $("div#o-"+oid).remove();
          }
        });
      });
    }
  });
  setTimeout("flush()", 60000);
}
$(function(){
  flush();
});
