import re
from notify.signals import notify

from .models import User, Question


def highlight(text):
    is_mentioned = re.search(r"\@\w+", text)

    if is_mentioned is not None:
        points = is_mentioned.span()
        x = int(points[0])
        y = int(points[1]) + 1

        open_tag = "<b>"
        close_tag = "</b>"

        new_text = list(text)
        new_text.insert(x, open_tag)
        new_text.insert(y, close_tag)
        new_text = "".join(new_text)
        new_comment = str(new_text)

        return new_comment
    else:
        return text
    
        



def send_notify(request, question_or_answer, content):
    is_mentioned = re.search("\@\w+", content)
    if is_mentioned is not None:
        mention = is_mentioned.group()[1:]

        if User.objects.filter(username=mention).exists():
            mentioned_user = User.objects.get(username=mention)

            if mentioned_user is not None:
                if Question.objects.filter(pk=question_or_answer.id).exists():
                    if question_or_answer.asked_by != request.user:
                        notify.send(request.user, recipient=mentioned_user, actor=request.user,
                                    verb='mentioned you in', obj=question_or_answer, nf_type='user_mentioned')
                else:
                    if question_or_answer.answered_by != request.user:
                        notify.send(request.user, recipient=mentioned_user, actor=request.user,
                                verb='mentioned you in', obj=question_or_answer, target=question_or_answer.question,
                                nf_type='user_mentioned')
