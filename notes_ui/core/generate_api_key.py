import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_key_page(request):
    return render(request, "api_key_page.html")

@csrf_exempt
def generate_api_key(request):
    if request.method == "POST":
        try:
            resp = requests.post("http://127.0.0.1:8000/generate-api-key")
            
            return JsonResponse(resp.json(), status=resp.status_code)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)