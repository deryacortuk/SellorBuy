function deletecomment(id){
   var url = $('#delete-comment').data('action');
    $.ajax({
        type: 'POST',
        url : url,
        data:{
            nodeid: id,
            action: 'delete',

        },
        headers:{
                        "X-Requested-With" :"XMLHttpRequest",
                        "X-CSRFToken" : getCookie("csrftoken"),

                    },
                     xhrFields: {
                        withCredentials: true
                       },
                       success: function(data){
                          alert("Your comment was deleted successfully");
                             $('#product-comment'+id).remove();
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