from rest_framework import serializers 
from .models import Listing
 
 
class ListingSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Listing
        fields = ('address',
                  'title',
                  'city',
                  'state','zipcode','price','bedrooms','sqft','bathrooms','lot_size','realtor')