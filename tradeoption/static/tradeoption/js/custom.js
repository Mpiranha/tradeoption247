/* ========================================================================= */
/*	Preloader
/* ========================================================================= */

// $(window).load(function(){

// 	$("#preloader").fadeOut("slow");
var isInViewport = function (elem) {
    var bounding = elem.get(0).getBoundingClientRect();
    return (
        bounding.top >= 0 &&
        bounding.left >= 0 &&
        bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
};
// });
   //-- Plugin implementation
   (function($) {
    $.fn.countTo = function(options) {
      return this.each(function() {
        //-- Arrange
        var FRAME_RATE = 60; // Predefine default frame rate to be 60fps
        var $el = $(this);
        var countFrom = parseInt($el.attr('data-count-from'));
        var countTo = parseInt($el.attr('data-count-to'));
        var countSpeed = $el.attr('data-count-speed'); // Number increment per second
  
        //-- Action
        var rafId;
        var increment;
        var currentCount = countFrom;
        var countAction = function() {              // Self looping local function via requestAnimationFrame
          if(currentCount < countTo) {              // Perform number incremeant
            $el.text(Math.floor(currentCount));     // Update HTML display
            increment = countSpeed / FRAME_RATE;    // Calculate increment step
            currentCount += increment;              // Increment counter
            rafId = requestAnimationFrame(countAction);
          } else {                                  // Terminate animation once it reaches the target count number
            $el.text(countTo);                      // Set to the final value before everything stops
            //cancelAnimationFrame(rafId);
          }
        };
        rafId = requestAnimationFrame(countAction); // Initiates the looping function
      });
    };
  }(jQuery));
  
  //-- Executing
  document.addEventListener('scroll', function() {
    if (isInViewport($('.parallax-overlay'))) {
        $('.number-counter').countTo();
        }
  })

 

$(document).ready(function(){

	/* ========================================================================= */
	/*	Menu item highlighting
    /* ========================================================================= */
    
 

	$('#nav').singlePageNav({
		offset: $('#nav').outerHeight(),
		filter: ':not(.external)',
		speed: 1200,
		currentClass: 'current',
		easing: 'easeInOutExpo',
		updateHash: true,
		beforeStart: function() {
			console.log('begin scrolling');
		},
		onComplete: function() {
			console.log('done scrolling');
		}
	});
	
    $(window).scroll(function () {
        if ($(window).scrollTop() > 400) {
            $("#navigation").css("background-color","#0EB493");
        } else {
            $("#navigation").css("background-color","rgba(16, 22, 54, 0.2)");
        }
    });
	
	/* ========================================================================= */
	/*	Fix Slider Height
	/* ========================================================================= */	

	var slideHeight = $(window).height();
	
	$('#slider, .carousel.slide, .carousel-inner, .carousel-inner .item').css('height',slideHeight);

	$(window).resize(function(){'use strict',
		$('#slider, .carousel.slide, .carousel-inner, .carousel-inner .item').css('height',slideHeight);
	});
	
	
	/* ========================================================================= */
	/*	Portfolio Filtering
	/* ========================================================================= */	
	
	
    // portfolio filtering

    $(".project-wrapper").mixItUp();
	
	
	$(".fancybox").fancybox({
		padding: 0,

		openEffect : 'elastic',
		openSpeed  : 650,

		closeEffect : 'elastic',
		closeSpeed  : 550,

		closeClick : true,
	});
	
	/* ========================================================================= */
	/*	Parallax
	/* ========================================================================= */	
	
	//$('#facts').parallax("50%", 0.3);
	
	/* ========================================================================= */
	/*	Timer count
	/* ========================================================================= */

	"use strict";
    $(".number-counters").appear(function () {
        $(".number-counters [data-to]").each(function () {
            var e = $(this).attr("data-to");
            $(this).delay(6e3).countTo({
                from: 50,
                to: e,
                speed: 3e3,
                refreshInterval: 50
            })
        })
    });
	
	/* ========================================================================= */
	/*	Back to Top
	/* ========================================================================= */
	
	
    $(window).scroll(function () {
        if ($(window).scrollTop() > 400) {
            $("#back-top").fadeIn(200)
        } else {
            $("#back-top").fadeOut(200)
        }
    });
    $("#back-top").click(function () {
        $("html, body").stop().animate({
            scrollTop: 0
        }, 1500, "easeInOutExpo")
    });
	
});


// ==========  START GOOGLE MAP ========== //
function initialize() {
    var myLatLng = new google.maps.LatLng(22.402789, 91.822156);

    var mapOptions = {
        zoom: 14,
        center: myLatLng,
        disableDefaultUI: true,
        scrollwheel: false,
        navigationControl: false,
        mapTypeControl: false,
        scaleControl: false,
        draggable: false,
        mapTypeControlOptions: {
            mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'roadatlas']
        }
    };

    var map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);


    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        icon: 'img/location-icon.png',
        title: '',
    });

}

google.maps.event.addDomListener(window, "load", initialize);
// ========== END GOOGLE MAP ========== //

