 $(document).ready(function(){

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
          $('#answer_div').remove();
        });

        $('.shaw').hover(function(){
          $('.newt').show();
        });

      $(".add").click(function() {
        var answer_id = this.id
        $("#now_" + answer_id).show();
        $(".add_comment_answer").hide();
      });

       $(".add2").click(function() {
        var answer_id = this.id
        $(".now_" + answer_id).show();
        $(".add_comment_question").hide();
      });

       $("textarea").keyup(function() {
         if ( $(this).val().length > 14 ){
             $("button").prop("disabled",false);
         }  else {
             $("button").prop("disabled",true);
         }
      });
      });