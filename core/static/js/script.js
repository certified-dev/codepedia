var score = JSON.parse(document.getElementById('score').textContent);
var upvoted = JSON.parse(document.getElementById('upvoted').textContent);
var downvoted = JSON.parse(document.getElementById('downvoted').textContent);
var answers = JSON.parse(document.getElementById('answers_serialized').textContent);
var current_user = JSON.parse(document.getElementById('current_user').textContent);
var question_owner = JSON.parse(document.getElementById('question_owner').textContent);
var question_id = JSON.parse(document.getElementById('question_id').textContent);
var result = "null"


Vue.component('answer', {
  delimiters: ["[[", "]]"],
  props: ['answer'],
  data : function () {
        return {
                current_user: current_user,
                question_id: question_id,
                question_owner: question_owner
                }
        },
  methods: {
    vote: vote,
    accept: accept,
    submitComment: submitComment

   },
  template: `
  <div>

   <div class="container mb-1 pl-0 pr-0">
      <div class="row">
         <div class="col-12 pr-2 pl-2">

            <div class="row mobile pl-3 pr-3">
              <div class="col-12">
                  <div class="row pl-0 pr-0">
                     <div class="col-2 pl-0 pr-2 bg-light">
                           <div class="row">
                              <div class="col-12 p-0 pl-2 text-center">
                                 <a href="javascript:void(0)" v-on:click="vote('upvote', answer.upvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.upvoted ? 'done' : 'undone']]">
                                    <svg width="30" height="30" viewBox="0 0 16 16" class="bi bi-caret-up-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                       <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                                    </svg>
                                 </a>
                              </div>
                           
                              <div class="col-12 p-0 pl-2 text-center">
                                 <h6 class="mb-0">[[ answer.score ]]</h6>
                              </div>

                              <div class="col-12 p-0 pl-2 text-center">
                                 <a href="javascript:void(0)" v-on:click="vote('downvote', answer.downvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.downvoted ? 'done' : 'undone']]">
                                    <svg width="30" height="30" viewBox="0 0 16 16" class="bi bi-caret-down-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                       <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                                    </svg>
                                 </a>
                              </div>
            
                              <div v-if="answer.question_owner == [[ current_user ]] " class="col-12 p-0 pl-2 text-center">
                                 <a href="javascript:void(0)" v-on:click="accept('accept', answer.accepted, '/answer/' + [[ answer.pk ]] + '/accept/')" :class="[[ answer.accepted ? 'checked' : 'undone']]">
                                    <i class="fas fa-check fa-lg"></i>
                                 </a>
                              </div>

                           <div v-if="answer.accepted && answer.question_owner != [[ current_user ]]" class="col-12 p-0 pl-2 text-center">
                              <i class="fas fa-check fa-lg text-success"></i>
                           </div>

                           </div>
                     </div>
                    
                     <div class="col-10 pl-2 pr-0">
                        <div class="answer-text" v-html="answer.text_html"></div>
                     </div>
                  </div>
               </div>
            </div>

            <div class="row laptop">
              <div class="col-1">
                  <div class="row">
                     <div class="col-12 p-0 pl-2 text-center">
                         <a href="javascript:void(0)" v-on:click="vote('upvote', answer.upvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.upvoted ? 'done' : 'undone']]">
                            <svg width="40" height="40" viewBox="0 0 16 16" class="bi bi-caret-up-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                               <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                            </svg>
                         </a>
                     </div>
                    
                     <div class="col-12 p-0 pl-2 text-center">
                        <h5 class="mb-0 text-secondary">[[ answer.score ]]</h5>
                     </div>
               
                     <div class="col-12 p-0 pl-2 text-center">
                        <a href="javascript:void(0)" v-on:click="vote('downvote', answer.downvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.downvoted ? 'done' : 'undone']]">
                           <svg width="40" height="40" viewBox="0 0 16 16" class="bi bi-caret-down-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                           </svg>
                        </a>
                     </div>

                     <div v-if="answer.question_owner == [[ current_user ]] " class="col-12 p-0 pl-2 text-center">
                        <a href="javascript:void(0)" v-on:click="accept('accept', answer.accepted, '/answer/' + [[ answer.pk ]] + '/accept/')" :class="[[ answer.accepted ? 'checked' : 'undone']]">
                           <i class="fas fa-check fa-2x"></i>
                        </a>
                     </div>
                     
                    <div v-if="answer.accepted && answer.question_owner != [[ current_user ]] " class="col-12 p-0 pl-2 text-center">
                       <i class="fas fa-check fa-2x text-success"></i>
                    </div>

                  </div>
              </div>
              <div class="col-11 pl-2">
                <div class="answer-text" v-html="answer.text_html"></div>
              </div>    
            </div>

         </div>

         <div class="col-12 mobile">
            <div class="row pl-2 pr-2">
               <div v-if="answer.answered_by == [[ current_user ]]" class="col-12 p-1 border-top mobile">   
                  <span class="small">
                     <a :href=" '/question/' + [[ question_id ]] +'/answer/' + answer.pk + '/update/'" class="mr-3 ml-1 text-secondary">edit</a>          
                     <a href="javascript:void(0)" class="text-secondary" onclick="alert('are you sure you want to delete this answer?')">delete</a>
                  </span>        
               </div>
               <div :class="[[ answer.answered_by == question_owner ? 'highlight-mobile col-12 p-2 border-top border-bottom shadow-sm' : 'col-12 p-2 border-top border-bottom shadow-sm' ]]">
                  <small class="text-secondary">
                     <a :href="'/users/' + answer.answered_by_id + '/' + answer.answered_by + '/'">
                        <img :src="answer.answered_by_image" class="rounded img-fluid" height="25" width="25"/>
                        <b>[[ answer.answered_by ]]</b>
                     </a>
                     <span class="text-dark">[[ answer.answered_by_points ]]</span>
                     <span class="float-right mt-1">asked [[ answer.posted_on ]]</span>
                  </small>
               </div>
               <div v-if="answer.updated_on" class="col-12 p-2 shadow-sm border-top border-bottom">
                   <small class="text-secondary">
                     <span class="float-right mt-1">edited [[ answer.updated_on ]]</span>
                  </small>
               </div>
            </div>
         </div>

         <div class="col-12 pl-2 pr-2 laptop">
            <div class="row">
               <div class="col-1"></div>
               <div class="col-11 pl-0 pr-1">                   
                  <div class="row pb-2">
                     <div class="col-8 pl-4">
                        <small v-if="answer.answered_by == [[ current_user ]]">
                           <a class="text-secondary" :href=" '/question/' + [[ question_id ]] +'/answer/' + answer.pk + '/update/'">edit</a>
                           <span class="mr-3"></span>
                           <a class="text-secondary" href="#" onclick="alert('are you sure you want to delete this answer?')">delete</a>
                        </small>

                        <span v-if="answer.updated_on" class="text-muted float-right small">edited [[ answer.updated_on ]]</span>
                     </div>
                     <div :class="[[ question_owner == answer.answered_by ? 'highlight-laptop col-3 pb-1 pl-3 ml-5' : 'col-3 pb-1 pl-3 ml-5']]">
                        <div class="row">
                           <div class="col-12">
                              <span class="text-secondary"><small> [[ answer.posted_on ]]</small></span>
                           </div>
                           <div class="col-12">
                              <div class="row">
                                 <div class="col-3">
                                    <a :href="'/users/' + answer.answered_by_id + '/' + answer.answered_by + '/'"><img :src="answer.answered_by_image"  class="rounded" width="28" height="28"/></a>
                                 </div>
                                 <div class="col-9 p-0 pl-1">
                                    <small>
                                       <span>
                                          <a :href="'/users/' + answer.answered_by_id + '/' + answer.answered_by + '/'"> [[ answer.answered_by ]]</a>
                                       </span>
                                       <span>
                                          <b class="text-secondary">[[ answer.answered_by_points ]]</b>
                                       </span>
                                    </small>
                                 </div>
                              </div>
                           </div>
                        </div>
                     </div>
                  </div>
               </div>            
            </div> 
         </div>
         
      </div>

      <div class="col-12 pl-2 pr-2 mobile">
         <div class="row pr-0 pl-0" v-if="answer.comments.length > 0">
            <div class="col-2 pr-0 mt-1 bg-light"></div>      
            <div class="col-10 pr-0 pl-0">
               <div v-for="comment in answer.comments" :id="'mob-answer-comment-' + comment.id" class="border-bottom mobile-answer-comment p-2 text-secondary">
                  <span v-html="comment.text_html"></span> – <a :href="'/users/' + comment.posted_by_id + '/' + comment.posted_by + '/'" :class="[[ comment.posted_by == answer.answered_by ? 'highlight-link font-weight-bold' : 'font-weight-bold' ]]">[[ comment.posted_by ]]</a> <span class="text-primary">[[ comment.posted_on ]]</span>
                     <span v-if="comment.posted_by == [[ current_user ]]">
                        <span :id="'add-mob-answer-comment-' + comment.id" style="display:none">
                        <a href="#" class="ml-1"><i class="fas fa-pen"></i></a>
                        <a href="#" class="text-danger ml-2"><i class="fas fa-trash"></i></a>
                     </span>
                  </span>
               </div>
            </div>
         </div>      
      </div>

      <div class="col-12 pl-0 pr-2 laptop">
         <div class="row pr-0 pl-0" v-if="answer.comments.length > 0">
            <div class="col-1 pr-0 laptop"></div>       
            <div class="col-11 pl-0 pr-0 border-bottom mb-2">
               <div v-for="comment in answer.comments" :id="'answer-comment-' + comment.id" class="border-top answer-comment p-1" >
                  <span v-html="comment.text_html"></span> – <a :href="'/users/' + comment.posted_by_id + '/' + comment.posted_by + '/'" :class="[[ comment.posted_by == answer.answered_by ? 'highlight-link' : '' ]]">[[ comment.posted_by ]]</a> <span class="text-secondary">[[ comment.posted_on ]]</span>
                  <span v-if="comment.posted_by == [[ current_user ]]"> <span :id="'add-answer-comment-' + comment.id" style="display:none"> <a href="#" class="ml-1">edit</a>  <a href="#" class="text-danger ml-2">delete</a></span></span>
               </div>
            </div>
         </div>      
      </div>
      

      <div class="col-12 pr-0 pl-0 comment-box-remove">
         <div :id="'now_add_comment-' + answer.pk" style="display:none">
              <div class="row pt-2 pl-2 laptop">
                 <div class="col-1"></div>
                 <div class="col-11 pl-0">
                    <div class="row">
                       <div class="col-10 pr-0 pl-1">
                          <form method="post" novalidate>
                             <div class="form-group">
                                <textarea class="form-control form-control-sm" :id="'id_laptop_comment_text-'+ answer.pk" name="text" rows="2" placeholder="Use comments to ask for more information."></textarea>
                                <small id="helpId" class="form-text text-muted">enter at least 15  characters.</small>
                             </div>
                          </form>
                       </div>
                       <div class="col-2 p-0 pl-2 text-center">
                          <button type="button" v-on:click="submitComment('laptop_comment_text-'+ answer.pk, '/answer/' + answer.pk + '/reply/')" class="btn btn-primary btn-sm"> Add Comment </button>
                       </div>
                    </div>
                 </div>
              </div>
               <div class="row pl-2 pt-2 mobile shadow-sm" novalidate>
                  <div class="col-12 pl-0 pr-2">
                     <form method="post" novalidate>
                        <div class="form-group">
                           <textarea class="form-control form-control-sm" :id="'id_mobile_comment_text-'+ answer.pk" name="text" rows="2" placeholder="Use comments to ask for more information."></textarea>
                        </div>
                     </form>
                  </div>
                  <div class="col-12 pl-0">
                     <div class="row mb-2">
                        <div class="col-5">
                           <button type="button" v-on:click="submitComment('mobile_comment_text-'+ answer.pk, '/answer/' + answer.pk + '/reply/')" class="btn btn-primary btn-sm"> Add Comment </button>
                        </div>
                        <div class="col-7 pl-0">
                           <small id="helpId" class="form-text text-muted">enter at least 15 characters.</small>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
         </div>


         <div class="row pt-0">
            <div class="col-12 laptop add_comment_answer">
               <div class="row">
                  <div class="col-1 pr-0"></div>
                     <div class="col-11 pl-1 pr-2">
                       <small>
                          <a v-if="[[ current_user.length ]] > 0" href="javascript:void(0)" class="add" :id=" 'add_comment-' + answer.pk ">add a comment</a>
                          <a v-else href="javascript:void(0)">add a comment</a>
                       </small>
                    </div>
                </div>
             </div>
           </div>
           <hr class="laptop">

            <div class="col-12 pl-2 pr-2 mobile add_comment_answer mb-2">
               <div class="row pr-0 pl-0">       
                  <div class="col-12 p-2 text-center pb-1 bg-light">
                     <small>
                      <a v-if="[[ current_user.length ]] > 0" href="javascript:void(0)" class="add" :id=" 'add_comment-' + answer.pk ">add a comment</a>
                      <a v-else href="javascript:void(0)">add a comment</a>
                    </small>
                  </div>
               </div>
            
            </div>                   
         </div>

      </div>
      
   </div>
   

  </div>
  `
})


var app = new Vue({
  delimiters: ["[[", "]]"],
  el: '#question', 
  data: {
    downvoted: downvoted,
    upvoted: upvoted,
    score: score,
    answers: answers,
    question_owner: question_owner

  },
  methods: {
    vote: vote,
    submitComment: submitComment
  },
});


function vote(voteType, voted, voteURL) {
  var bodyFormData = new FormData();
  if (voted) {
    bodyFormData.set('vote_type', 'cancel_vote');
  } else {
    bodyFormData.set('vote_type', voteType);
  }

  axios({
    method: 'post',
    url: voteURL,
    data: bodyFormData,
    headers: {'Content-Type': 'multipart/form-data' }
  }).then((response) => {

    var responseVoteType = response.data.vote_type;
    var targetObj;

    if('answer' in this){
      targetObj = this.answer;
    } else {
      targetObj = this;
    }

    if (responseVoteType == 'upvote') {
      targetObj.upvoted = true;
      targetObj.downvoted = false;
    } else if (responseVoteType == 'downvote') {
      targetObj.upvoted = false;
      targetObj.downvoted = true;
    } else {
      targetObj.upvoted = false;
      targetObj.downvoted = false;
    }

    targetObj.score = response.data.score;

  }).catch((error) => {

    if(error.message.includes('401')) {
      window.location.href = "/accounts/login/";
    } else if (error.message.includes('400')) {
      alert('you cannot vote on your posts');
    }

  });
}


function accept(accept_type, accepted, acceptURL) {
  var bodyFormData = new FormData();
  if (accepted) {
    bodyFormData.set('accept_type', 'cancel_accept');
  } else {
    bodyFormData.set('accept_type', accept_type);
  }

  axios({
    method: 'post',
    url: acceptURL,
    data: bodyFormData,
    headers: {'Content-Type': 'multipart/form-data' }
  }).then((response) => {

    var responseAcceptType = response.data.accept_type;
    targetObj = this.answer;

    if (responseAcceptType == 'accept') {
      targetObj.accepted = true;
    } else if (responseAcceptType == 'cancel_accept') {
      targetObj.accepted = false;
    }

  }).catch((error) => {

    if(error.message.includes('401')) {
      window.location.href = "/accounts/login/";
    } else if (error.message.includes('400')) {
      alert('you cannot accept your own answers');
    }

  });
}


function submitComment(button_id, Comment_Url) {
   var bodyFormData = new FormData();
   var text_content = $("#id_" + button_id ).val();

   if ( text_content.length < 1) {
      alert('cannot submit empty comment!');
   } else if( text_content.length < 14 ) {
      alert('enter at least 15  characters!');
   } else{
      bodyFormData.set('text', text_content);

      axios({
          method: 'post',
          url: Comment_Url,
          data: bodyFormData,
          headers: {'Content-Type': 'application/json' }
      }).then((response) => {

      if('answer' in this){
         targetObj = this.answer;
      } else {
         targetObj = this;
      }

      if ( $(".add_comment_question").is(":hidden") ){

         $(".add_comment_question").show();
         $(".comment-box-remove").hide();

         if (response.data.last_comment == result){

            location.reload(true);

         } else {

            $("#comment-" + response.data.last_comment).removeClass('border-bottom');

            if (response.data.posted_by == question_owner ) {
   
               $("#comment-" + response.data.last_comment).after("<div class='border-top border-bottom activate-update p-1'>" + response.data.text_html + " – <a href='' class='highlight-link'>" + response.data.posted_by + "</a><span class='text-secondary'>" + response.data.posted_on + "</span></div>");
               $("#second-comment-" + response.data.last_comment).after("<div class='border-bottom pl-1 activate-update2 p-2 text-secondary' style='font-size: 12px;'>" + response.data.text_html + " – <a href='' class='highlight-link'>" + response.data.posted_by + "</a> <span class='text-secondary'>" + response.data.posted_on + "</span> </div>");
   
            } else {
               
               $("#comment-" + response.data.last_comment).after("<div class='border-top border-bottom activate-update p-1'>" + response.data.text_html + " – <a href=''>" + response.data.posted_by + "</a> <span class='text-secondary'>" + response.data.posted_on + "</span> </div>");
               $("#second-comment-" + response.data.last_comment).after("<div class='border-bottom pl-1 activate-update2 p-2 text-secondary' style='font-size: 12px;'>" + response.data.text_html + " – <a href=''>" + response.data.posted_by + "</a> <span class='text-secondary'>" + response.data.posted_on + "</span> </div>");
               
            }

         }

      }

      if ( $(".add_comment_answer").is(":hidden") ){

         $(".add_comment_answer").show();
         $(".comment-box-remove").hide();

         if (response.data.last_comment == result){

            location.reload(true);

         } else {

            if (response.data.posted_by == targetObj.answered_by ) {

               $("#answer-comment-" + response.data.last_comment).after("<div class='border-top answer-comment p-1'>" + response.data.text_html + " – <a href='' class='highlight-link'>" + response.data.posted_by + "</a> <span class='text-secondary'>" + response.data.posted_on + "</span> </div>");           
               $("#mob-answer-comment-" + response.data.last_comment).after("<div class='border-top pl-1 mobile-answer-comment p-2 text-secondary'>" + response.data.text_html + " – <a href='' class='highlight-link font-weight-bold'>" + response.data.posted_by + "</a> <span class='text-primary'>" + response.data.posted_on + "</span> </div>");
   
            } else {
   
               $("#answer-comment-" + response.data.last_comment).after("<div class='border-top answer-comment p-1'>" + response.data.text_html + " – <a href='' class=''>" + response.data.posted_by + "</a> <span class='text-secondary'>" + response.data.posted_on + "</span> </div>");     
               $("#mob-answer-comment-" + response.data.last_comment).after("<div class='border-top pl-1 mobile-answer-comment p-2 text-secondary'>" + response.data.text_html + " – <a href='' class='font-weight-bold'>" + response.data.posted_by + "</a> <span class='text-primary'>" + response.data.posted_on + "</span> </div>");
   
            }   

         } 
         
      }

      }).catch((error) => {

         alert(error);

      });

   }

}

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
