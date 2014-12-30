$(function(){
  var $_GET = (function(){
    var url = window.document.location.href.toString();
    var u = url.split("?");
    if(typeof(u[1]) == "string"){
      u = u[1].split("&");
      var get = {};
      for(var i in u){
        var j = u[i].split("=");
        get[j[0]] = j[1];
      }
      return get;
    } else {
      return {};
    }
  })();
  localStorage.user = $_GET['user'] || localStorage.user;
  if(!localStorage.user || !$_GET['sid'] || !$_GET['name']){
    window.history.go(-1); 
    return;
  }
  var sname = $.url.decode($_GET['name']);
  document.title = sname;
  $("li#shopname").text(sname);
  localStorage.sname = sname;
  localStorage.sid = $_GET['sid'];

  var sum = 0.0;
  // computeSum();
  $('input').val(0);
  $('#total').html(sum.toFixed(1));

  var goods = {};
  if(sessionStorage.goods) {
    goods = JSON.parse(sessionStorage.goods);
  }
  if(goods && goods[$_GET['sid']]) {
    fillGoods(goods[$_GET['sid']]);
  } else {
    $.ajax({
      url: "../wxstore/goods",
      method: "POST",
      data: {'sid': $_GET['sid']},
      dataType: "json",
      success: function(data, e) {
        if(data.ret != 0){
          $('table').hide();
          $('h3#error').show();
          return;
        }
        goods[$_GET['sid']] = data.data;
        sessionStorage.goods = JSON.stringify(goods);
        fillGoods(data.data);
      }
    });
  }
  function fillGoods(goods) {
    if(goods.length == 0) {
      $('table').hide();
      $('h3#none-tip').show();
    }
    var cart = localStorage.cart && JSON.parse(localStorage.cart);
    if(cart && cart.sid != $_GET['sid']){
      cart = undefined;
    }
    var buy = cart && cart.buy;
    sum = cart && cart.sum || sum;
    for(var i = 0; i < goods.length; i++) {
      var good = goods[i];
      var num = (buy && buy[good.id] && buy[good.id].num) || 0;
      $("table > tbody").append("<tr id='gid-"+ good.id +"'><td>" + good.name +
          "</td><td>￥" + good.price.toFixed(1) +
          "</td><td><div class='input-group'>" +
          "<span class='input-group-addon'><span class='glyphicon glyphicon-minus'></span></span>" +
          "<input type='text' class='form-control' value='"+num+"'/>" +
          "<span class='input-group-addon'><span class='glyphicon glyphicon-plus'></span></span>" +
          "</div></td></tr>");
    }
    $('#total').html(sum.toFixed(1));
    $('div.input-group > span:first-child.input-group-addon').click(function(e) {
      var num = parseInt($(this).next().val());
      if(num > 0) { 
        $(this).next().val( num - 1 );
        sum -= parseFloat($(this).parents("td").prev().text().slice(1));
        $('#total').html(sum.toFixed(1));
      }
    });
    $('div.input-group > span:last-child.input-group-addon').click(function(e) {
      $(this).prev().val( parseInt($(this).prev().val()) + 1 );
      sum += parseFloat($(this).parents("td").prev().text().slice(1));
      $('#total').html(sum.toFixed(1));
    });
    $('input.form-control').blur(function(e) {
      var tmp = parseInt($(this).val());
      if(isNaN(tmp)) tmp = 0;
      $(this).val(tmp);
      computeSum();
    });
  }

  $('button#buy').click(function(e) {
    var goods = $("table > tbody > tr"), buy = {}, cart;
    for(var i = 0; i < goods.length; i++) {
      var item = goods[i];
      var num = parseInt($(item).children('td').eq(2).find('input').val());
      if(num == 0) continue;
      var id = $(item).attr('id');
      buy[id.slice(4)] = {
        'name': $(item).children('td').eq(0).text(),
        'price': $(item).children('td').eq(1).text(),
        'num': num
      };
    }
    if(sum == 0) return;
    cart = {'sid': $_GET['sid'], 'buy':buy, 'sum':sum};
    localStorage.cart = JSON.stringify(cart);
    window.location.href = "confirm.html";
  });
  function computeSum(){
    sum = 0.0;
    var goods = $('.table > tbody > tr');    
    for(var i = 0; i < goods.length; i++) {
      var good = goods[i];
      var price = $(good).children('td').eq(1).text().slice(1);
      var num = $(good).children('td').eq(2).find('input').val();
      sum += parseFloat(price) * parseInt(num);
    }
    $('#total').html(sum.toFixed(1));
  }
});
