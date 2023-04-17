$(function(){
        $("#shop-action").on('click',"#wishlist-add",function(){
            let id = $(this).attr("data-id");
            let url = $(this).data("action");
          
           
            if(confirm("Are you sure?")){
                 
                
                 $.ajax({
                     url: url,
                    
                    type:"POST",
                    dataType:"json",
                    data:{
                        id:id,
                        
                    },
                    headers:{
                        "X-Requested-With" :"XMLHttpRequest",
                        "X-CSRFToken" : getCookie("csrftoken"),

                    },
                     xhrFields: {
                        withCredentials: true
                       },
                    success: function(data){
                      
                       alert("Product was added successfully.")
                          
                    },
                    error: function(data){
                        alert("We have encountered an error.");
                    }



                 });

            }
        });
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

