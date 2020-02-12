from pydiagrams.AWS import AWSContext as Context
from pydiagrams.Diagram import Items

# Need to use a helper that can understand AWS syntax, eg: PUML_AWS
from pydiagrams.helpers.PUML_AWS import Helper
# from pydiagrams.helpers.Graphviz_AWS import Helper

with Context(Helper) as c:

    c.passthrough("""
skinparam DiagramBorderThickness 6
skinparam TitleFontSize 36 
title <u>ThirdParty Loyalty Account Link
""")

    DB = c.Genericdatabase
    BUCKET= c.AmazonSimpleStorageServiceS3_Bucket
    Zone = c.Package
    Group = c.Frame

    # Define the Entities replicated in DaaS
    entities = ['Customer', 'Reward', 'Offer']

    with c.Cloud('Salesforce') as sf:
        whlau_crm = DB('CRM DJ/CRG')

    with Group('AWS') as aws:

        with Zone('Raw') as raw:
            raw_items = [BUCKET(e) for e in entities]

        for (item, label) in zip(raw_items, entities):
            whlau_crm >> item % ('Informatica ' + label)

        glue = c.AWSGlue('Glue')

        with Zone('Staged') as staged:
            stg_items = [BUCKET('Staged ' + e) for e in entities]

        aws_rdsLoyalty = c.AmazonRDS('Loyalty RDS')

        # Link each Raw Item to a Glue Item to a Stage Item
        for (r, s) in zip(raw_items, stg_items):
            r >> glue >> s
        
        # The 'Items' class allows a list of items to be used on the LHS of a link
        # Link all staged items to RDS
        Items(*stg_items) >> aws_rdsLoyalty

        with Group('Lambda') as lambda_grp:
            aws_lambda_custAPI = c.AWSLambda("Customer API")

            aws_lambda_ThirdPartyAPI = c.AWSLambda_LambdaFunction("Loyalty Data Upd")
            aws_lambda_GetCustomer = c.AWSLambda_LambdaFunction("Get Customer Id")
            aws_lambda_UpdCustomer = c.AWSLambda_LambdaFunction("Upd Customer Attr")
            aws_lambda_GetBenefits = c.AWSLambda_LambdaFunction("Get Benefits Details ")

            # Link all functions to lambda
            aws_lambda_custAPI >> lambda_grp.all_except(aws_lambda_custAPI)

        # Link stage items to Lambda
        # Items(*stg_items) >> aws_lambda_custAPI

        aws_apigw = c.AmazonAPIGateway("API Gateway")

    with c.Cloud('Third Party'):
        whlau_thirdPartLoyalty = DB('Third Party')

    # APis, upward from 3rd party to lambda via GW
    whlau_thirdPartLoyalty ^ aws_apigw % 'account link / unlink'
    aws_apigw ^ aws_lambda_custAPI % 'account link / unlink'


    aws_lambda_ThirdPartyAPI >> whlau_thirdPartLoyalty % 'Push - Updates, Rewards, Offers'

    aws_rdsLoyalty >> aws_lambda_GetCustomer % 'query data'
    aws_rdsLoyalty >> aws_lambda_GetBenefits % 'query data'
    aws_rdsLoyalty >> aws_lambda_ThirdPartyAPI % 'Deltas'