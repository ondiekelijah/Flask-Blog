window.onscroll = function () { scrollFunction() };

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("main").style.background = "rgba(0, 0, 0, 0.9)";
    document.getElementById("main").style.transition= "all 2s";
    document.getElementById("main").style.padding= "3px";    
  } else {
    document.getElementById("main").style.background = "";
    document.getElementById("main").style.transition= "";
    document.getElementById("main").style.padding= "12px";
  }
}
// --------------------------------------------------------------------------
$(function () {
  $(document).scroll(function () {
    var $nav = $(".navbar-fixed-top");
    $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
  });
});
// --------------------------------------------------------------------------

$(document).ready(function() {
  $('.carousel').carousel({
    interval: 5000
  })
});
// ---------------------------------------------------------------------------

// --------------------------------------------------------------------------

/*Scroll to top when arrow up clicked BEGIN*/
$(window).scroll(function () {
  var height = $(window).scrollTop();
  if (height > 100) {
    $('#back2Top').fadeIn();
  } else {
    $('#back2Top').fadeOut();
  }
});
$(document).ready(function () {
  $("#back2Top").click(function (event) {
    event.preventDefault();
    $("html, body").animate({ scrollTop: 0 }, "slow");
    return false;
  });

});
// --------------------------------------------------------------------------

//With a function, I am able to perform multiple tasks 
function SwitchButtons(buttonId) {
  var hideBtn, showBtn, menuToggle;
  if (buttonId == 'button1') {
    menuToggle = 'menu2';
    showBtn = 'button2';
    hideBtn = 'button1';
  }
  //  else {
  //   menuToggle = 'menu3';
  //   showBtn = 'button1';
  //   hideBtn = 'button2';
  // }
  //I don't have your menus, so this is commented out.  just uncomment for your usage
  // document.getElementById(menuToggle).toggle(); //step 1: toggle menu
  document.getElementById(hideBtn).style.display = 'none'; //step 2 :additional feature hide button
  document.getElementById(showBtn).style.display = ''; //step 3:additional feature show button
}
// --------------------------------------------------------------------------
function myFunction() {
  var x = document.getElementById("demo");
  if (x.className.indexOf("w3-show") == -1) {
      x.className += " w3-show";
  } else { 
      x.className = x.className.replace(" w3-show", "");
  }
}
// --------------------------------------------------------------------------
$(document).ready(function(){
  $(".button a").click(function(){
      $(".overlay").fadeToggle(200);
     $(this).toggleClass('btn-open').toggleClass('btn-close');
  });
});
$('.overlay').on('click', function(){
  $(".overlay").fadeToggle(200);   
  $(".button a").toggleClass('btn-open').toggleClass('btn-close');
  open = false;
});
