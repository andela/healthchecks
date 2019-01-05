$(function () {
    
    $("#reports_allowed").click(function() {
        
        if($("#reports_allowed").is(':checked')){
            $(".report_period").prop({ disabled: false });
            $("#monthly_report_period").prop({ checked: true });
        }else{
            $(".report_period").prop({ checked: false, disabled: true  });
        }
        
    });
});