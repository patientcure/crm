from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import User
from links.models import Link
from .models import Customer
from .serializers import CustomerOnboardingSerializer
from .html_assets import get_onboarding_html 

class CustomerOnboardingAPIView(APIView):
    permission_classes = () 

    def get(self, request, link_id, connector_id, format=None):
        # 1. Validation
        link = get_object_or_404(Link, pk=link_id)
        try:
            connector = User.objects.get(id=connector_id)
            if connector.role not in ('ADMIN', 'STAFF', 'CONNECTOR'):
                 return HttpResponse("Invalid Connector Role", status=400)
        except User.DoesNotExist:
             return HttpResponse("Connector Not Found", status=404)

        # 2. Prepare Data
        context_data = {
            "product_name": link.product.name,
            "bank_name": link.bank.name,
            "bank_logo_url": link.bank.logo.url if link.bank.logo else "",
            "connector_name": connector.get_full_name() or connector.username,
            "post_url": f"/onboard/customer/{link_id}/{connector_id}/",
            "redirect_url": link.utm_link
        }

        # 3. Generate HTML from the imported function
        html_content = get_onboarding_html(context_data)

        return HttpResponse(html_content)

    def post(self, request, link_id, connector_id, format=None):
        # (Keep your existing POST logic exactly as it is)
        serializer = CustomerOnboardingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                referrer_user = User.objects.get(id=connector_id)
                if referrer_user.role not in ('ADMIN','STAFF', 'CONNECTOR'):
                    return Response({"detail": "Invalid connector."}, status=400)
            except User.DoesNotExist:
                return Response({"detail": "Invalid connector."}, status=404)
            
            link = get_object_or_404(Link, id=link_id)
            pan = serializer.validated_data['pan']
            
            if Customer.objects.filter(pan=pan).exists():
                return Response({'pan': ['Customer exists.']}, status=400)

            serializer.save(referred_by=referrer_user, referred_for_product=link)

            return Response({
                "message": "Saved",
                "redirect_url": link.utm_link
            }, status=201)
        
        return Response(serializer.errors, status=400)