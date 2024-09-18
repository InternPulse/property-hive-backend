from django.http import JsonResponse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .models import Company
from rest_framework.decorators import api_view


@api_view(["POST"])
def generate_custom_url(request):
    company_id = request.data.get("company_id")
    company = get_object_or_404(Company, id=company_id)

    if not company.custom_url:
        slug = slugify(company.name)
        company.custom_url = f"{slug}.propertyhive.com"
        company.save()

    return JsonResponse(
        {
            "status_code": 200,
            "message": "Custom URL generated successfully",
            "data": {"custom_url": company.custom_url},
        }
    )
