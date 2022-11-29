#!/usr/bin/env python
"""
This example shows how to create a pickup request and then cancel it
"""
import datetime

from config import CONFIG_OBJ
from fedex_wrapper.services.pickup_service import FedexCreatePickupRequest

pickup_date = datetime.datetime.now().replace(microsecond=0)

customer_transaction_id = "*** PickupService Request v11 using Python ***"  # Optional transaction_id
pickup_service = FedexCreatePickupRequest(CONFIG_OBJ, customer_transaction_id)

pickup_service.OriginDetail.PickupLocation.Contact.PersonName = 'IT Department'
pickup_service.OriginDetail.PickupLocation.Contact.EMailAddress = 'IT@Redcanary.com'
pickup_service.OriginDetail.PickupLocation.Contact.CompanyName = 'Red Canary'
pickup_service.OriginDetail.PickupLocation.Contact.PhoneNumber = '8559770686'
pickup_service.OriginDetail.PickupLocation.Address.StateOrProvinceCode = 'CO'
pickup_service.OriginDetail.PickupLocation.Address.PostalCode = '80202'
pickup_service.OriginDetail.PickupLocation.Address.CountryCode = 'US'
pickup_service.OriginDetail.PickupLocation.Address.StreetLines = ['1601 19th St', 'Suite 900']
pickup_service.OriginDetail.PickupLocation.Address.City = 'Denver'
# pickup_service.OriginDetail.PickupLocation.Address.UrbanizationCode = ''  # For Puerto Rico only
pickup_service.OriginDetail.PickupLocation.Address.Residential = False

# FRONT, NONE, REAR, SIDE
# pickup_service.OriginDetail.PackageLocation = 'NONE'

# APARTMENT, BUILDING, DEPARTMENT, FLOOR, ROOM, SUITE
pickup_service.OriginDetail.BuildingPart = 'SUITE'

# Identifies the date and time the package will be ready for pickup by FedEx.
pickup_service.OriginDetail.ReadyTimestamp = pickup_date.isoformat()

# Identifies the latest time at which the driver can gain access to pick up the package(s)
pickup_service.OriginDetail.CompanyCloseTime = '23:00:00'

pickup_service.CarrierCode = 'FDXE'

pickup_service.TotalWeight.Units = 'LB'

print("")
print("Welcome to Create Pickup! Please enter the total estimated weight (LBs) of your pikcup and press 'Enter'.")
print("")
pickup_service.TotalWeight.Value = input() #If these inputs don't work later both of these data types need to be strings

print("What is the total number of packages you're sending today?")
pickup_service.PackageCount = input()
# pickup_service.OversizePackageCount = '1'

# pickup_service.CommodityDescription = ''

# DOMESTIC or INTERNATIONAL
# pickup_service.CountryRelationship = 'DOMESTIC'

# See PickupServiceCategoryType
# pickup_service.PickupServiceCategory = 'FEDEX_DISTANCE_DEFERRED'

pickup_service.send_request()

print('Pickup request sent:')
print(pickup_service.response.HighestSeverity == 'SUCCESS')
print(pickup_service.response.Notifications[0].Message)

# # Cancel the pickup request that we just got confirmation for
# cancel_pickup = FedexCancelPickupRequest(CONFIG_OBJ)

# cancel_pickup.PickupConfirmationNumber = pickup_service.response.PickupConfirmationNumber
# # the date for the pickup (eg. '2016-09-26')
# cancel_pickup.ScheduledDate = pickup_date.strftime('%Y-%m-%d')
# cancel_pickup.EndDate = pickup_date.strftime('%Y-%m-%d')
# cancel_pickup.Location = pickup_service.response.Location
# cancel_pickup.Remarks = None
# cancel_pickup.ShippingChargesPayment =  None
# cancel_pickup.Reason = ''
# cancel_pickup.ContactName = 'Sender Name'
# cancel_pickup.PhoneNumber = '9012638716'
# cancel_pickup.PhoneExtension = ''

# cancel_pickup.CarrierCode = 'FDXE'

# cancel_pickup.send_request()

# print('Cancel pickup request sent:')
# print('Highest severity:',cancel_pickup.response.HighestSeverity)
# print('Message:',cancel_pickup.response.Notifications[0].Message)
