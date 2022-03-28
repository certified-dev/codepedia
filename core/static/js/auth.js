var username = $('#auth_form input[type="text"]');
var password = $('#auth_form input[name="password"]');
var repass = $('#auth_form input[name="password2"]');
var email = $('#auth_form input[type="email"]');

var user_bool = false;
var pass_bool = false;
var email_bool = false;
var repass_bool = false;

$(username).keyup(function(e) {

  if ($(this).val().length > 3) {

    $(this).removeClass("is-invalid");
    $(this).addClass("is-valid");

    user_bool = true;

  } else {

    $(this).addClass("is-invalid");
    $(this).removeClass("is-valid");

    user_bool = false;

  }

});

$(email).keyup(function(e) {

  if ($(this).val().length > 5) {

    $(this).removeClass("is-invalid");
    $(this).addClass("is-valid");

    email_bool = true;

  } else {

    $(this).addClass("is-invalid");
    $(this).removeClass("is-valid");

    email_bool = false;

  }

});

$(password).keyup(function(e) {

  if ($(this).val().length > 5) {

    $(this).removeClass("is-invalid");
    $(this).addClass("is-valid");

    pass_bool = true;

  } else {

    $(this).addClass("is-invalid");
    $(this).removeClass("is-valid");

    pass_bool = false;

  }

});


$(repass).keyup(function(e) {

  if (password.val() === $(this).val()) {

      $(this).removeClass("is-invalid");
      $(this).addClass("is-valid");

      repass_bool = true;

  } else {

      $(this).addClass("is-invalid");
      $(this).removeClass("is-valid");

      repass_bool = false;

  }

});


function checkForm(e) {

  var form = $('#auth_form');

  if ( repass_bool ) {

    if (username && email && password && repass) {
      $('#auth_form').submit();

      $.ajax({
        url: form.attr('data-validate-username-url'),
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
          if (data.username_unavailable && !data.email_unavailable) {

            alert('user already exists!!!');
            $('#reg_error_username').show();

          } else if (data.email_unavailable && !data.username_unavailable) {

            alert('user with email already exists!!!');
            $('#reg_error_email').show();

          } else if (data.username_unavailable && data.email_unavailable) {

            alert('user with username and email already exists!!!');
            $('#reg_error').show();

          } else {

            $('#auth_form').submit();

          }
        }
      });
      
    } else {

      alert('enter your username/email and password');
      
    }

  } else {

    if ( user_bool && pass_bool ) {

      $('#auth_form').submit();

    } else if(!user_bool && !pass_bool) {

      alert('check your username and password');

    } else if(!user_bool | !pass_bool) {

      alert('check your username/password');
    }

  } 

}



