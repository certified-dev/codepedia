import re
from notify.signals import notify

from .models import User, Question


def highlight(text):
    points = re.search(r"\@\w+", text).span()

    if points is not None:
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



def send_notify(request, question_or_answer, content):
    if re.search("\@\w+", content) is not None:
        mention = (re.search("\@\w+", content).group())[1:]
        mentioned_user = User.objects.get(username=mention)

        if mentioned_user is not None:
            if Question.objects.filter(pk=question_or_answer.id).exists():
                notify.send(request.user, recipient=mentioned_user, actor=request.user,
                                verb='mentioned you in', obj=question_or_answer, nf_type='user_mentioned')
            else:
                notify.send(request.user, recipient=mentioned_user, actor=request.user,
                            verb='mentioned you in', obj=question_or_answer, target=question_or_answer.question,
                            nf_type='user_mentioned')
