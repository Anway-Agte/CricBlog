
$(document).ready(function(){
    $("#like").click(function(){
        var Url = "{{url_for('like-unlike' , post_id = '{{ post['_id'] }} ') }}" ; 
        $.ajax({

            url : Url , 
            type : "post" , 
            success : function(result){
                alert("Wuhu") ; 
            } ,
            error : function(result){
                alert("ono") ; 
            }
        }) ;
    })

}) ; 

