from rest_framework import serializers 
from .models import CompanyModel, CompanyStockInformation

class CompanyModelSerializer(serializers.ModelSerializer):
    company_id = serializers.CharField(source='id')
    class Meta:
        model = CompanyModel
        fields = ['company_id', 'company_name']

# A nested serializer for the stock information; it creates the company if it isn't listed and adds the stock
# to the existing company if it does. 
class CompanyStockInformationSerializer(serializers.ModelSerializer):
    company = CompanyModelSerializer()
    class Meta:
        model = CompanyStockInformation
        fields = [
            'id', 'company', 'number_of_transactions',
            'maximum', 'minimum', 'closing', 'traded_shares',
            'amount', 'previous_closing', 'difference_rs', 'date_added'
        ]
    
    def create(self, validated_data):
        company_data = validated_data.pop('company')
        company, created = CompanyModel.objects.get_or_create(**company_data)
        stock, created_ = CompanyStockInformation.objects.get_or_create(company=company, **validated_data)
        return stock