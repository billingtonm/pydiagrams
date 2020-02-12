from pydiagrams.AWS import AWSContext as Context

# Need to use a helper that can understand AWS syntax, eg: PUML_AWS
from pydiagrams.helpers.PUML_AWS import Helper
# from pydiagrams.helpers.Graphviz_AWS import Helper

with Context(Helper) as c:
    # Set up the components, showing the AWS items within a frame
    app = c.Mobileclient("App")
    
    with c.Frame("AWS") as aws:
        gw = c.AmazonAPIGateway("API Gateway")
        f1 = c.Component("Function 1")
        f2 = c.AWSLambda("Function 2")
        f3 = c.AWSLambda("Function 3")
        db = c.AmazonDynamoDB("Dynamo DB")

        fb = c.Facebook('Facebook loyalty')

    # App connects to API gateway
    app >> gw

    # The gateway is a proxy for the lambda function
    gw >> [f1, f2, f3]

    #Some connections between functions
    f1 >= f2 % 'Invokes'
    f3 <= f2 % 'Invokes'

    # Function 2 operates on the database
    f2 | db % "Updates"