// pls não me violem, eu fiz o melhor que podia, não entendo nada de JS
function do_table_work(title) {
   if (title === 'All') {
      var elements = document.getElementsByClassName('table-dD95W')
      var oo = document.getElementsByClassName("command-1Ek3-");
      for (var i = 0; i < elements.length; i++) {
         elements[i].style.display = 'block';
         oo[i].style.display = 'block';
      }
   } else {
      var elements = document.getElementsByClassName('table-dD95W')
      for (var i = 0; i < elements.length; i++) {
         if (elements[i].style.display === 'none') {
            if (elements[i].id === title) {
               elements[i].style.display = 'block';
            }
         } else {
            if (elements[i].id === title) {
               continue
            }
         elements[i].style.display = 'none';
         }
      }
   }
}

window.onload = function() {
   var header = document.getElementById("sideNavChoose");
   var btns = header.getElementsByClassName("btn"); 

   for (var i = 0; i < btns.length; i++) {
      btns[i].addEventListener("click", function() {
      var current = document.getElementsByClassName("active-4svGK");
      if (current.length > 0) { 
         current[0].className = current[0].className.replace(" active-4svGK", "");
      }
      this.className += " active-4svGK";
      });
   }
}