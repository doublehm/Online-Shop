$(document).ready(function(){
   console.log("loaded"); 
   
    $(document).on("submit", ".registeration-form", function(e){
        e.preventDefault();
        console.log("scripty works")

        var form = $('.registeration-form').serialize();
        $.ajax({
            url: '/postregisteration',
            type: 'POST',
            data: form,
            success: function(response){
                if(response == "error"){
                    alert("this E-mail is already taken!")
                }else{
                    console.log('new user has registered')
                    alert('congratulations! you have registered seccessfully!')
                    window.location.href = '/login'
                }
            }
        });
    });

    $(document).on('submit', '.login-form', function(e){
        e.preventDefault();

        var form = $('.login-form').serialize();
        $.ajax({
            url: '/checklogin',
            type: 'POST',
            data: form,
            success: function(response){
                if(response == "error"){
                    alert("could not log in")
                }else{
                    console.log("loged in as", response)
                    window.location.href = '/'
                }
            }
        });
    });

    $(document).on('click', '#logout-link', function(e){
        e.preventDefault();

        $.ajax({
            url: '/logout',
            type: 'GET',
            success: function(response){
                if(response == 'success'){
                    window.location.href = '/'
                }else{
                    alert("something went wrong!")
                }
            }
        });
    });

    $(document).on('submit', '#post-form', function(e){
        e.preventDefault();
       console.log('posting content...') 
        var form = $('#post-form')[0];
        var formData = new FormData(form);
        $.ajax({
            url: '/submitposts',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response){
                console.log(response);
                window.location.href = '/controlpanel' 
            }
        });
    });

    $(document).on('submit', '#new-product', function(e){
        e.preventDefault();
        console.log("new product releasing")
        var form = $('#new-product')[0];
        var formData = new FormData(form);
        $.ajax({
            url: '/submitnewproduct',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response){
                window.location.href = '/controlpanel'
                console.log(response);
            }
        });
    });

    $(document).on('submit', '#comment-form', function(e){
        e.preventDefault();
        var form = $('#comment-form').serialize();
        $.ajax({
            url: '/submit-comment',
            type: 'POST',
            data: form,
            success: function(response){
                if(response == "success"){
                    window.location.href = window.location.href;
                    console.log(response);
                }else if(response == "error"){
                    alert("you have to login to send comments");
                    window.location.href = "/login";
                }else{
                    alert("something went wrong!");
                }
            }
        });
    });

    $(document).on('submit', '.contact-us', function(e){
        e.preventDefault();
        var form = $(this).serialize();
        $.ajax({
            url: '/contact-request',
            type: 'POST',
            data: form,
            success: function(response){
                console.log(response);
            }
        });
    });

    $(document).on('submit', '.profile', function(e){
        e.preventDefault();

        var form = $(this).serialize();
        $.ajax({
            url: '/update-profile',
            type: 'POST',
            data: form,
            success: function(response){
                window.location.href = window.location.href;
                console.log(response);
            }
        })
    });
/*
    $('#productCount1').on('blur', function(e){
        e.preventDefault();
        var value = $(this).val();
        var sum = value * $('#productPrice1').val();
        $('#productTP1').val(sum);
        var total = +sum + +$('#productTP2').val() + +$('#productTP3').val() + +$('#productTP4').val()
        $('#total-value').val(total);
    })
    $('#productCount2').on('blur', function(e){
        e.preventDefault();
        var value = $(this).val();
        var sum = value * $('#productPrice2').val();
        $('#productTP2').val(sum);
        var total = +sum + +$('#productTP1').val() + +$('#productTP3').val() + +$('#productTP4').val()
        $('#total-value').val(total);
    })
    $('#productCount3').on('blur', function(e){
        e.preventDefault();
        var value = $(this).val();
        var sum = value * $('#productPrice3').val();
        $('#productTP3').val(sum);
        var total = +sum + +$('#productTP2').val() + +$('#productTP1').val() + +$('#productTP4').val()
        $('#total-value').val(total);
    })
    $('#productCount4').on('blur', function(e){
        e.preventDefault();
        var value = $(this).val();
        var sum = value * $('#productPrice4').val();
        $('#productTP4').val(sum);
        var total = +sum + +$('#productTP2').val() + +$('#productTP3').val() + +$('#productTP1').val()
        $('#total-value').val(total);
    })
*/

    $('.count').change(function(e){
        e.preventDefault();
        var param = {
            'id': $(this).attr("id"), 
            'count': $(this).val() ,
        };
        $.ajax({
            url: '/price-calculation',
            type: 'POST',
            data: param,
            success: function(response){
                window.location.href = window.location.href;
            }
        })
    })
});

