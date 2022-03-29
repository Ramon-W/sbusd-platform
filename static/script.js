$(document).ready(function(){
  $(".space").click(function() {
    $.ajax({
      type: "POST",
      url: '/space',
      dataType: "json",
      data: JSON.stringify([{'space_i': 'test'}]), //JSOn.stringify
      contentType: 'application/json;charset=UTF-8',
      success: function(result) {
        alert(JSON.stringify(result));
      } 
    });
  });
  $("#information").click(function() {
    $.ajax({
      type: "POST",
      url: '/chat_history',
      dataType: "json",
      contentType: 'application/json;charset=UTF-8',
      success: function(chat_history) {
        alert(JSON.stringify(chat_history));
      } 
    });
  });
});
