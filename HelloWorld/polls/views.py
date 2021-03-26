from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World.You're at the polls index.")

def datail(request, question_id):
    return HttpResponse('You are looking at question %s.' % question_id)

def results(question, question_id):
    response = "you're looking at results of question %s"
    return HttpResponse(response % question_id)
