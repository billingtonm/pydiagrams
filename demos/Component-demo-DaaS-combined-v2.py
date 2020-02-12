# This version demonstrates the functionality for Component groups to be 'anonymous'
# ie: instead of
## with ComponentContext(...) as x:
##    with x.Frame('My Group') as MYGROUP:
##       foo = MYGROUP.Component('foo')
# Have this instead:
## with ComponentContext(...) as x:
##    with x.Frame('My Group'):
##          foo = x.Component('foo')

from pydiagrams.Component import *

# Select from one of these Helpers (PUML recommended)
# from pydiagrams.helpers.Graphviz import Helper
from pydiagrams.helpers.PUML     import Helper
#from pydiagrams.helpers.GraphML     import Helper
# from pydiagrams.helpers.arcentry     import Helper


SystemFill='#b9CDe5'
Helper.theme = r'w:\plantuml\theme-woolworths.iuml'

# Project attributes
connected_retail = {fillcolor:color3}
martech = {fillcolor:color7}

DPI=72
WIDTH=180/DPI
PAD=15/DPI

with ComponentContext(Helper) as x:
    x.attrs = {'width':WIDTH}

    # Define some shortcuts for functions
    F=x.Frame
    C=x.Component
    I=x.Interface
    N=x.Node
    D=x.Database

    with F('Amazon Web Services') as aws:
        with F('S3') as aws_s3:
            aws_s3_img = N('Image and Video Storage')

        with F('RDS') as aws_rds:
            aws_rds_inv = D('Inventory')

    with F('Data As a Service', fillcolor=SystemFill) as daas:
        
        with F('API Gateway') as daas_api_gw:
            daas_pers_api       = I('Personalisation APIs')
            daas_ml_api         = I('ML APIs')
            daas_cust_api       = I('Customer APIs')
            daas_inv_api        = I('Inventory APIs')
            daas_price_api      = I('Pricing APIs')
            daas_product_apis   = I('Product APIs')
            daas_orders_apis    = I('Order APIs')

        with F('Services') as daas_services:
            with F('Personalisation', **connected_retail) as daas_pers:
                prec = C('Product Recs')
                offers = C('Offers')
                daas_pers_api << daas_pers.all_except(shape=Interface)

            with F('Machine Learning', **martech) as daas_ml:
                cda =       C('Core Analytics')
                denrich =   C('Data Enrichment')
                seg =       C('Advanced Clustering')
                daas_ml_api << daas_ml.all_except(shape=Interface)

            with F('Customer Services', **connected_retail) as daas_cust:
                uci = C('Unified Customer Identity')
                daas_cust_api << daas_cust.all_except(shape=Interface)

            with F('Inventory', **connected_retail) as daas_inv:
                avail =         C('Availability Service')
                inv =           C('Inventory Service')
                find_in_store = C('Find In Store')
                if False: #Optionally show more detail
                    inv_monitor = C('Inventory Monitor')
                    inv_db = D('Inventory DB')
                    inv << inv_monitor << inv_db
                inv << aws_rds_inv

                daas_inv_api << daas_inv.all_except(shape=Interface)

            with F('Pricing', **connected_retail) as daas_price:
                price =         C('Price')
                order_calc =    C('Order Calculation')
                promotions =    C('Promotions')

                daas_price_api << daas_price.all_except(shape=Interface)

            with F('Product', **connected_retail) as daas_product:
                image_service =     C('Images')
                product_feed =      C('Product Feeds')
                product_service =   C('Product Service')

                daas_product_apis << daas_product.all_except(shape=Interface)
                image_service << aws_s3_img

            with F('Orders', **connected_retail) as daas_orders:
                orders =        C('Orders')
                fulfilment =    C('Fulfillment')

                daas_orders_apis << daas_orders.all_except(shape=Interface)

        daas_dal      = C('Data Abstraction', width=len(daas_services.all()) * (PAD+WIDTH))

        daas_raw                = N('Raw')
        daas_business_layer     = N('Business Layer')
        daas_redshift           = D('Redshift')        
        
        daas_bi = I('BI')
        daas_athena = I('Athena')

        daas_raw ^ daas_business_layer ^ daas_redshift >= daas_bi
        daas_business_layer >= daas_athena

        daas_dal ^ daas_services.all()
        all_services = daas_services.all()
        daas_business_layer >> daas_dal

    with F('Google Cloud Platform') as gcp:
        ga360 = C('GA360')
        dv360 = C('DV360')
        sa360 = C('SA360')
        gcs =   N('Cloud Storage')
        gbq =   D('BigQuery')

        gcs ^ gcp.all_except(gcs) # Link gcs to all other Items in gcp

    with F('Systems of Engagement') as soe:
        soe_int = I('Interface')
        soe_api = I('APIs')

        with F('Customer Engagement') as soe_ce:
            sfmc = C('SFMC')
            digm = C('[Digital Marketing]')
            dync = C('Movable Ink [Dynamic Content]')            
            cself = C('Customer Self Service')
            awsconn = C('Amazon Connect')

        with F('POS / Smart Checkout') as soe_pos:
            pos     = C('POS')
            sexp    = C('Store Experience')

        with F('Mobile') as soe_mobile:
            mobile = C('Customer Mobile App')

        with F('Online Commerce') as soe_web:
            ec  = C('Headless UX')
            sli = C('SLI [Search]')
            ecp = C('eCommerce Content Personalisation')

        # Link apis to all SOE systems
        soe_api ^ soe.all_except(soe_int, soe_api) 

    with F('Integration') as integration:
        ait  = C('AIT')
        infm = C('Informatica')
        
        soe_int << integration.all() # link to all items

    with F('Systems of Record') as sor:
        cdc =       I('Change Database Capture (DMS)')
        saas_dal =  I('SaaS Connectors')
        dbconn =    I('Database Connectors')
        sor_int =   I('SOR Interfaces')

        with F('Financials') as sor_fin:
            crgfin  = C('CRG OraFin')
            djfin   = C('DJ OraFin')

        with F('Merchandise & Supply Chain Systems') as sor_mer:
            djrms   = C('DJ RMS')
            crgrms  = C('CRG RMS')

        with F('Sales Transaction Systems') as sor_sales:
            edw     = C('EDW')
            djpos   = C('DJ POS')
            crgpos  = C('CRG POS')

        with F('Customer Systems', **martech) as sor_customer:
            sor_customer_int = I('Connectors')
            sfdc =      C('SFDC')
            srvy =      C('GetFeedback [Surveys]')
            cmpgn =     C('[Campaign  Management]') 
            loyalty =   C('[Loyalty]')           
            identity =  C('[Identity and AccessManagement]', **connected_retail)

            sor_customer_int << sor_customer.all_except(sor_customer_int)

        with F('eCommerce', **connected_retail) as sor_ecomm:
            sor_ecomm_int = I('Connectors')
            isams =         C('iSAMS')
            pim =           C('[Product Information Management]')
            dam =           C('[Digital Asset Management]')
            search =        C('SLI Search')
            cms =           C('CMSaaS')
            payment =       C('Payment Gateway')
            price_promo =   C('[Price and Promotions Engine]')
            sor_ecomm_int << sor_ecomm.all_except(sor_ecomm_int)

        saas_dal <<  sor_ecomm_int
        saas_dal << sor_customer_int

        # link cdc to all items in sor_mer, sor_fin, sor_sales
        db_systems = sor_mer.all() + sor_fin.all_except(djfin) + sor_sales.all()
        cdc << dbconn
        cdc ^ daas_raw

        dbconn << db_systems

        daas_dal << [dbconn , saas_dal]
        saas_dal << djfin

        sor_int ^ integration.all()
        sor_int << dbconn

    daas_raw <= gcs
    gcs >> daas_raw 

    soe_int ^ sfmc 

    soe_api << daas_api_gw.all()

    infm >> gcs

print ('-'*80)
print(f'showing x: {x=} {type(x)=}')
print(f'{x.parent=}')

print(x.__str__)