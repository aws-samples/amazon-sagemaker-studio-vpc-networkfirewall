# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import time
import boto3

sm_client = sm_client = boto3.client('sagemaker')

def delete_apps(domain_id, user_profile_name):
    print("Start deleting user applications..")

    for p in sm_client.get_paginator('list_apps').paginate(DomainIdEquals=domain_id, UserProfileNameEquals=user_profile_name):
        for a in p["Apps"]:
            sm_client.delete_app(DomainId=a["DomainId"], UserProfileName=a["UserProfileName"], AppType=a["AppType"], AppName=a["AppName"])
        
    apps = 1
    while apps:
        apps = 0
        for p in sm_client.get_paginator('list_apps').paginate(DomainIdEquals=domain_id, UserProfileNameEquals=user_profile_name):
            apps += len([a["AppName"] for a in p["Apps"] if a["Status"] != "Deleted"])

        print(f"Number of active apps: {str(apps)}")
        time.sleep(5)

    print("All apps are shutdown")


delete_apps("d-icecisjo29dt", "demouser-profile-us-west-2")