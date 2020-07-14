$(document).ready(function(){
   console.log("loaded"); 
    $(document).on("submit", "#post-form", function(e){
        e.preventDefault();

        var form = $('#post-form').serialize();
        $.ajax({
            url: '/feedsubmit',
            type: 'POST',
            data: form,
            success: function(response){
                console.log(response);
            }
        });
    });

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
});
