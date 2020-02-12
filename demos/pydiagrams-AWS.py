from pydiagrams.AWS import AWSContext as Context

# Need to use a helper that can understand AWS syntax, eg: PUML_AWS
from pydiagrams.helpers.PUML_AWS import Helper
# from pydiagrams.helpers.Graphviz_AWS import Helper

# These two lines are only needed for debugging during development
# import pydiagrams.baseItems
# pydiagrams.baseItems.log_enabled=False


with Context(Helper) as c:
    # Define some shortcuts
    BUCKET = c.AmazonSimpleStorageServiceS3_Bucket
    DB = c.Genericdatabase

    Zone = c.Package    # Use the Package container for AWS Zones
    Group = c.Frame     # Use Frame for groups

    # Start diagram here
    