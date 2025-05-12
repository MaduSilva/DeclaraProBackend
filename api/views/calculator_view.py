from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .permissions import IsCustomerOrAdmin, IsCustomer
from api.auth import CustomerAuthentication
from rest_framework.response import Response 
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Enter the token in format: 'Bearer' + token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'income': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'inss': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'private_pension': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'paid_irrf': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'dependents': openapi.Schema(type=openapi.TYPE_INTEGER),
                'education': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'health': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'alimony': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
            },
            required=['income', 'inss', 'private_pension', 'paid_irrf', 'dependents', 'education', 'health', 'alimony']
    ),
)
@api_view(['POST'])
@authentication_classes([CustomerAuthentication])
@permission_classes([IsCustomer])
def calculateIRPF(request):
    try:
        income = request.data.get("income", 0)
        inss = request.data.get("inss", 0)
        private_pension = request.data.get("private_pension", 0)
        paid_irrf = request.data.get("paid_irrf", 0)
        dependents = request.data.get("dependents", 0)
        education = request.data.get("education", 0)
        health  = request.data.get("health", 0)
        alimony = request.data.get("alimony", 0)

        detailed_deduction = (
            inss +
            min(private_pension, 0.12 * income) +
            (dependents  * 2275.08) +
            min(education, 3561.50) +
            health +
            alimony
        )

        simplified_deduction = min(income * 0.20, 16754.34)

        best_deduction = max(simplified_deduction, detailed_deduction)

        taxable_amount = max(0, income - best_deduction)

        # exercício de 2026 (ano calendário de 2025)
        tableIRPF = [
            {
                "min_amount": 0.00,
                "max_amount": 27110.40,
                "rate": 0.0,
                "deduction": 0.0
            },
            {
                "min_amount": 27110.41,
                "max_amount": 33919.80,
                "rate": 0.075,
                "deduction": 2033.28
            },
            {
                "min_amount": 33919.81,
                "max_amount": 45012.60,
                "rate": 0.15,
                "deduction": 4577.27
            },
            {
                "min_amount": 45012.61,
                "max_amount": 55976.16,
                "rate": 0.225,
                "deduction": 7953.21
            },
            {
                "min_amount": 55976.17,
                "max_amount": float("inf"),
                "rate": 0.275,
                "deduction": 10752.02
            }
        ]

        tax_due = 0.0
        for item in tableIRPF:
            if item["min_amount"] < taxable_amount <= item["max_amount"]:
                tax_due = taxable_amount * item["rate"] - item["deduction"]
                break


        tax_due = max(0, tax_due)

        amountDifference = paid_irrf - tax_due
        isRefund = amountDifference > 0

        return Response({
            "taxable_amount": round(taxable_amount, 2),
            "tax_due": round(tax_due, 2),
            "paid_irrf": round(paid_irrf, 2),
            "amountDifference": round(abs(amountDifference), 2),
            "isRefund": isRefund,
            "deduction": "Detailed" if detailed_deduction > simplified_deduction else "Simplified"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)