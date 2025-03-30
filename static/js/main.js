/*======================
========================*/

(function ($) {
  "use strict";

  /*========== Preloader ==========*/
  $(window).on("load", () => {
    $("#preloader").fadeOut(500);
  });

  $(document).ready(function ($) {
    /*========= sticky menu ==========*/
    $(window).scroll(function () {
      try {
        var window_top = $(window).scrollTop() + 1;
        var header = $(".header");
        if (window_top > 200) {
          header.addClass("header_fixed animate__animated animate__fadeIn");
        } else {
          header.removeClass("header_fixed animate__animated animate__fadeIn");
        }
      } catch (error) {
        console.error("An error occurred while handling scroll:", error);
      }
    });

    /*========= sticky menu two ==========*/
    $(window).scroll(function () {
      try {
        var window_top = $(window).scrollTop() + 1;
        var header = $(".PrimaryMenu");
        if (window_top > 200) {
          header.addClass("menu_fixed animate__animated animate__fadeIn");
        } else {
          header.removeClass("menu_fixed animate__animated animate__fadeIn");
        }
      } catch (error) {
        console.error("An error occurred while handling scroll:", error);
      }
    });

    /*========= sticky menu three ==========*/
    $(window).scroll(function () {
      try {
        var window_top = $(window).scrollTop() + 1;
        var header = $(".PrimaryMenu");
        if (window_top > 200) {
          header.addClass("menu_fixed animate__animated animate__fadeIn");
          header.removeClass("transparent");
        } else {
          header.removeClass("menu_fixed animate__animated animate__fadeIn");
        }
      } catch (error) {
        console.error("An error occurred while handling scroll:", error);
      }
    });




    /*========= Modal Video ==========*/
    try {
      $(".video-play .yt__play").modalVideo({
        channel: "youtube",
      });
    } catch (error) {
      console.log("Modal Video Not Loded");
    }
    // video slider
    try {
      $(".yt__play").modalVideo({
        channel: "youtube",
      });
    } catch (error) {
      console.log("Modal Video Not Loded");
    }

    /*========= Magic Kursor Js ==========*/
    try {
      new kursor({
        type: 1,
        color: "#fff",
      });
    } catch (error) {
      console.log("Kursor not enable this page");
    }

    /*========= Nice Select js ==========*/
    try {
      $("select").niceSelect();
    } catch (error) {
      console.log("Nice select not enable this page");
    }

    /*============= Wow Js =============*/
    
    // mobile device animation off.
    const scrollAnimations = sal();
    function isMobileDevice() {
      return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    if (isMobileDevice()) {
      scrollAnimations.disable();
    }

    try {
      sal({
        threshold: 1,
        once: false,
      });
    } catch (error) {
      console.log("Sal js not enable this page");
    }

    /*============ offcanvase Menu =========*/
    try {
      $(".offcanvase__menu--close-icon, .offcanvas__overlay").on(
        "click",
        function () {
          $(".offcanvase").removeClass("info-open");
          $(".offcanvas__overlay").removeClass("overlay-open");
        }
      );
      $(".menu-icon").on("click", function () {
        $(".offcanvase").addClass("info-open");
        $(".offcanvas__overlay").addClass("overlay-open");
      });
    } catch (error) {
      console.log("offcanvase Menu Not loaded");
    }

    /*========= Mobile Menu =========*/
    try {
      $("#offcanvase__menu").meanmenu({
        meanMenuContainer: ".offcanvase-menu",
        meanScreenWidth: "767",
        meanExpand: ["+"],
      });
    } catch (error) {
      console.log("Mobile Menu Not loaded");
    }

    /*============= Header Slider =============*/
    try {
      $(".slider__wrapper").slick({
        autoplay: false,
        dots: true,
        pauseOnHover: false,
        slidesToShow: 1,
        arrows: false,
      });
    } catch (error) {
      console.log("This slider only enable for homepage.");
    }

    /*========== Testimonial Slider ==========*/
    try {
      $(".testimonial-slider").slick({
        autoplay: false,
        dots: true,
        pauseOnHover: false,
        slidesToShow: 1,
        arrows: false,
        responsive: [
          {
            breakpoint: 991,
            settings: {
              dots: false,
            },
          },
        ],
      });
    } catch (error) {
      console.log("This slider is not for this page");
    }
    /*========== Testimonial Slider ==========*/
    try {
      new Swiper(".testimonial .slider", {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        dots: true,
        speed: 1000,
        autoplay: {
          delay: 5000,
          disableOnInteraction: false,
        },
        pagination: {
          el: ".pagination__dots",
          clickable: true,
        },
  
        on: {
          init: function () {
            $(".animated__line").removeClass("animated");
            $(".animated__line").removeClass("active");
            $(".animated__line").eq(0).addClass("animated");
            $(".animated__line").eq(0).addClass("active");
          },
          slideChangeTransitionStart: function () {
            $(".animated__line").removeClass("animated");
            $(".animated__line").removeClass("active");
            $(".animated__line").eq(0).addClass("active");
          },
          slideChangeTransitionEnd: function () {
            $(".animated__line").eq(0).addClass("animated");
          },
        },
      });
    } catch (error) {
      console.log('swiper js not loade')
    }
    
    /*========== sponsor slider home three ==============*/
    new Swiper(".sponsor__slider", {
      slidesPerView: 5,
      spaceBetween: 50,
      loop: true,
      speed: 1000,
      freeMode: true,
      autoplay: {
        delay: 1000,
        disableOnInteraction: false,
      },
      breakpoints: {
        1024: {
          slidesPerView: 5,
        },
        767: {
          slidesPerView: 4,
        },
        575: {
          slidesPerView: 3,
        },
        320: {
          slidesPerView: 2,
        },
      },
    });

    /*============= Blog slider three ============*/
    new Swiper(".blog__slider", {
      slidesPerView: 2,
      loop: true,
      speed: 1000,
      spaceBetween: 30,
      autoplay: {
        delay: 1000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
      },
      navigation: {
        nextEl: ".btn__next-Slider",
        prevEl: ".btn__prev-Slider",
      },
      breakpoints:{
        991:{
          slidesPerView: 2,
        }, 
        767:{
          slidesPerView: 2,
        },
        575:{
          slidesPerView: 1,
        },
        320: {
          slidesPerView: 1,
        }
      }
    });
    
    /*============= Client Testimonial Slider Three ============*/
    new Swiper(".clientTestimonial__slider", {
      slidesPerView: 1,
      loop: true,
      speed: 1000,
      grabCursor: true,
      spaceBetween: 30,
      autoplay: {
        delay: 1000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
      },
      navigation: {
        nextEl: ".btn__next",
        prevEl: ".btn__prev",
      },
    });

    /*========== service Two Slider ==============*/
    new Swiper(".service__slider", {
      slidesPerView: 3,
      spaceBetween: 40,
      loop: true,
      speed: 5000,
      centeredSlides: true,
      autoplay: {
        delay: 2500,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".slider-pagination",
        clickable: true,
      },
      breakpoints: {
        1024: {
          slidesPerView: 3,
        },
        767: {
          slidesPerView: 2,
          centeredSlides: false,
        },
        575: {
          slidesPerView: 1,
        },
        320: {
          slidesPerView: 1,
        },
      },
    });
    /*============= Testimonial slider three ============*/
    new Swiper(".testimonial__slider", {
      slidesPerView: 1,
      loop: true,
      speed: 5000,
      grabCursor: true,
      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
      },
      pagination: {
        el: ".testimonial__dot",
        clickable: true,
      },
    });
    /*============= Client Testimonial Slider Three ============*/
    new Swiper(".clientTestimonial__slider", {
      slidesPerView: 1,
      loop: true,
      speed: 1000,
      grabCursor: true,
      spaceBetween: 30,
      autoplay: {
        delay: 1000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
      },
      navigation: {
        nextEl: ".btn__next",
        prevEl: ".btn__prev",
      },
    });

    /*========== home Three slider ===========*/
    // hero slider
    new Swiper(".heroSlider__active", {
      slidesPerView: 3,
      spaceBetween: 30,
      loop: false,
      speed: 1000,
      autoplay: {
        delay: 1000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
      },
      pagination: {
        el: ".heroSlider__pagination",
        clickable: true,
      },
      breakpoints:{
        991:{
          slidesPerView: 3,
        },
        767:{
          slidesPerView: 2,
        },
        320:{
          slidesPerView: 1,
        }
      }
    });

    /*========== HOME 4 TESTIMONIAL SLIDER ==========*/
    new Swiper(".testimonial__active", {
      slidesPerView: 2,
      spaceBetween: 30,
      loop: false,
      speed: 1000,
      autoplay: {
        delay: 1000,
        disableOnInteraction: false,
      },
      navigation: {
        nextEl: ".btn__next",
        prevEl: ".btn__prev",
      },
      breakpoints:{
        991:{
          slidesPerView: 2,
        },
        767:{
          slidesPerView: 1,
        },
        320:{
          slidesPerView: 1,
        }
      }
    });

     // Team Swiper JS
     var SwiperTraveler = new Swiper(".team-slider", {
      loop: true,
      spaceBetween: 25,
      autoplay: {
          delay: 5000,
          disableOnInteraction: false,
      },
      navigation: {
          nextEl: ".team-button-next",
          prevEl: ".team-button-prev",
      },
      breakpoints: {
          0: {
              slidesPerView: 1
          },
          768: {
              slidesPerView: 2
          },
          992: {
              slidesPerView: 3
          },
          1200: {
              slidesPerView: 4
          },
      }
  });
     // Testimonial Swiper JS
     var SwiperTraveler = new Swiper(".testimonials-slider", {
      loop: true,
      spaceBetween: 25,
      autoplay: {
          delay: 5000,
          disableOnInteraction: false,
      },
      navigation: {
          nextEl: ".testimonial-button-next",
          prevEl: ".testimonial-button-prev",
      },
      breakpoints: {
          0: {
              slidesPerView: 1
          },
          768: {
              slidesPerView: 2
          },
          992: {
              slidesPerView: 2
          },
          1200: {
              slidesPerView: 3
          },
      }
  });
     // Blog Swiper JS
     var SwiperTraveler = new Swiper(".blog-slider", {
      loop: true,
      spaceBetween: 25,
      autoplay: {
          delay: 5000,
          disableOnInteraction: false,
      },
      navigation: {
          nextEl: ".blog-button-next",
          prevEl: ".blog-button-prev",
      },
      breakpoints: {
          0: {
              slidesPerView: 1
          },
          768: {
              slidesPerView: 2
          },
          992: {
              slidesPerView: 3
          },
          1200: {
              slidesPerView: 3
          },
      }
  });
     // Team Swiper JS
     var SwiperTraveler = new Swiper(".portfolio-slider", {
      loop: true,
      spaceBetween: 25,
      autoplay: {
          delay: 5000,
          disableOnInteraction: false,
      },
      pagination: {
        el: '.swiper-pagination',
        type: 'progressbar',
      },
      on: {
        init: function () {
          $(".animated__line").removeClass("animated");
          $(".animated__line").removeClass("active");
          $(".animated__line").eq(0).addClass("animated");
          $(".animated__line").eq(0).addClass("active");
        },
        slideChangeTransitionStart: function () {
          $(".animated__line").removeClass("animated");
          $(".animated__line").removeClass("active");
          $(".animated__line").eq(0).addClass("active");
        },
        slideChangeTransitionEnd: function () {
          $(".animated__line").eq(0).addClass("animated");
        },
      },
      breakpoints: {
          0: {
              slidesPerView: 1
          },
          768: {
              slidesPerView: 2
          },
          992: {
              slidesPerView: 3
          },
          1200: {
              slidesPerView: 4
          },
      }
  });


    /*========== product slider ========*/
    try {
      $(".slider-for").slick({
        autoplay: false,
        dots: false,
        pauseOnHover: false,
        slidesToShow: 1,
        arrows: true,
      });
      $(".slider-for").slickLightbox({
        src: "src",
        itemSelector: ".pd-main-image img",
        background: "rgba(0, 0, 0, .7)",
      });
    } catch (error) {
      console.log("product slider not enable this page");
    }

    /*======= Popular Post Slider =========*/
    try {
      $(".popular-slider").slick({
        autoplay: false,
        dots: true,
        pauseOnHover: false,
        slidesToShow: 1,
        arrows: false,
      });
    } catch (error) {
      console.log("popular slider not enable this page");
    }


    /*========= progress bar =======*/
    try {
      const progressBars = document.querySelectorAll(".progress-bar");
      progressBars.forEach((progressBar) => {
        const ariaValuenow = progressBar.getAttribute("aria-valuenow");
        progressBar.style.width = `${ariaValuenow}%`;
      });
    } catch (error) {
      console.log("progress bar not enable this page");
    }
  });

  /*============ accordion style ======== */
  document.addEventListener("DOMContentLoaded", function () {
    var accordionHeaders = document.querySelectorAll(".accordion-header");
    accordionHeaders.forEach(function (header, index) {
      header.addEventListener("click", function () {
        var accordionItems = document.querySelectorAll(".accordion-item");
        accordionItems.forEach(function (item) {
          item.classList.remove("active");
        });
        var clickedItem = document.querySelectorAll(".accordion-item")[index];
        clickedItem.classList.add("active");
      });
    });
  });

  /*=========== Tab Js ===========*/
  try {
    $(".tab__button").click(function () {
      const tabId = $(this).data("tab");
      $(".tab__button").removeClass("active");
      $(this).addClass("active");
      $(".tab__content").removeClass("open").hide();
      $("#" + tabId)
        .addClass("open")
        .show();
    });
    $('.tab__button[data-tab="tab1"]').click();
  } catch (error) {
    console.error("Tab Button not enable this page", error);
  }

  /*======== Price Range =========*/
  try {
    function updateValues() {
      var rangeValue = $("#priceRange").val();
      $(".value-left").text("0");
      $(".value-right").text("$" + rangeValue);
    }
    $("#priceRange").on("input", function () {
      updateValues();
    });
    updateValues();
  } catch (error) {
    console.log("Range Only Enable for Product page");
  }

  /*======== Delete Cart item =========*/
  try {
    function handleDeleteClick(event) {
      const row = event.target.closest("tr");
      if (row) {
        row.remove();
      }
    }
    const deleteIcons = document.querySelectorAll(".cart__delete");
    deleteIcons.forEach((icon) => {
      icon.addEventListener("click", handleDeleteClick);
    });
  } catch (error) {
    console.log("Table Delete only enable for cart Page");
  }

  /*==============mixitup filtering ==============*/
  try {
    var mixer = mixitup(".filter-list");
  } catch (error) {
    console.log("Mixitup Plugin Not Working");
  }

  /*========== Button scroll up js ===========*/
  var scrollPath = document.querySelector(".scroll path");
  var pathLength = scrollPath.getTotalLength();
  scrollPath.style.transition = scrollPath.style.WebkitTransition = "none";
  scrollPath.style.strokeDasharray = pathLength + " " + pathLength;
  scrollPath.style.strokeDashoffset = pathLength;
  scrollPath.getBoundingClientRect();
  scrollPath.style.transition = scrollPath.style.WebkitTransition =
    "stroke-dashoffset 10ms linear";
  var updatescroll = function () {
    var scroll = $(window).scrollTop();
    var height = $(document).height() - $(window).height();
    var scroll = pathLength - (scroll * pathLength) / height;
    scrollPath.style.strokeDashoffset = scroll;
  };
  updatescroll();
  $(window).scroll(updatescroll);
  var offset = 50;
  var duration = 950;
  jQuery(window).on("scroll", function () {
    if (jQuery(this).scrollTop() > offset) {
      jQuery(".scroll").addClass("active-scroll");
    } else {
      jQuery(".scroll").removeClass("active-scroll");
    }
  });
  jQuery(".scroll").on("click", function (event) {
    event.preventDefault();
    jQuery("html, body").animate(
      {
        scrollTop: 0,
      },
      duration
    );
    return false;
  });


  // Home five

  // Home Five Slide JS
  var SwiperTraveler = new Swiper(".home-five-slide", {
    loop: true,
    slidesPerView: 1,
    spaceBetween: 0,
    centeredSlides: true,
    navigation: {
        nextEl: ".home-five-next",
        prevEl: ".home-five-prev",
    },
});

// Designs Slide JS
var SwiperTraveler = new Swiper(".designs-five-slide", {
  loop: true,
  spaceBetween: 25,
  autoplay: {
      delay: 5000,
      disableOnInteraction: false,
  },
  breakpoints: {
      0: {
          slidesPerView: 1
      },
      768: {
          slidesPerView: 2
      },
      992: {
          slidesPerView: 2
      },
      1200: {
          slidesPerView: 3
      },
      1400: {
          slidesPerView: 4
      },
      1600: {
          slidesPerView: 5
      },
  }
});
})(jQuery);
