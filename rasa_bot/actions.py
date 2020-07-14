# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


import logging
from datetime import datetime
from typing import Text, Dict, Any, List
import json
import requests


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ConversationPaused
from rasa_sdk import Action, Tracker
import smtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)



#Custom Code Starts Here


class ActionSearchProperty(Action):
    """
    Search the property using location .
    Required Parameters: Location
    """
    def name(self) -> Text:
        return "action_search_property"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print()
        print("====Inside ActionSearchProperty====")
        print()

        ## extract the required slots
        location=tracker.get_slot("location")
        # lat=tracker.get_slot("latitude")
        # lon=tracker.get_slot("longitude")
        # entity_id=tracker.get_slot("location_id")
        # entity_type=tracker.get_slot("location_type")
        # city_id=tracker.get_slot("city_id")

        # ## extract the entities
        # locationEntity=next(tracker.get_latest_entity_values("location"), None)
        # user_locationEntity=next(tracker.get_latest_entity_values("user_location"), None)
        # latEntity=next(tracker.get_latest_entity_values("latitude"), None)
        # lonEntity=next(tracker.get_latest_entity_values("longitude"), None)

        # ## if we latitude & longitude entities are found, set it to slot
        # if(latEntity and lonEntity):
        #     lat=latEntity
        #     lon=lonEntity
        
        # ## if user wants to search restaurants in his current location
        # if(user_locationEntity or (latEntity and lonEntity) ):
        #     ##check if we already have the user location coordinates stoed in slots
        #     if(lat==None and lon==None):
        #         dispatcher.utter_message(text="Sure, please allow me to access your location 🧐",json_message={"payload":"location"})
                
        #         return []
        #     else:
        #         pass
        # ## if user wants to search property by location name
        # if(locationEntity):
        #     print("The locationEntity is ",locationEntity)
           
        #     entity_id=locationEntities["entity_id"]
        #     entity_type=locationEntities["entity_type"]
        #     city_id=locationEntities["city_id"]
        #     SlotSet("location", locationEntities["title"])

      
        
        # print("Entities:  ",entity_id," ",entity_type," ",cuisine_id," ",location," ")
        # print()
        dispatcher.utter_message("Sorry we couldn't find any property that serves {}  😞".format(location))
        return [UserUtteranceReverted()] 

           
class ActionSearchBestProperty(Action):
    """
    Search the best property using location.
    
    Required Parameters: Location
    """
    def name(self) -> Text:
        return "action_search_best_property"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print()
        print("======Inside Action Search Best Property====")
        print()

        ## extract the required slots
        location=tracker.get_slot("location")
        # lat=tracker.get_slot("latitude")
        # lon=tracker.get_slot("longitude")
        # entity_id=tracker.get_slot("location_id")
        # entity_type=tracker.get_slot("location_type")
        # city_id=tracker.get_slot("city_id")

        ## extract the entities
        locationEntity=next(tracker.get_latest_entity_values("location"), None)
        # user_locationEntity=next(tracker.get_latest_entity_values("user_location"), None)
        # latEntity=next(tracker.get_latest_entity_values("latitude"), None)
        # lonEntity=next(tracker.get_latest_entity_values("longitude"), None)

        ## if we latitude & longitude entities are found, set it to slot
        # if(latEntity and lonEntity):
        #     lat=latEntity
        #     lon=lonEntity

        ## if user wants to search the best restaurants in his current location
        # if(user_locationEntity or (latEntity and lonEntity) ):
        #     ##check if we already have the user location coordinates stoed in slots
        #     if(lat==None and lon==None):
        #         dispatcher.utter_message(text="Sure, please allow me to access your location 🧐",json_message={"payload":"location"})
              
        #         return []
        #     else:
        #         pass

        ## if user wants to search best restaurants by location name
        # if(locationEntity):
        #     locationEntities=zomatoApi.getLocationDetailsbyName(locationEntity)
        #     entity_id=locationEntities["entity_id"]
        #     entity_type=locationEntities["entity_type"]
        #     city_id=locationEntities["city_id"]

        #print("Entities: ",entity_id," ",entity_type," ",city_id," ",locationEntity)
        
        ## search the best restaurts by calling zomatoApi api
        #restaurants=zomatoApi.getLocationDetails(entity_id,entity_type)
        

        dispatcher.utter_message("Sorry we couldn't find any property that serves {}  😞".format(location))
        return [UserUtteranceReverted()] 

class GetPincode(Action):
    """
    Search the best property using location.
    
    Required Parameters: Location
    """
    def name(self) -> Text:
        return "get_pincode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print()
        print("======Inside Action Get Pincode====")
        print()
        pincode=tracker.get_slot("pincode")
        pincodeEntity=next(tracker.get_latest_entity_values("pincode"), None)
        dispatcher.utter_message("Sorry we couldn't find any property that serves at this pincode {}  😞".format(pincode))
        return [UserUtteranceReverted()] 

        
class DaysOffMail(Action):

  def name(self) -> Text: 
      return "action_check_restaurants"
  
    
  def run(self, dispatcher, tracker, domain):
      to_email=tracker.get_slot('email')
      location=tracker.get_slot('location')
      name=tracker.get_slot('name')
      intentions=tracker.get_slot('buy_property')
      pincode=tracker.get_slot('pincode')
      buy_slots=['buy','view','show','buying']
      result=[True if i in buy_slots else False for i in intentions.split(' ')]

      if any(result)==True:
        if location:
            print("===================*********** BUY **************===============")
            stri='http://localhost:8000/listings/search?keywords=&city=%s'%(location.split(' ')[1])
          
            dispatcher.utter_message("Hi {} as per your need we have fetched few property for you at  {} You can visit {} 😞".format(name,location.split(' ')[1],stri))
      
        else:
            stri='http://localhost:8000/listings/'
            dispatcher.utter_message("Hi {} as per your need we have fetched few property for you You can visit {} 😞".format(name,stri))


      else:
        if location:
            print("===================*********** SELLL **************===============")
            budget=tracker.get_slot('budget_sell')
            url = "http://localhost:8000/listings/api/listing"
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache"}
            payload = {"realtor":1,"sqft":2000,"city":location.split(' ')[1],\
            "address":location.split(' ')[1],"zipcode":pincode,"title":name,\
            "state":location.split(' ')[1],"price":budget,"bedrooms":2,"bathrooms":2,
            "lot_size":2000}
            
            response = requests.request("POST", url, data=payload, headers=headers)
            print("RESPONSE",response.status_code)
            if response.status_code==200:
                dispatcher.utter_message("Hi {} we have successfully listed your property {} :)".format(name,response.text))
                return [UserUtteranceReverted()] 
            else:
                dispatcher.utter_message("Sorry we cant list your proprty right now please come back later 😞".format(name,response.text))
                return [UserUtteranceReverted()] 
                
      return [UserUtteranceReverted()] 


    #   msg = EmailMessage()
    #   msg['Subject'] = 'Days Off Request'
    #   msg['From'] = 'kanishkgupta1998@gmail.com'  #sender's email address
    #   msg['To'] = to_email  #receiver's email address
    #   msg.set_content('Hi,\nOur member {} has submitted a days off request starting from {} to {} (if both dates are same, its a one day leave request). The reason\ for the leave request is \"{}\" currently \"{}\". Please acknowledge this request. \nYour\'s sincerely,\nYour-bot') 
    #   with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    #     smtp.login('kanishkgupta1998@gmail.com', 'Kaku123niec@')	#replace with your email and password
    #     smtp.send_message(msg)
      
class Action_Send_Listing(Action):

  def name(self) -> Text: 
      return "action_send_listing"
  
    
  def run(self, dispatcher, tracker, domain):
      to_email=tracker.get_slot('email')
      location=tracker.get_slot('location')
      name=tracker.get_slot('name')
      pincode=tracker.get_slot('pincode')
      budget=tracker.get_slot('budget_sell')
      url = "http://localhost:8000/listings/api/listing"
      headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"}
      payload = {"realtor":1,"sqft":2000,"city":location.split(' ')[1],\
      "address":location.split(' ')[1],"zipcode":pincode,"title":name,\
      "state":location.split(' ')[1],"price":budget,"bedrooms":2,"bathrooms":2,
      "lot_size":2000}
      
      response = requests.request("POST", url, data=payload, headers=headers)
      print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",response)
      if response.status_code==200:
        dispatcher.utter_message("Hi {} we have successfully listed your property {} :)".format(name,response.text))
        return [UserUtteranceReverted()] 
      else:
        dispatcher.utter_message("Sorry we cant list your proprty right now please come back later 😞".format(name,response.text))
        return [UserUtteranceReverted()] 
          

