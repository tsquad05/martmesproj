$(document).ready(function(){

      
    $('#registerForm').on('submit', function(e) {
        e.preventDefault();
        
        // Disable the button and show loading state
        $('#registerBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating...');
    
        $.ajax({
            type: 'POST',
            url: '/user/sign-up/',  // Update with your register view URL
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    // Registration success
                    window.location.href = '/';
                    // You may want to redirect or update the page content here
                } else {
                    // Registration failure
                    $("#SignUpErrorMessage").text("Registration failed. Please check the email and phone field.");
                    setTimeout(() => {
                        $("#SignUpErrorMessage").text("");
                    }, 5000);
                }
            },
            error: function(error) {
                // Handle error
                
                // Clear the error message
               
            },
            complete: function() {
                // Re-enable the button and restore its original text
                $('#registerBtn').prop('disabled', false).html('Create my account');
            }
        });
    });
    

    // AJAX for login
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();
        
        // Disable the button and show loading state
        $('#loginBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...');
    
        $.ajax({
            type: 'POST',
            url: '/user/sign-in/', 
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {

                    window.location.reload()
                } else {
                    // Login failure
                    $("#LoginErrorMessage").text(response.message);
                    setTimeout(() => {
                        $("#LoginErrorMessage").text("");
                    }, 4000);
                }
            },
            error: function(error) {
                // Handle error
                console.log(error.responseText);
                
            },
            complete: function() {
                // Re-enable the button and restore its original text
                $('#loginBtn').prop('disabled', false).html('Login');
            }
        });
    });
    $('#ForgotPasswordForm').on('submit', function(e) {
        e.preventDefault();
        
        // Disable the button and show loading state
        $('#ForgotPasswordBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...');
    
        $.ajax({
            type: 'POST',
            url: '/user/send-password-reset-email/',  
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    $('.dissapear-content').html("")
                    $('#passwordCheckmark').html('<div style="display: flex; align-items: center; justify-content: center;"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 12L9 18L21 6" stroke="rgba(0,0,0,0.95)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg></div>')
                    $('#passwordMessage').html('<p>An email has been sent to your account to reset your password.</p>')
                    
                } else {
                   
                    $("#ForgotPasswordErrorMessage").text(response.message);
                    setTimeout(() => {
                        $("#ForgotPasswordErrorMessage").text("");
                    }, 4000);
                }
            },
            error: function(error) {
               
                console.log(error.responseText);
                
            },
            complete: function() {
              
                $('#ForgotPasswordBtn').prop('disabled', false).html('Login');
            }
        });
    });

})

$(document).ready(function() {
    
    // Function to get CSRF token from cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    $('.btn-get-wishlist').click(function() {
        let productId = $(this).attr('data-product-item');
        let this_val = $(this);
    
        $.ajax({
            url: '/add-to-wishlist/',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: { id: productId }, // Corrected data format
            dataType: 'json',
            beforeSend: function(){
                this_val.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
            },
            success: function(data) {
                if (data.bool === true) {
                    this_val.html('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.4454 20.7608L3.57617 12.5663C1.35964 10.2582 1.49922 6.4736 3.87922 4.34929C6.24035 2.24181 9.82044 2.65105 11.6863 5.24171L12 5.67724L12.3137 5.24171C14.1796 2.65105 17.7596 2.24181 20.1208 4.34929C22.5008 6.4736 22.6404 10.2582 20.4238 12.5663L12.5546 20.7608C12.2483 21.0797 11.7517 21.0797 11.4454 20.7608Z" stroke="rgba(0,0,0,0.95)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>');
                } else {
                    
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.error('Error:', errorThrown);
            }
        });
    });
    $('.btn-delete-wishlist').click(function() {
        let productId = $(this).attr('data-product-item');
        let this_val = $(this);
        
        $.ajax({
            url: '/delete-from-wishlist/',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: { id: productId }, // Corrected data format
            dataType: 'json',
            beforeSend: function(){
                this_val.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
            },
            success: function(data) {
                if (data.success) {
                    this_val.closest('#content-delete').remove();
                } else {
                    this_val.html('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16 8L12 12M12 12L8 16M12 12L8 8M12 12L16 16" stroke="rgba(0,0,0,0.95)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><circle cx="12" cy="12" r="10" stroke="rgba(0,0,0,0.95)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></circle></svg>');
                    
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.error('Error:', errorThrown);
            }
        });
    });
    

});





