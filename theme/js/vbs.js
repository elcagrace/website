if (!$('#vbs-name')[0].checkValidity) {
  $('#enroll').on('click', () => {
    if ($('input:invalid').length > 0) {
      $('input:valid').css('box-shadow', 'none');
      $('input:invalid').css('box-shadow', '0px 0px 3px #f00');
      alert('Some fields are incomplete or contain data in the wrong format.');
      return false;
    }
  });
}
