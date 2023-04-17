function changequantity(id){
   var url = $('#quantity').data('action');
   var cartid = $('#quantity').data('id');
   var quantity = $('#quantity').val();
   
    $.ajax({
        type: 'POST',
        url : url,
        data:{
            id: id,
           quantity:quantity,
           cartid:cartid

        },
        headers:{
                        "X-Requested-With" :"XMLHttpRequest",
                        "X-CSRFToken" : getCookie("csrftoken"),

                    },
                     xhrFields: {
                        withCredentials: true
                       },
              success: function(data){
                          alert("Success");
                         location.reload(true);
                            
                       },
                       error : function(xhr, errmsg, err){}
    });
}
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