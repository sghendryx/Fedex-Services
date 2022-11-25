#!/usr/bin/env python
import logging
import binascii
import datetime
import sys
import os

from config import CONFIG_OBJ
from fedex_wrapper.services.ship_service import FedexProcessShipmentRequest

print("")
print("Hello! Please enter the first and last name of the person you are shipping to.")
print("Type your answer and hit 'Enter'.")
recipient_name = input()

print("")
print("Phone number:")
recipient_phone_number = input()

print("")
print("Street Address:")
recipient_address = input()

print("")
print("City:")
recipient_city = input()

print("")
print("Sate Code:")
recipient_state = input()

print("")
print("Zip Code:")
recipient_zipcode = input()

# Generates the shipping label as a PDF.
GENERATE_IMAGE_TYPE = 'PDF'

# Un-comment to see the response from Fedex printed in stdout.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# This is the object that will be handling our shipment request.
# We're using the FedexConfig object from config.py in this dir.
customer_transaction_id = "*** ShipService Request v17 using Python ***"  # Optional transaction_id
shipment = FedexProcessShipmentRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id)

# This is very generalized, top-level information.
# REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER or STATION
shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'

# Type of shipping, you can choose from:
# STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER,
# FEDEX_2_DAY, INTERNATIONAL_PRIORITY, SAME_DAY, INTERNATIONAL_ECONOMY
shipment.RequestedShipment.ServiceType = 'FEDEX_2_DAY'

# What kind of package this will be shipped in.
# FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING, FEDEX_ENVELOPE
shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

# Shipper contact info.
shipment.RequestedShipment.Shipper.Contact.PersonName = 'IT Department'
shipment.RequestedShipment.Shipper.Contact.CompanyName = 'Red Canary'
shipment.RequestedShipment.Shipper.Contact.PhoneNumber = '8559770686'

# Shipper address.
shipment.RequestedShipment.Shipper.Address.StreetLines = ['1601 19th St Suite 900']
shipment.RequestedShipment.Shipper.Address.City = 'Denver'
shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'CO'
shipment.RequestedShipment.Shipper.Address.PostalCode = '80202'
shipment.RequestedShipment.Shipper.Address.CountryCode = 'US'
shipment.RequestedShipment.Shipper.Address.Residential = True

# Recipient contact info.
shipment.RequestedShipment.Recipient.Contact.PersonName = recipient_name
shipment.RequestedShipment.Recipient.Contact.PhoneNumber = recipient_phone_number

# Recipient address
shipment.RequestedShipment.Recipient.Address.StreetLines = recipient_address
shipment.RequestedShipment.Recipient.Address.City = recipient_city
shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = recipient_state

shipment.RequestedShipment.Recipient.Address.PostalCode = recipient_zipcode
shipment.RequestedShipment.Recipient.Address.CountryCode = 'US'
# This is needed to ensure an accurate rate quote with the response. Use AddressValidation to get ResidentialStatus
shipment.RequestedShipment.Recipient.Address.Residential = True
shipment.RequestedShipment.EdtRequestType = 'NONE'

# Senders account information
shipment.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber = CONFIG_OBJ.account_number

# Who pays for the shipment?
# RECIPIENT, SENDER or THIRD_PARTY
shipment.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

# Specifies the label type to be returned.
# LABEL_DATA_ONLY or COMMON2D
shipment.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'

# Specifies which format the label file will be sent to you in.
# DPL, EPL2, PDF, PNG, ZPLII
shipment.RequestedShipment.LabelSpecification.ImageType = GENERATE_IMAGE_TYPE

# To use doctab stocks, you must change ImageType above to one of the
# label printer formats (ZPLII, EPL2, DPL).
# See documentation for paper types, there quite a few.
shipment.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_7X4.75'

# Timestamp in YYYY-MM-DDThh:mm:ss format, e.g. 2002-05-30T09:00:00
shipment.RequestedShipment.ShipTimestamp = datetime.datetime.now().replace(microsecond=0).isoformat()

# This indicates if the top or bottom of the label comes out of the
# printer first.
# BOTTOM_EDGE_OF_TEXT_FIRST or TOP_EDGE_OF_TEXT_FIRST
shipment.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'TOP_EDGE_OF_TEXT_FIRST'

# Delete the flags we don't want.
# Can be SHIPPING_LABEL_FIRST, SHIPPING_LABEL_LAST or delete
if hasattr(shipment.RequestedShipment.LabelSpecification, 'LabelOrder'):
    del shipment.RequestedShipment.LabelSpecification.LabelOrder  # Delete, not using.

# Create Weight, in pounds, according to what item you're sending. If not a laptop or a monitor,
# you can select 'Other' to input the values yourself.
package1_weight = shipment.create_wsdl_object_of_type('Weight')
package1_insure = shipment.create_wsdl_object_of_type('Money')

print("")
print("Are you shipping a laptop, monitor, or other?")
print("Type your answer and hit 'Enter'.")
answer = input()
equipment_type = answer

if answer == "Laptop" or answer == "laptop":
    print("")
    print("Are you shipping a monitor with this as well? Y/N")
    answer = input()
    if answer == "Y" or answer == "y":
        print("generate a monitor shipping label as well")
    package1_weight.Value = 10.0
    package1_weight.Units = "LB"

    # Insured Value of Laptop
    package1_insure.Currency = 'USD'
    package1_insure.Amount = 2000.0

elif answer == "Monitor" or answer == "monitor":
    package1_weight.Value = 15.0
    package1_weight.Units = "LB"

    # Insured Value of Monitor
    package1_insure.Currency = 'USD'
    package1_insure.Amount = 500.0

elif answer == "Other" or answer == "other":
    print("")
    print("Weight of package (LBs):")
    weight = 10.0
    package1_weight.Value = weight
    package1_weight.Units = "LB"

    print("")
    print("Insured value of the package contents:")
    package1_insure.Currency = 'USD'
    package1_insure.Amount = 200.0

else: 
    print("")
    print("I didn't quite catch that. Try again?")

# Create PackageLineItem
package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
# BAG, BARREL, BASKET, BOX, BUCKET, BUNDLE, CARTON, CASE, CONTAINER, ENVELOPE etc..
package1.PhysicalPackaging = 'BOX'
package1.Weight = package1_weight

# Add Insured and Total Insured values.
package1.InsuredValue = package1_insure
shipment.RequestedShipment.TotalInsuredValue = package1_insure

# This adds the RequestedPackageLineItem WSDL object to the shipment. It
# increments the package count and total weight of the shipment for you.
shipment.add_package(package1)

# Fires off the request, sets the 'response' attribute on the object.
shipment.send_request()

# Here is the overall end result of the query.
print("HighestSeverity: {}".format(shipment.response.HighestSeverity))

# Getting the tracking number from the new shipment.
print("Tracking #: {}"
      "".format(shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber))

# Net shipping costs. Only show if available. Sometimes sandbox will not include this in the response.
CompletedPackageDetails = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0]
if hasattr(CompletedPackageDetails, 'PackageRating'):
    print("Net Shipping Cost (US$): {}"
          "".format(CompletedPackageDetails.PackageRating.PackageRateDetails[0].NetCharge.Amount))
else:
    print('WARNING: Unable to get shipping rate.')

ascii_label_data = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].Label.Parts[0].Image

# Convert the ASCII data to binary.
label_binary_data = binascii.a2b_base64(ascii_label_data)

"""
This is an example of how to dump a label to a local file.
"""
# This will be the file we write the label out to.
recipient_name = recipient_name.replace(' ', '_')
recipient_name = recipient_name.replace("'", "")
out_path = (f'{recipient_name}_{equipment_type}.%s') % GENERATE_IMAGE_TYPE.lower()
print("Writing to file {}".format(out_path))
out_file = open(out_path, 'wb')
out_file.write(label_binary_data)
out_file.close()
os.system(f"open {out_path}")
