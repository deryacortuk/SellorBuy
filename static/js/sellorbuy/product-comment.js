$(document).on('submit', '#aa-review-form',function(e){
    e.preventDefault();
    let id = $(this).data("id");
    let url = $(this).attr("action");
    let rating = $(this).find('#rating').children(".a-rating").data("value"); 
    console.log(rating);
    
   
   
    let content = $(this).children('#form-comment').find("#message").val();
   
    $.ajax({
        url : url,
        type: 'POST',
           headers:{
                        "X-Requested-With" :"XMLHttpRequest",
                        "X-CSRFToken" : getCookie("csrftoken"),

                    },
                     xhrFields: {
                        withCredentials: true
                       },
                
        data:{
            id : id,               
            rating:rating,
            content:content,
            

        },
        success: function(json){
          
  alert("Your comment was added successfully");
           window.location.reload();
           
        },
        error: function(xhr, errmsg, err){
            
        }


    })
});
   function getCookie(name){
       let cookieValue = null;
       if(document.cookie && document.cookie !==""){
           const cookies = document.cookie.split(";");
           for(let i = 0;cookies.length; i++){
               const cookie = cookies[i].trim();
               if(cookie.substring(0,name.length +1)===(name + "=")){
                   cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                   break;
               }
           }
       }
       return cookieValue;
   }