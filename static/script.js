$(document).ready(function(){
  var textarea = document.getElementById("message_input");
  var limit = 200;
  textarea.oninput = function() {
    textarea.style.height = "";
    textarea.style.height = Math.min(textarea.scrollHeight, 300) + "px";
  }; 
  function handleEnter(evt) {
    if (evt.keyCode == 13 && evt.shiftKey) {
        if (evt.type == "keypress") {
            pasteIntoInput(this, "\n");
        }
        evt.preventDefault();
    }
  }
  $("#message_input").keydown(handleEnter).keypress(handleEnter);
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
});
