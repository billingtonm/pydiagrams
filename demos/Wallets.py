from pydiagrams.AWS import AWSContext as Context
from pydiagrams.helpers.PUML_AWS import Helper


with Context(Helper) as c:

    SFObject = c.Salesforce
    S3 = c.AmazonSimpleStorageServiceS3
    Lambda = c.AWSLambda
    lambdaFn = c.AWSLambda_LambdaFunction
    SNS = c.AmazonSimpleNotificationServiceSNS

    with c.Cloud('Salesforce'):
        sf_customer = SFObject('Customers')
        sf_benefits = SFObject('Rewards and Offers')

    with c.Frame('DaaS') as aws:
        customer_bucket = S3('Customer Bucket')
        benefits_bucket = S3('Benefits Bucket')

        aws_database = c.Genericdatabase('Benefits DB')
        
        aws_lambda_customer = Lambda('Customer Delta')
        aws_lambda_benefits = Lambda('Benefits Delta')

        customer_bucket >> aws_lambda_customer % 'Called as S3 Event'
        benefits_bucket >> aws_lambda_benefits 

        aws_lambda_exp = Lambda("Batch Expiring Offers", note='Scheduled Task\nFinds benefits that have expired')
        aws_database >> aws_lambda_exp % {'label':'Expired Offers', 'color':'blue'}
        
        aws_sns_cust = SNS("SNS Topic: Customer Delta")
        aws_sns_benefits = SNS("SNS Topic: Benefits Delta")

        aws_lambda_customer >> aws_sns_cust % 'Publishes Event'
        aws_lambda_benefits >> aws_sns_benefits % 'Publishes Event'
        aws_lambda_exp >> aws_sns_benefits % 'Publishes Event'

        aws_wallets = Lambda('Wallets Subscriber', note='Fetches data about customer and benefits, and makes API call.')
        
        with c.Package('Customer Endpoint'):
            api_benefits_api = lambdaFn('GetBenefits')
            api_customer_api = lambdaFn('GetCustomer')

        api_customer_api >> aws_wallets #% 'Provides customer data'
        api_benefits_api >> aws_wallets #% 'Provides benefits data'

        aws_database <= [api_customer_api, api_benefits_api]

        aws_sns_cust >> aws_wallets % 'Subscribed by'
        aws_sns_benefits >> aws_wallets % 'Subscribed by'

    with c.Frame('Wallets Solution'):
        GW=c.Component
        wallets_apigw = GW('API Gateway')
        wallets_update_api = Lambda('Wallet Update API')

        wallets_updates_ios       = c.Apple('iOS')
        wallets_updates_android   = c.Android('Android')
        wallets_updates_fbloyalty = c.Facebook('FB Loyalty')
        wallets_updates_stocard    = c.Component('Stocard')


        wallets_update_api >> [wallets_updates_ios, wallets_updates_android, wallets_updates_fbloyalty, wallets_updates_stocard]



    sf_customer >> customer_bucket % 'Changes as JSON via Informatica'
    sf_benefits >> benefits_bucket

    aws_wallets >> wallets_apigw % 'Calls through to. API includes all the data'
    wallets_apigw >> wallets_update_api