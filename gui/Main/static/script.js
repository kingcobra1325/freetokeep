// CREATED BY JOHN EARL COBAR

function gameref(){
  $.ajax({
    type: "POST",
    url: '/_refresh',
    success: function(response) {
      $("#gamelist").html(response.refresh);
    }
  });
}
$(document).ready(function() {
  gameref();
  setInterval(gameref, 60000);
  $("#EmailRegisterID").click(function(e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: '/_register',
    data: {email: $("#EmailRegisterIDValue").val()},
    beforeSend: function() {
      $("#EmailRegisterID").prop('disabled', true);
      $("#EmailRegisterClose").prop('disabled', true);
      $("#EmailRegisterIDValue").prop('disabled', true);
      $("#EmailRegisterIDLoader").attr('style','display:block;width:30%;');
      $("#EmailRegisterID").attr('style','display:none;width:30%;');
  },
    success: function(result) {
      $("#result").attr('style','display:block;');
      $("#result").text(result.message);
      $("#result").attr('class',result.alert);
      $('#EmailRegister').modal('hide');
      $("#EmailRegisterID").prop('disabled', false);
      $("#EmailRegisterClose").prop('disabled', false);
      $("#EmailRegisterIDValue").prop('disabled', false);
      $("#EmailRegisterIDValue").val('');
      $("#EmailRegisterIDLoader").attr('style','display:none;width:30%;');
      $("#EmailRegisterID").attr('style','display:block;width:30%;');
      $('#result').delay(3000).fadeOut('fast');
    }
  });
});
$("#EmailDeleteID").click(function(e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: '/_delete',
    data: {email: $("#EmailDeleteIDValue").val()},
    beforeSend: function() {
      $("#EmailDeleteID").prop('disabled', true);
      $("#EmailDeleteClose").prop('disabled', true);
      $("#EmailDeleteIDValue").prop('disabled', true);
      $("#EmailDeleteIDLoader").attr('style','display:block;width:30%;');
      $("#EmailDeleteID").attr('style','display:none;width:30%;');
  },
    success: function(result) {
      $("#result").attr('style','display:block;');
      $("#result").text(result.message);
      $("#result").attr('class',result.alert);
      $('#EmailDelete').modal('hide');
      $("#EmailDeleteID").prop('disabled', false);
      $("#EmailDeleteClose").prop('disabled', false);
      $("#EmailDeleteIDValue").prop('disabled', false);
      $("#EmailDeleteIDValue").val('');
      $("#EmailDeleteIDLoader").attr('style','display:none;width:30%;');
      $("#EmailDeleteID").attr('style','display:block;width:30%;');
      $('#result').delay(3000).fadeOut('fast');
    }
  });
});
});
