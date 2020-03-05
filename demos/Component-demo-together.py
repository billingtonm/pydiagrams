#! python3

# Example of using the "Together" grouping
# Translation of PUML on https://mrhaki.blogspot.com/2016/12/plantuml-pleasantness-keeping-elements.html

from pydiagrams.Component import ComponentContext as Context

# Select from one of these Helpers (PUML recommended)
from pydiagrams.helpers.Graphviz import Helper
#from pydiagrams.helpers.Blockdiag     import Helper
# from pydiagrams.helpers.PUML     import Helper

# Setup a Component diagram called c
with Context(Helper) as c:
    User = c.Actor('Actor')
    ThirdPartyApp = c.Component("Third party application")

    # Two items that should occur together
    with c.Together():
        PostgresDB = c.Database('PostgreSQL database')
        Mail = c.Component('Mail server')

    with c.Package("Spring Boot Application"):
        Controllers = c.Component('Controllers')
        DataStoreService = c.Component('DataStoreService')
        Repository = c.Component('Repository')

    User >> Controllers
    ThirdPartyApp >> Controllers
    Controllers >> DataStoreService
    DataStoreService >> Repository
    DataStoreService >> Mail
    Repository >> PostgresDB