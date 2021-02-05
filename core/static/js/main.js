 $(document).ready(function(){

    if ($(window).width() < 1000 ){
      
      $(".laptop").remove();

    } else {

      $(".mobile").remove();
    
    }

    $("#modelId").modal('show');

    $("#wmd-input-id_body,#wmd-input-id_description").addClass('border-bottom-0 border-left-0 border-right-0');
    
    $(".post-answer").click(function(e) {

      var content = $("#wmd-input-id_body").val();

      if ( content.length < 1) {
          e.preventDefault();
          alert('cannot submit empty answer!');
        } else if ( content.length < 19 ) {
          e.preventDefault();
          alert('enter at least 20  characters!');
        } else {

        }

    });


      $("#question-toggle").click(function(e) {
          e.preventDefault();
          $("#click").toggleClass("fa-minus fa-plus");

          if ($("#inner").html() === "Show") {
             $("#inner").html("Hide")
          } else {
             $("#inner").html('Show')
          }
      });


       $('#remove').click(function(){
          $('#answer_div').hide();
       });


       $('.activate-update').hover(function(){
           var comment = this.id
           if ($("#activate-" + comment).is(':visible')) {
              $('#activate-' + comment).hide();
           } else {
              $('#activate-' + comment).show();
          }
       });

      $('.activate-update2').hover(function(){
          var comment = this.id
          if ($("#activate-" + comment).is(':visible')) {
           $('#activate-' + comment).hide();
          } else {
           $('#activate-' + comment).show();
          }
      });


        $('.answer-comment').hover(function(){
            var comment = this.id
            if ($("#add-" + comment).is(':visible')) {
                $('#add-' + comment).hide();
            } else {
                $('#add-' + comment).show();
            }
         });


        $('.mobile-answer-comment').hover(function(){
            var comment = this.id
            if ($("#add-" + comment).is(':visible')) {
                $('#add-' + comment).hide();
            } else {
                $('#add-' + comment).show();
            }
        });


      $(".add").click(function() {
           var answer_id = this.id
           $("#now_" + answer_id).show();
           $(".add_comment_answer").hide();
      });

      $(".add2").click(function() {
           var question_id = this.id
           $(".now_" + question_id).show();
           $(".add_comment_question").hide();        
      });


      $('#inbox').click(function(){

        if ($("#menu").is(":visible")) {

          $("#menu").hide();
          $("#menu-link").removeClass('bg-light');

        }

         if ($("#achievement-row").is(":visible")) {

          $("#achievement-row").hide();
          $("#achievement-link").removeClass('bg-light');

        }

         if ($("#inbox-row").is(":visible")) {

            $("#mini-nav").hide();
            $("#nav-anchor").removeClass('fixed-top');

            $("#inbox-row").hide();
            $("#inbox-link").removeClass('bg-light');

            $("#popup-container").hide();

          } else {

            $("#mini-nav-action").html('Inbox');
            $("#mini-nav").show();
            $("#nav-anchor").addClass('fixed-top');

            $("#inbox-row").show();
            $("#inbox-link").addClass('bg-light');

            $("#popup-container").show();

          }
  
      });

      $('#achievement').click(function(){

        if ($("#menu").is(":visible")) {

          $("#menu").hide();
          $("#menu-link").removeClass('bg-light');

        }

        if ($("#inbox-row").is(":visible")) {

           $("#inbox-row").hide();
           $("#inbox-link").removeClass('bg-light');

        }

        if ($("#achievement-row").is(":visible")) {

            $("#mini-nav").hide();
            $("#nav-anchor").removeClass('fixed-top');

            $("#achievement-row").hide();
            $("#achievement-link").removeClass('bg-light');

            $("#popup-container").hide();

          } else {

            $("#mini-nav-action").html('Achievement');
            $("#mini-nav").show();
            $("#nav-anchor").addClass('fixed-top');

            $("#achievement-row").show();
            $("#achievement-link").addClass('bg-light');

            $("#popup-container").show();

          }

      });

    
      $('#menu-click').click(function(){

        if ($("#inbox-link").hasClass('bg-light')) { 

          $("#inbox-row").hide();
          $("#inbox-link").removeClass('bg-light');
          
        } 

        if ($("#achievement-link").hasClass('bg-light')) { 
          
          $("#achievement-row").hide();
          $("#achievement-link").removeClass('bg-light');

        } 
       
        if ($("#menu").is(":visible")) {

          $("#mini-nav").hide();
          $("#nav-anchor").removeClass('fixed-top');
          $("#menu").hide();
          $("#menu-link").removeClass('bg-light');
          $("#popup-container").hide();


        } else {

          $("#popup-container").show();
          $("#mini-nav-action").html('About');
          $("#mini-nav").show();
          $("#nav-anchor").addClass('fixed-top');
          $("#menu").show();  
          $("#menu-link").addClass('bg-light');
          
        }

      });

      $('#cancel-all').click(function(){
        $("#mini-nav").hide();
        $("#nav-anchor").removeClass('fixed-top');

        $("#inbox-row").hide();
        $("#inbox-link").removeClass('bg-light');

        $("#achievement-row").hide();
        $("#achievement-link").removeClass('bg-light');

        $("#menu").hide();  
        $("#menu-link").removeClass('bg-light');

        $("#popup-container").hide();

      });


   });