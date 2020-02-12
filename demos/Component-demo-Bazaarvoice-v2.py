# Attempting an ideal syntax that uses local variables
# eg:
# instead of defining a component:
#   C('rms_prod', 'Products')
# do this:
#   rms_prod = C('Products')

# Lines:
#       >>  link (vertical arrow)
#       >>= dotted link (vertical dotted)
#       -   horizontal line (no arrows)
#       ==  vertical line  (no arrows)
# With Direction:
#       ^   up
#       >=  right
#       <=  left
#       |   down

from pydiagrams.Component import *
from pydiagrams.helpers.PUML import Helper

with ComponentContext(Helper)  as x:
    # Define some shortcuts for functions
    F=x.Frame
    C=x.Component
    I=x.Interface
    N=x.Node
    D=x.Database
    Cl=x.Cloud

    with x.Database("RMS", fillcolor='#adfcad') as rms:
        rms_prod    = C('Products')
        rms_sales   = C('Sales')
        rms_pf      = I('[DR1] Product Feed')
        rms_sf      = I("[DR2] Sales Feed")
        rms_cra     = I('[DR3] Customer Review Authorisation')

        rms_prod >> rms_pf
        rms_sales >> rms_sf
        rms_sales >> rms_cra


    with F("Biztalk 2016") as bt:
        int_pf = I('[DI1] Product Feed')


    with Cl("Informatica Cloud") as ic:
        with F("Data Integration", fillcolor=white) as di:
            int_sf = I('[DI2] Sales Feed')
            int_cf = I('[DI3] Client Feed')

        with F("Application Integration", fillcolor=white) as ai:
            inf_cra = I("[DA1] Customer Review Authorisation")


    with Cl("BazaarVoice", fillcolor='#d5adfc') as bv:
        bv_pie      = I("Post-interaction email feed")
        bv_pf       = I("Product Feed")
        bv_prod     = C("Products")
        bv_sales    = C("Post Interface Events")
        bv_reviews  = C("Reviews")
        bv_pie  >> bv_sales
        bv_pf   >> bv_prod
        bv_email    = I("Outbound Emails")
        bv_scf      = I("Standard Client Feed")

        bv_sales >> bv_email
        bv_prod  >> bv_email

        bv_reviews ^ bv_scf #Up arrow

    with Cl("iSAMS", fillcolor='#adfcfc') as isams:
        is_prod = C('Products')
        is_pdp  = I('Product Detail Page')
        is_plp  = I('Product Listing Page')
        is_pr   = I('Product Review Page')

        is_prod ^ is_plp #Up
        is_prod ^ is_pdp #Up


    with Cl("Google Cloud Platform / AWS S3", fillcolor='#fcd5ad') as cloud:
        cloud_crm = C('Customer Product Reviews')


    with Cl('Salesforce') as sf:
        sf_crm  = C('Customer Product Reviews', note='Out of Scope')

    # main group
    c = x.Actor('Customer')

    bv_email >> c % "Email"

    rms_pf >> int_pf
    int_pf >> bv_pf % "SFTP"

    rms_sf >> int_sf
    int_sf >> bv_pie % 'SFTP'

    c >> is_pr % "Writes Review"
    is_pr >> bv_reviews

    bv_reviews >> is_plp % "Rating and Review"
    bv_reviews >> is_pdp % "Rating and Review"

    bv_scf ^ int_cf # Up
    int_cf ^ cloud_crm # Up

    sf_crm | cloud_crm %  "via API" #down

    # Customer Review Authorisation
    inf_cra >> rms_cra
    is_pdp >> inf_cra % 'Online Review Auth'


