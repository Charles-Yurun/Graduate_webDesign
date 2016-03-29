/**
 * Created by simi on 15/7/29.
 */
$(document).ready(function(){
    $('.delete').click(function(){
        if(confirm('确定要删除吗?')){
            return true;
        }else{
            return false;
        }
    });
});