from __future__ import print_function
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
import json
import xml.etree.ElementTree as ET

old_tree = ET.parse("/home/alex/Downloads/Intrusion_Prevention_Rules.xml")
new_tree = ET.parse("/home/alex/Downloads/Intrusion_Prevention_Rules(1).xml")

# looking for a UserEdited tag
old_root = old_tree.getroot()
new_root = new_tree.getroot()

for child in new_root.iter("PayloadFilter2"):
    for baby in child.iter("UserEdited"):
        if baby.text == "true":
            rule_id = child.attrib["id"]
            print(rule_id)

# for child in new_root.iter("UserEdited"):
#     if child.text == "true":
#         print("cowabunga")
