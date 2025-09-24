import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

FASTAPI_URL = "http://127.0.0.1:8000/admin/generate-api-key"  # your FastAPI server
# ADMIN_SECRET = "super-secret-felix-only"  # must match FastAPI

import requests
from django.shortcuts import render
from django.http import JsonResponse

def api_key_page(request):
    api_key = None
    error = None
    
    if request.method == "POST":
        try:
            resp = requests.post("http://127.0.0.1:8000/generate-api-key")
            if resp.status_code == 200:
                api_key = resp.json().get("api_key")
            else:
                error = f"Error {resp.status_code}: {resp.text}"
        except Exception as e:
            error = str(e)
    
    return render(request, "api_key_page.html", {"api_key": api_key, "error": error})


def generate_api_key(request):
    if request.method == "POST":
        try:
            resp = requests.post("http://127.0.0.1:8001/generate-api-key")
            return JsonResponse(resp.json(), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
