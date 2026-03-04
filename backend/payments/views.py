from django.http import HttpResponse

def payment_return(request):
    return HttpResponse("OK. Payment return received. Await webhook for final status.")