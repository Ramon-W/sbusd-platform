$(document).ready(function(){
  $(".space").click(function() {
    $.ajax({
      type: "POST",
      url: '/space/12345678',
      dataType: "json",
      data: JSON.stringify([{'space_i': 'test'}]), //JSOn.stringify
      contentType: 'application/json;charset=UTF-8',
      success: function(result) {
        alert(JSON.stringify(result));
      } 
    });
  });
});
