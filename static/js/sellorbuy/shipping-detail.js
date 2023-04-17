$(document).on('submit',"#track-shipping", function(e){
    e.preventDefault();
    let url = $(this).attr("action");        
    let carriername = $("#carriername").val();
    let carriercode = $("#carriercode").val();
    let trackingnumber = $("#trackingnumber").val();
    let eventid = $("#eventid").val();
    
    

    $.ajax({
  url:url,
  type:'POST',
   headers:{
                        "X-Requested-With" :"XMLHttpRequest",
                        "X-CSRFToken" : getCookie("csrftoken"),

                    },
                     xhrFields: {
                        withCredentials: true
                       },

  data:{
    
  carriername:carriername,
        carriercode:carriercode,
        trackingnumber:trackingnumber,
        eventid:eventid
  },
  success:function(data){
 $('#shippinginformation').load(' #shippinginformation', function(){$(this).children().unwrap()});
  $('#collapseThree').load(' #collapseThree', function(){$(this).children().unwrap()}); 
  },
  error:function(xhr, errmsg, err){
            
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
