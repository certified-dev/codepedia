import re
import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from notify.signals import notify

from .models import User


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


def send_notify(request, question_or_answer, object_type, content):
    is_mentioned = re.search("\@\w+", content)
    if is_mentioned is not None:
        mention = is_mentioned.group()[1:]

        mentioned_user = User.objects.get(username=mention)
        if mentioned_user:
            if object_type == 'question':
                if question_or_answer.asked_by != request.user:
                    notify.send(request.user, recipient=mentioned_user, actor=request.user,
                                verb='mentioned you in', obj=question_or_answer, nf_type='user_mentioned')
            elif object_type == "answer":
                if question_or_answer.answered_by != request.user:
                    notify.send(request.user, recipient=mentioned_user, actor=request.user,
                                verb='mentioned you in', obj=question_or_answer, target=question_or_answer.question,
                                nf_type='user_mentioned')


def compress(file):
    temp_image = Image.open(file)
    outputIoStream = BytesIO()
    resized_temp_image = temp_image.resize((1100, 1000))
    resized_temp_image.save(outputIoStream, format='JPEG', quality=60)
    outputIoStream.seek(0)
    final_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % file.name.split('.')[0],
                                       'image/jpeg', sys.getsizeof(outputIoStream), None)
    return final_image
