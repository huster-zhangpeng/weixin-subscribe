$(function(){
  $.ajax({
    url:"../wxstore/myGoods",
    method: "POST",
    dataType: 'json',
    success: function(data) {
      if(data.ret != 0) {
        alert(data.msg);
        return;
      }

      var goods = data.data;
      for(var i = 0; i < goods.length; i++) {
        var good = goods[i];
        $("table#myGoods tbody").append(
          "<tr id='good-"+good.gid+"'><td><input type='text' value='"+good.gimg+"'></td>"+
          "<td><input type='text' value='"+good.gname+"'></td>" +
          "<td><input type='text' value='"+parseFloat(good.gprice).toFixed(1)+"'></td>" +
          "<td><input type='text' value='"+good.gremain+"'></td>" +
          "<td><input type='text' value='"+good.gdesc+"'></td>" +
          "<td><input type='text' value='"+good.grank+"'></td>" +
          "<td><input class='save' type='button' value='保存'>" +
          "<input class='del' type='button' value='删除'></td></tr>"
        );
      }
      $(".save").on('click', function(e){
        var gid = $(this).parents('tr').attr('id').slice(5); 
        var tds = $(this).parents('tr').children();
        var gimg = tds[0].firstChild.value;
        var gname = tds[1].firstChild.value;
        var gprice = tds[2].firstChild.value;
        var gremain = tds[3].firstChild.value;
        var gdesc = tds[4].firstChild.value;
        var grank = tds[5].firstChild.value;
        $.ajax({
          url:"../wxstore/updateGoods",
          method: "POST",
          data: {
            gid: gid, gimg: gimg, gname: gname, 
            gprice: gprice, gremain: gremain,
            gdesc: gdesc, grank: grank
          },
          dataType: 'json',
          success: function(data) {
            if(data.ret != 0) {
              alert(data.msg);
              return;
            }
            alert("修改成功");
          }
        });
      });
      $(".del").on('click', function(e){
        var gid = $(this).parents('tr').attr('id').slice(5); 
        $.ajax({
          url:"../wxstore/delGoods",
          method: "POST",
          data: {
            gid: gid
          },
          dataType: 'json',
          success: function(data) {
            if(data.ret != 0) {
              alert(data.msg);
              return;
            }
            alert("删除成功");
            $("#good-"+gid).remove();
          }
        });
      
      });
    }
  });
});
