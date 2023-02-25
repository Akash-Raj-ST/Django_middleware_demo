function basicfunction(){
    document.getElementById("amt").defaultValue = "0";
}
document.getElementById("submit").addEventListener("click", function(event){
    event.preventDefault();
    var e = document.getElementById("users");
    var user = e.options[e.selectedIndex].text;
    var amt=document.getElementById("amt").value
    alert(user)
    if(user=='-- select user --'){
        document.getElementById("select_optn").style.display="block";
    }
    if(user!='-- select user --'){
        document.getElementById("select_optn").style.display="none";
    }
    if(amt=="0"){
        document.getElementById("amt_value").style.display="block";
    }
    if(amt!="0"){
        document.getElementById("amt_value").style.display="none";
    }
    var payment = document.getElementsByName('bank');
    var pay_meth="";
    for(var i = 0; i < payment.length; i++){
        if(payment[i].checked){
            pay_meth = payment[i].value;
        }
    } 
    if(pay_meth==""){
        document.getElementById("payment_method").style.display="block";
        
    }
    if(pay_meth!=""){
        document.getElementById("payment_method").style.display="none";
    }
});