from pydiagrams.AWS import AWSContext as Context

# Need to use a helper that can understand AWS syntax, eg: PUML_AWS
from pydiagrams.helpers.PUML_AWS import Helper
# from pydiagrams.helpers.Graphviz_AWS import Helper

# These two lines are only needed for debugging during development
# import pydiagrams.baseItems
# pydiagrams.baseItems.log_enabled=False

EMP='Emp'
CONFIG='Config'

with Context(Helper) as c:
    # Define some shortcuts
    BUCKET = c.AmazonSimpleStorageServiceS3_Bucket
    DB = c.Genericdatabase

    Zone = c.Package    # Use the Package container for AWS Zones
    Group = c.Frame     # Use Frame for groups

    # ---------------------------------------------------
    # Start Diagram

    crg_payroll  = DB("Payglobal")
    crg_peopleDB = DB("People DB")    
    
    with c.Database("RMS DB"):
        workplace_config = c.Component( "Workplace Config - RMSDB")

    with c.Cloud("Empower"):
        dj_payroll = DB( "DJ Employees")

    with Group('AWS Cloud / DaaS'):

        dms      = c.AWSDatabaseMigrationService("AWS Database Migration Service")
        aws_sftp = c.AWSTransferforSFTP("AWS Transfer for SFTP")

        with Zone('Landing') as landing:
            aws_landingEmp      = BUCKET(EMP)
            aws_landingConfig   = BUCKET(CONFIG)

        with Zone('Raw') as raw:
            aws_rawEmp      = BUCKET(EMP)
            aws_rawConfig   = BUCKET(CONFIG)

        aws_glue1 = c.AWSGlue("AWS Glue Emp Job")
        aws_glue2 = c.AWSGlue("AWS Glue Config Job")

        with Zone('Staged') as curated:
            aws_curateEmp       = BUCKET(EMP)
            aws_curateConfig    = BUCKET(CONFIG)

        with Group('Lambda') as lambda_group:
            aws_lambda_fbAPI     = c.AWSLambda("AWS Lambda")
            aws_lambda_fbAPI_new = c.AWSLambda_LambdaFunction("New Employee")
            aws_lambda_fbAPI_mod = c.AWSLambda_LambdaFunction("Modify Employee")
            aws_lambda_fbAPI_grp = c.AWSLambda_LambdaFunction("Group Assignment")

            # c1 = c.Custom1('hello')

    with c.Cloud('FB Workplace'):
        workplace_fb = DB('Employees')

    ###############################################
    # Connections
    # >> : normal connection 'to'
    # <= : left
    # >= : right
    # %  : Label of the connection

    # On prem HR DBs ------------------------------
    crg_payroll >= crg_peopleDB % 'Informatica (Existing)'

    dj_payroll <= aws_sftp % 'FTP'
    aws_sftp >> aws_landingEmp

    # To dms : '<<' means from
    crg_peopleDB >> dms
    workplace_config >> dms

    dms >> landing.all() # DMS links to all items in raw

    # AWS ----------------------------------------

    aws_landingEmp >> aws_rawEmp
    aws_landingConfig >> aws_rawConfig

    # Link raw to curated via glue
    aws_rawEmp    >> aws_glue1 % 'via S3 event' >> aws_curateEmp
    aws_rawConfig >> aws_glue2 % 'via S3 event' >> aws_curateConfig

    # Link all Curated items to lambda
    curated.all() >> aws_lambda_fbAPI         

    # Lambdas
    aws_lambda_fbAPI >> lambda_group.all_except(aws_lambda_fbAPI)

    # Link lambdas to FB
    lambda_group.all_except(aws_lambda_fbAPI) >> workplace_fb    
