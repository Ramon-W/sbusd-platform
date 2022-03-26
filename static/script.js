$(document).ready(function(){
  $(".space").click(function() {
    $.ajax({
    	type: "GET",
     	url: '/space',
     	dataType: "json",
    	data: JSON.stringify([{'space_id': 'test'}]), //JSOn.stringify
    	contentType: 'application/json;charset=UTF-8',
			success: function(result) {
        alert(result);
      } 
    });
  });
});
