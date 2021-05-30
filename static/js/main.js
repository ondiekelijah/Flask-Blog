const $dropdown = $(".dropdown");
const $dropdownToggle = $(".dropdown-toggle");
const $dropdownMenu = $(".dropdown-menu");
const showClass = "show";

$(window).on("load resize", function () {
  if (this.matchMedia("(min-width: 768px)").matches) {
    $dropdown.hover(
      function () {
        const $this = $(this);
        $this.addClass(showClass);
        $this.find($dropdownToggle).attr("aria-expanded", "true");
        $this.find($dropdownMenu).addClass(showClass);
      },
      function () {
        const $this = $(this);
        $this.removeClass(showClass);
        $this.find($dropdownToggle).attr("aria-expanded", "false");
        $this.find($dropdownMenu).removeClass(showClass);
      }
    );
  } else {
    $dropdown.off("mouseenter mouseleave");
  }
});

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

// cookie banner
const cookieContainer = document.querySelector(".cookie-container");
const cookieButton = document.querySelector(".cookie-btn");


cookieButton.addEventListener("click", () => {
  cookieContainer.classList.remove("active");
  // localStorage.setItem("cookieBannerDisplayed", "true");
});

setTimeout(() => {
  // if (!localStorage.getItem("cookieBannerDisplayed"))
  cookieContainer.classList.add("active");
}, 2000);

// Newsletter popup
const newsPopup = document.querySelector(".newsletter");
const close = document.querySelector(".close");
const dismiss = document.querySelector(".newsletter-cta");
const email = document.querySelector(".newsletter-email");


// show using step 1

window.addEventListener("load", () => {
  setTimeout(() => {
    // if (!localStorage.getItem("alreadySubscribed"))
    newsPopup.classList.add("show")
  }, 800);

  dismiss.addEventListener("click", () => {
    if (email && email.value) {
      swal({
        title: "Welcome Home!",
        text: "You are one of us!",
        icon: "success",
        button: "Close",
      });
      // localStorage.setItem("alreadySubscribed", "true");

      setTimeout(() => {
        newsPopup.classList.remove("show")
      }, 5000);
    }
    else {
      swal({
        title: "Did you forget your email?",
        text: "Please re-enter your email!",
        icon: "warning",
        button: true,
        popup: 'format-pre'
      });
    }

    // setTimeout(() => {
    //   newsPopup.classList.remove("show")
    // }, 5000);
  });

});

// show using step 2

// window.addEventListener("load", () => {
//     showPopup();
// });
// function showPopup() {
//     const timeLimit = 5 // seconds;
//     let i = 0;
//     const timer = setInterval(() => {
//         i++;
//         if (i == timeLimit) {
//             clearInterval(timer);
//             newsPopup.classList.add("show")
//         }
//         console.log(i)
//     }, 1000);
// };

close.addEventListener("click", () => {
  newsPopup.classList.remove("show")
});

// hide and show comment-reply form on click

// function showForm() {
//   var  reply_frm = document.getElementByClassName("comment-replies-section");


//   // if (reply_frm.style.display === "none") {
//   //   reply_frm.style.display = "block";
//   // } else {
//   //   reply_frm.style.display = "none";
//   // }
//   alert('reply_frm');
// }
$('.majorpoints').click(function(){
  $(this).find('.hiders').show();
});

// Reload comments automatically
// $(document).ready( function() {
//   $('#comment-post').click(function() {
//      $.ajax("{{ url_for('blog.article') }}").done(function (reply) {
//         $('#comments-main-section').html(reply);
//      });
//   });
// });
