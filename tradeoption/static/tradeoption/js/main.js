(function () {
    window.onload = function () {
        $('.loader').fadeOut()

    };

    autoStartVideo();

    function autoStartVideo() {
        if ($('.embed-responsive-item')) {
            if ($('.embed-responsive-item').get(0).paused) {
                $('.embed-responsive-item').get(0).play();
            }
        }
    }
})();