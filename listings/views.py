from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from decimal import Decimal

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from realtors.models import Realtor
from .serializers import ListingSerializer
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import Listing
import datetime
def index(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }

  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': listing
  }

  return render(request, 'listings/listing.html', context)

def search(request):
  queryset_list = Listing.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # State
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      queryset_list = queryset_list.filter(state__iexact=state)

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET
  }

  return render(request, 'listings/search.html', context)


@api_view(['GET', 'POST', 'DELETE'])
def listing_list(request):
    
    if request.method == 'GET':
        tutorials = Listing.objects.all()
        print("*****************",request.query_params)
        
        title = request.query_params.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = ListingSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        print("REQUEST",request.POST)
        tutorial_data = JSONParser().parse(request)
        obj=Realtor.objects.filter(email='shivam@gmail.com').first()
        
        if obj is not None:
          
          tutorial_serializer = ListingSerializer(data=tutorial_data)
          data=datetime.datetime.now(tz=timezone.utc)
          
          if tutorial_serializer.is_valid():
              
              tutorial_serializer.save()
              
              return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
          return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
          
          data=datetime.datetime.now(tz=timezone.utc)
          
          obj=Realtor(name=tutorial_data['realtor'],email=tutorial_data['realtor'],phone='1234455',hire_date=data)
          if obj.is_valid:
            obj.save()
            tutorial_serializer = ListingSerializer(data=tutorial_data)
            if tutorial_serializer.is_valid():
                tutorial_serializer.save()
                return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

          #obj=Realtor(name='kanishk',description='SignuP through chatbot',phone='3243535344',email='kanishkg@gmail.com')
    
    elif request.method == 'DELETE':
        count = Listing.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def listing_detail(request, pk):
    try: 
        tutorial = Listing.objects.get(pk=pk) 
    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = ListingSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = ListingSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def listing_list_published(request):
    tutorials = Listing.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = ListingSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)