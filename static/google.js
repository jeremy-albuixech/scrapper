function submitGoogleConfig() {
    if(document.getElementById("androidid").value) {
        localStorage.setItem('androidid', document.getElementById("androidid").value);
        document.getElementById("androidconfig").submit();
    }    
}
function logout(){
    if(localStorage.getItem('androidid')) { 
        localStorage.removeItem('androidid');   
        document.getElementById("googlelogout").submit();  
    }
}
if(localStorage.getItem('androidid')) {
    document.getElementById("androidid").value = localStorage.getItem('androidid');
}