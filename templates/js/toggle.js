// Toggle visibility tags
$(".toggler").on("click", function(){
    var $this = $(this);
    $this.parent().next().slideToggle();
    $this.toggleClass('bi-chevron-up bi-chevron-down');
});

$('.dropdown-toggle').click(function() {
    $(this).next('.dropdown-menu').toggleClass('show');
});
