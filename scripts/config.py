"""
This file holds various configuration options used for all of the scripts.

You will need to change the values below to match your test account.
"""
import os
import sys

# Use the fedex_wrapper directory included in the downloaded package instead of
# any globally installed versions.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fedex_wrapper.config import FedexConfig

# Change these values to match your testing account/meter number.
CONFIG_OBJ = FedexConfig(key='xxxxxxxxxxxx',
                         password='xxxxxxxxxxxx',
                         account_number='xxxxxxxxxxxx',
                         meter_number='xxxxxxxxxxxx',
                         freight_account_number='xxxxxxxxxxxx',
                         use_test_server=True)
