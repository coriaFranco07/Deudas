function listarMarcas(){
    
    $.ajax({
        url:"/marca/",
        type: "get",
        dataType:'json',
        success: function(response){
            console.log(response)
        },
        error: function(error){
            console.log(error)
        }
    })
}

$(document).ready(function(){
    listarMarcas()
})