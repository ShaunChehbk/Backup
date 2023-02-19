from django.http import HttpResponse
import datetime

def lvelvelve(request):
    now = datetime.datetime.now()
    html = '<html><body><center><font style="font-size:55px">🐵 🙈 🙉 🙊<br>%s</font></center></body></html>' % now
    return HttpResponse(html)