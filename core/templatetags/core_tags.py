from hashlib import md5
from django import template

register = template.Library()


@register.filter(name="gravatar")
def gravatar(user, size=35):
    email = str(user.email.strip().lower()).encode('utf-8')
    email_hash = md5(email).hexdigest()
    url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
    return url.format(email_hash, size)


@register.filter
def shorten_naturaltime(naturaltime):
    naturaltime = naturaltime.replace('minute', 'min').replace('minutes', 'mins').replace('hours', 'hrs').replace('days', 'd').replace('day', 'd')
    naturaltime = naturaltime.replace('months', 'mth').replace('weeks', 'wks').replace('week', 'wk')
    return naturaltime
