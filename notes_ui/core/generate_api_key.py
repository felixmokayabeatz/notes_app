# generate_api_key.py
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_key_page(request):
    """
    Serve the HTML page for generating API keys
    """
    return render(request, "api_key_page.html")

@csrf_exempt
def generate_api_key(request):
    """
    Proxy endpoint to call FastAPI (optional - you can call FastAPI directly from frontend)
    """
    if request.method == "POST":
        try:
            # Directly call FastAPI
            resp = requests.post("http://127.0.0.1:8000/generate-api-key")
            
            # Return the same response from FastAPI
            return JsonResponse(resp.json(), status=resp.status_code)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)