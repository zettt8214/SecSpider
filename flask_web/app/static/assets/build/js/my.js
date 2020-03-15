$(document).ready(function(){
  $("#btn_sendemail").click(function(){
    $(this).hide();
    $('#save_sendemail').attr("style","");
    $('.sendemail').removeAttr("disabled");
  });

  $("#btn_setagent").click(function () {
      $(this).hide();
      $('#save_agent').removeAttr("style");
      $('.setagent').removeAttr('disabled')
  });



  $('#EmailSet').click(function () {
      var recvemail=$('#recvemail').val()


      $.ajax({
          type:"POST",
          url:"email_set",
          async:true,
          contentType: "application/json;charset=utf-8",
          data:JSON.stringify({'recvemail':recvemail,'action':'add'}),
          success:function () {

            $('#myModal').modal('hide');
            $('#emailList').append('<li class="list-group-item"><span class="badge delete">删除</span>'+recvemail+'</li>')
          }
      })
  });


  // $('.delete').on('click',function () {
  //     var recvemail=$(this).parent().text().substring(2)
  //
  //     var element=$(this).parent()
  //     $.ajax({
  //         type:"POST",
  //         url:"email_set",
  //         async:true,
  //         contentType: "application/json;charset=utf-8",
  //         data:JSON.stringify({'recvemail':recvemail,'action':'delete'}),
  //         success:function () {
  //           alert('delete seccuss');
  //           element.remove()
  //         }
  //     })
  // })

     $('#btn_save').click(function () {
         var title=$('#title').val()
         var href=$('#href').val()
         var time=$('#time').val()
         $.ajax({
          type:"POST",
          url:"../save/",
          async:true,
          contentType: "application/json;charset=utf-8",
          data:JSON.stringify({'title':title,'href':href,'time':time}),
          success:function (data) {
              data=JSON.parse(data)
              if(data.code==1){
                  $('#title').val("");
                  $('#href').val("");
                  $('#time').val("");
              }
              else{
                  alert(title+" "+data.message)
              }
          }
      })
     });

     $('.add').click(function () {
         var title=$(this).parents("tr").find("a").html();
         var date=$(this).parents("tr").find("span")[0].textContent;
         var href=$(this).parents("tr").find("a")[0].href;
         $.ajax({
          type:"POST",
          url:"/auth/save/",
          async:true,
          contentType: "application/json;charset=utf-8",
          data:JSON.stringify({'title':title,'href':href,'time':date}),
          success:function (data) {
              data=JSON.parse(data)
                if(data.code==1){
                  $('#title').val("");
                  $('#href').val("");
                  $('#time').val("");
              }
              else{
                  alert(title+" "+data.message)
              }
          }
      })
     });



 });

$(document).on("click", ".delete", function () {
  var recvemail=$(this).parent().text().substring(2)

  var element=$(this).parent()
  $.ajax({
      type:"POST",
      url:"email_set",
      async:true,
      contentType: "application/json;charset=utf-8",
      data:JSON.stringify({'recvemail':recvemail,'action':'delete'}),
      success:function () {
        element.remove()
      }
  });
});

$(document).on("click", ".infodelete", function () {
  var title=$(this).parents("tr").find("a").html();

  var element=$(this).parents("tr")
  $.ajax({
      type:"POST",
      url:"/auth/delete/",
      async:true,
      contentType: "application/json;charset=utf-8",
      data:JSON.stringify({'title':title}),
      success:function () {
        element.remove()
      }
  });
});