var score = JSON.parse(document.getElementById('score').textContent);
var upvoted = JSON.parse(document.getElementById('upvoted').textContent);
var downvoted = JSON.parse(document.getElementById('downvoted').textContent);
var answers = JSON.parse(document.getElementById('answers_serialized').textContent);
var current_user = JSON.parse(document.getElementById('current_user').textContent);
var question_id = JSON.parse(document.getElementById('question_id').textContent);


Vue.component('answer', {
  delimiters: ["[[", "]]"],
  props: ['answer'],
  data : function () {
        return {
                current_user: current_user,
                question_id: question_id
                }
        },
  methods: {
    vote: vote,
    accept: accept,
    submitComment: submitComment

   },
  template: `
  <div>

   <div class="container mb-1 pt-1 pb-1 pl-2 pr-2">
      <div class="row">
         <div class="col-12 pr-2 pl-2" >
            <div class="row">

              <div class="col-1 ml- mobile">
                  <div class="row">
                     <div class="col-12 p-0 pl-2 text-center mobile">
                         <a href="javascript:void(0)" v-on:click="vote('upvote', answer.upvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.upvoted ? 'done' : 'undone']]">
                            <svg width="30" height="30" viewBox="0 0 16 16" class="bi bi-caret-up-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                               <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                            </svg>
                         </a>
                     </div>
                     <div class="col-12 p-0 pl-2 text-center laptop">
                         <a href="javascript:void(0)" v-on:click="vote('upvote', answer.upvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.upvoted ? 'done' : 'undone']]">
                            <svg width="40" height="40" viewBox="0 0 16 16" class="bi bi-caret-up-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                               <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                            </svg>
                         </a>
                     </div>
                     <div class="col-12 p-0 pl-2 text-center">
                        <h6 class="mb-0 mobile">[[ answer.score ]]</h6>
                        <h5 class="mb-0 text-secondary laptop">[[ answer.score ]]</h5>
                     </div>
                     <div class="col-12 p-0 pl-2 text-center mobile">
                        <a href="javascript:void(0)" v-on:click="vote('downvote', answer.downvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.downvoted ? 'done' : 'undone']]">
                           <svg width="30" height="30" viewBox="0 0 16 16" class="bi bi-caret-down-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                           </svg>
                        </a>
                     </div>
                     <div class="col-12 p-0 pl-2 text-center laptop">
                        <a href="javascript:void(0)" v-on:click="vote('downvote', answer.downvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.downvoted ? 'done' : 'undone']]">
                           <svg width="40" height="40" viewBox="0 0 16 16" class="bi bi-caret-down-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                           </svg>
                        </a>
                     </div>

                     <div v-if="answer.question_owner == [[ current_user ]] " class="col-12 p-0 pl-2 text-center laptop">
                        <a href="javascript:void(0)" v-on:click="accept('accept', answer.accepted, '/answer/' + [[ answer.pk ]] + '/accept/')" :class="[[ answer.accepted ? 'checked' : 'undone']]">
                           <i class="fas fa-check fa-2x"></i>
                        </a>
                     </div>
                     <div v-if="answer.question_owner == [[ current_user ]] " class="col-12 p-0 pl-2 text-center mobile">
                        <a href="javascript:void(0)" v-on:click="accept('accept', answer.accepted, '/answer/' + [[ answer.pk ]] + '/accept/')" :class="[[ answer.accepted ? 'checked' : 'undone']]">
                           <i class="fas fa-check fa-lg"></i>
                        </a>
                     </div>

                    <div v-if="answer.accepted && answer.question_owner != [[ current_user ]] " class="col-12 p-0 pl-2 text-center laptop">
                       <i class="fas fa-check fa-2x text-success"></i>
                    </div>
                    <div v-if="answer.accepted && answer.question_owner != [[ current_user ]]" class="col-12 p-0 pl-2 text-center mobile">
                       <i class="fas fa-check fa-lg text-success"></i>
                    </div>

                  </div>
              </div>

              <div class="col-1 laptop">
                  <div class="row">
                     <div class="col-12 p-0 pl-2 text-center mobile">
                         <a href="javascript:void(0)" v-on:click="vote('upvote', answer.upvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.upvoted ? 'done' : 'undone']]">
                            <svg width="30" height="30" viewBox="0 0 16 16" class="bi bi-caret-up-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                               <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                            </svg>
                         </a>
                     </div>
                     <div class="col-12 p-0 pl-2 text-center laptop">
                         <a href="javascript:void(0)" v-on:click="vote('upvote', answer.upvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.upvoted ? 'done' : 'undone']]">
                            <svg width="40" height="40" viewBox="0 0 16 16" class="bi bi-caret-up-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                               <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                            </svg>
                         </a>
                     </div>
                     <div class="col-12 p-0 pl-2 text-center">
                        <h6 class="mb-0 mobile">[[ answer.score ]]</h6>
                        <h5 class="mb-0 text-secondary laptop">[[ answer.score ]]</h5>
                     </div>
                     <div class="col-12 p-0 pl-2 text-center mobile">
                        <a href="javascript:void(0)" v-on:click="vote('downvote', answer.downvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.downvoted ? 'done' : 'undone']]">
                           <svg width="30" height="30" viewBox="0 0 16 16" class="bi bi-caret-down-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                           </svg>
                        </a>
                     </div>
                     <div class="col-12 p-0 pl-2 text-center laptop">
                        <a href="javascript:void(0)" v-on:click="vote('downvote', answer.downvoted, '/answer/' + [[ answer.pk ]] + '/vote/')" :class="[[answer.downvoted ? 'done' : 'undone']]">
                           <svg width="40" height="40" viewBox="0 0 16 16" class="bi bi-caret-down-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                           </svg>
                        </a>
                     </div>

                     <div v-if="answer.question_owner == [[ current_user ]] " class="col-12 p-0 pl-2 text-center laptop">
                        <a href="javascript:void(0)" v-on:click="accept('accept', answer.accepted, '/answer/' + [[ answer.pk ]] + '/accept/')" :class="[[ answer.accepted ? 'checked' : 'undone']]">
                           <i class="fas fa-check fa-2x"></i>
                        </a>
                     </div>
                     <div v-if="answer.question_owner == [[ current_user ]] " class="col-12 p-0 pl-2 text-center mobile">
                        <a href="javascript:void(0)" v-on:click="accept('accept', answer.accepted, '/answer/' + [[ answer.pk ]] + '/accept/')" :class="[[ answer.accepted ? 'checked' : 'undone']]">
                           <i class="fas fa-check fa-lg"></i>
                        </a>
                     </div>

                    <div v-if="answer.accepted && answer.question_owner != [[ current_user ]] " class="col-12 p-0 pl-2 text-center laptop">
                       <i class="fas fa-check fa-2x text-success"></i>
                    </div>
                    <div v-if="answer.accepted && answer.question_owner != [[ current_user ]]" class="col-12 p-0 pl-2 text-center mobile">
                       <i class="fas fa-check fa-lg text-success"></i>
                    </div>

                  </div>
              </div>

              <div class="col-11 pl-3 mobile">
                <span class="mobile"><div class="answer-text" v-html="answer.text_html"></div></span>
              </div>

              <div class="col-11 pl-2 laptop">
                <span class="laptop"><div class="answer-text" v-html="answer.text_html"></div></span>
              </div>

           </div>
         </div>


         <div v-if="answer.answered_by != [[ current_user ]]" class="col-12 pl-2 pr-2">
             <div class="row">

                 <div class="col-1"></div>
                 <div class="col-11 pl-2 pr-3">

                      <small class="text-secondary mobile">
                        <img :src="answer.answered_by_image" class="rounded img-fluid" height="18" width="18"/>
                          <a :href="'/user/' + answer.answered_by_id + '/profile/'">[[ answer.answered_by ]]</a>
                       <span class="float-right"><i class="fas fa-clock"></i> [[ answer.posted_on ]]</span>
                      </small>


                      <div class="row pb-2 laptop">
                         <div class="col-8 pl-3">
                         <span v-if="answer.updated_on" class="text-muted float-right small">edited [[ answer.updated_on ]]</span>
                         </div>
                             <div class="col-3 bg-light pb-1 ml-5">
                                 <div class="row">
                                     <div class="col-12">
                                         <span class="text-secondary"><small> [[ answer.posted_on ]]</small></span>
                                     </div>
                                     <div class="col-12">
                                        <div class="row">
                                           <div class="col-3">
                                              <img :src="answer.answered_by_image"  class="rounded" width="28" height="28"/>
                                           </div>
                                           <div class="col-9 p-0 pl-1">

                                              <small>
                                                  <span>
                                                    <a :href="'/user/' + answer.answered_by_id + '/profile/'"> [[ answer.answered_by ]]</a>
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


         <div v-if="answer.answered_by == [[ current_user ]]" class="col-12 pl-2 pr-2">
            <div class="row">

               <div class="col-1"></div>
               <div class="col-11 pl-0 pr-1">

                  <small class="text-secondary mobile">
                     <img :src="answer.answered_by_image" class="rounded img-fluid" height="18" width="18"/>
                     <a :href="'/user/' + answer.answered_by_id + '/profile/'">[[ answer.answered_by ]]</a>
                     <span class="text-secondary"> | </span>
                     <a :href=" '/question/' + [[ question_id ]] +'/answer/' + answer.pk + '/update/'" class="text-secondary">edit</a>
                     <span class="text-secondary"> | </span>
                     <a href="javascript:void(0)" class="text-secondary" onclick="alert('are you sure you want to delete this answer?')">delete</a>
                     <span class="float-right"><i class="fas fa-clock"></i> [[ answer.posted_on ]]</span>
                  </small>

                  <div class="row pb-2 laptop">
                     <div class="col-8 pl-2">
                        <small>
                           <a class="text-secondary" :href=" '/question/' + [[ question_id ]] +'/answer/' + answer.pk + '/update/'">edit</a>
                           <span class="mr-3"></span>
                           <a class="text-secondary" href="#" onclick="alert('are you sure you want to delete this answer?')">delete</a>
                       </small>
                       <span v-if="answer.updated_on" class="text-muted float-right small">edited [[ answer.updated_on ]]</span>
                     </div>
                     <div class="col-3 bg-light pb-1 ml-5">
                         <div class="row">
                             <div class="col-12">
                                 <span class="text-secondary"><small> [[ answer.posted_on ]]</small></span>
                             </div>
                             <div class="col-12">
                                 <div class="row">
                                     <div class="col-3">
                                         <img :src="answer.answered_by_image"  class="rounded" width="28" height="28"/>
                                     </div>
                                     <div class="col-9 p-0 pl-1">

                                        <small>
                                            <span>
                                                <a :href="'/user/' + answer.answered_by_id + '/profile/'"> [[ answer.answered_by ]]</a>
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

      <div class="col-12 pl-2 pr-2">
         <div class="row pr-2 pl-0" v-if="answer.comments.length > 0">

            <div class="col-1 pr-0"></div>
            <div class="col-11 pr-0 pl-0 mobile">
               <div v-for="comment in answer.comments" :id="'mob-answer-comment-' + comment.id" class="border-top pl-1 mobile-answer-comment p-1">
                  <span v-html="comment.text_html"></span> – <a :href="'/user/' + comment.posted_by_id + '/profile/'" :class="[[ comment.posted_by == answer.answered_by ? 'highlighted' : '' ]]">[[ comment.posted_by ]]</a> <span class="primary text-secondary">[[ comment.posted_on ]]</span>
                     <span v-if="comment.posted_by == [[ current_user ]]">
                        <span :id="'add-mob-answer-comment-' + comment.id" style="display:none">
                        <a href="#" class="ml-1"><i class="fas fa-pen"></i></a>
                        <a href="#" class="text-danger ml-2"><i class="fas fa-trash"></i></a>
                     </span>
                  </span>
               </div>
            </div>

            <div class="col-11 pl-0 pr-0 laptop border-bottom">
               <div v-for="comment in answer.comments" :id="'answer-comment-' + comment.id" class="border-top answer-comment p-1" >
                  <span v-html="comment.text_html"></span> – <a :href="'/user/' + comment.posted_by_id + '/profile/'" :class="[[ comment.posted_by == answer.answered_by ? 'highlighted' : '' ]]">[[ comment.posted_by ]]</a> <span class="text-secondary">[[ comment.posted_on ]]</span>
                  <span v-if="comment.posted_by == [[ current_user ]]"> <span :id="'add-answer-comment-' + comment.id" style="display:none"> <a href="#" class="ml-1">edit</a>  <a href="#" class="text-danger ml-2">delete</a></span></span>
               </div>
            </div>

         </div>
         
      </div>
      


      <div class="col-12 pr-1 comment-box-remove">
         <div :id="'now_add_comment-' + answer.pk" class="comment-box-remove" style="display:none">


               <div class="col-12 pl-2 laptop">  
                  <div class="row pt-2">
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
                           <div class="col-2 p-0 text-center">
                              <button type="button" v-on:click="submitComment('laptop_comment_text-'+ answer.pk, '/answer/' + answer.pk + '/reply/')" class="btn btn-primary btn-sm"> Add Comment </button>
                           </div>
                        </div>
                     </div>
                  </div>
               </div>

               <div class="row pt-2 mobile" novalidate>

                  <div class="col-12 pl-0">
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


         <div class="row pt-2 laptop add_comment_answer">
            <div class="col-1 pr-0"></div>
               <div class="col-11 pl-1 pr-2">
                  <small><a href="javascript:void(0)" class="add" :id=" 'add_comment-' + answer.pk">add a comment</a></small>
               </div>
            </div>

            <div class="col-12 pl-2 pr-2 mobile add_comment_answer">
               <div class="row pr-2 pl-0">
                  <div class="col-1 pr-0"></div>
                  <div class="col-11 pl-1 pr-1 text-center border border-bottom-0 pb-1 bg-light">
                     <small><a href="javascript:void(0)" class="add" :id=" 'add_comment-' + answer.pk ">add a comment</a></small>
                  </div>
               </div>
               <div class="mobile border-top"></div>
           </div>

           <hr class="laptop">

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
    answers: answers

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

      console.log(response.data);
      alert('comment-posted!!!');

      $(".comment-box-remove").hide();

      }).catch((error) => {

         alert('error!!!');

      });

   }

}

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
