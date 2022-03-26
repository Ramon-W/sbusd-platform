$(document).ready(function(){
  $(".space").click(function() {
    $.ajax({
    	type : "POST",
     	url : '/space' + '/123456789',
     	dataType: "json",
    	data: JSON.stringify() //(you can put in a variable in here to send data with the request),
    	contentType: 'application/json;charset=UTF-8',
    	success: function (data) {
		console.log(data);
		}
	});
  });
});
