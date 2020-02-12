from pydiagrams.Component import *
# from pydiagrams.helpers.PUML     import Helper
from pydiagrams.helpers.Graphviz     import Helper
# from pydiagrams.helpers.GraphML     import Helper

Helper.output_format = 'svg'

with ComponentContext(Helper) as x:
    F = x.Frame
    P = x.Package
    R = x.Rectangle

    # Group
    G = lambda l: F(l, fillcolor=grey1)
    # System Group
    Sg = lambda l: F(l, fillcolor=grey4)

    # Application
    if Helper.name == 'PUML': 
        app_format = '**{s}**\\n{l}'
    elif Helper.name == 'Graphviz':
        Helper.html_labels = True
        app_format = '<table border="0" cellpadding="0"><tr><td align="center"><B>{s}</B></td></tr><tr><td>{l}</td></tr></table>'
    else:
        app_format = '{s}\\n{l}'

    node_properties = {
        'GraphML':{'width':210, 'height':30}
    }

    App = lambda s,l: R(app_format.format(s=s, l=l), fillcolor='#FFFFFF', **node_properties.get(Helper.name, {}))

    # Component
    C = lambda l: x.Component(l, fillcolor=white)
    # Package
    P = lambda s: F(s, fillcolor=grey3)

    # Company
    if Helper.name == 'PUML':
        cobu_format = '{co} ({bu})'
    else:
        cobu_format = '{co}'

    Company_BusinessUnit = lambda company_name, business_unit, fill: x.Package(cobu_format.format(co=company_name, bu=business_unit), fillcolor=fill)
    # Define region functions for the Companies to use
    DJ   = lambda s=None: Company_BusinessUnit('David Jones', s, color1)
    CRG  = lambda s=None: Company_BusinessUnit('CRG', s, color3)
    PX   = lambda s=None: Company_BusinessUnit('Politix', s, color7)


    show_DJ = False
    # show_DJ = True
    # show_CRG = False
    show_CRG = True
    show_PX = False
    # show_PX = True

    # -------------------------------------------------------------------------------------------------------------------

    # Stores and Operations
    with G('Stores and Operations'):
        
        if show_DJ:
            with DJ('sop'):
                with Sg('POS'):
                    vbs = App('VBS', 'Vision Bean Store')
                    dj_pos = App('VOD', 'Vision On Demand')
                    dj_pceft = App('PC EFTPOS', 'PIN Pads')

                fsis = App('FSIS', 'Frontline Sales Incentive Scheme')
                sim = App('SIM', 'Store Inventory Management')
                # with P('SIM') as sim:
                #     C('Logistics')
                #     C('Inventory')
                #     C('Items')
                #     C('Stocktake')
                #     C('In Store Ordering')
                #     C('Customer Orders')

                App('Reflexis', 'Store Rostering')


                with G('Food'):
                    episys = App('Episys', 'Ticket Printing (Food)')
                    atria= App('Atria', 'Scales (Food)')

        if show_CRG:
            with CRG('sop'):
                crg_pos = App('Magenta', 'Point of Sale')
                App('Dayforce', 'Store Rostering')
                App('LeaseEagle', 'Lease Management')

        if show_PX:
            with PX('sop'):
                px_pos = App('Futura', 'Futura POS')
                px_yr = App('YReceipts', 'Electronic Receipts')
                px_pos >> px_yr

        with G('Payment Services'):
            if show_DJ:
                with DJ('pay'):
                    dj_givex = App('Givex', 'Gift Cards and Laybys')
                    dj_aftpay = App('Afterpay', 'BNPL')
                    dj_netmap = App('NetMap', 'Transaction Fraud Detection')

            with CRG('pay'):
                crg_giftcard = App('Blackhawk', 'Gift Cards and Laybys')
                crg_aftpay = App('Afterpay', 'BNPL')
                crg_netmap = App('NetMap', 'Transaction Fraud Detection')



    # Merchandise
    with G('Merchandise'):

        if show_DJ:
            with DJ('mer'):
                dj_boa = App('BOA', 'Buyers Ordering Assistant')
                dj_rms = App('RMS', 'Merchandising (DJ)')
                dj_rdf = App('RDF', 'Retek Demand Forecasting')
                dj_pro = App('Profectus', 'Vendor Rebate and Deal Management')
                intactix = App('Intactix', 'Space Planning')
                dj_mfp = App('MFP', 'Merchandise Financial Planning (DJ)')

                with G('Food'):
                    dj_fls = App('FLS', 'Food Legislation System')
                    amos = App('AMOS', 'Food Master Data')

                dj_boa >> dj_rms
                dj_rms >> [dj_rdf, dj_fls, amos]

        if show_CRG:
            with CRG('mer'):
                crg_rms = App('RMS', 'Merchandising (CRG)')
                crg_mfp = App('MFP', 'Merchandise Financial Planning')

        if show_PX:
            with PX('mer'):            
                px_rms = App('Futura', 'Merchandising System')


    # Online and Digital
    with G('Online and Digital'):
        if show_DJ:
            with DJ('onl'):
                dj_isams = App('iSAMS', 'eCommerce (DJ)')
                dj_osm = App('OSM', 'Online Store Management (DJ)')        
                cobra = App('COBRA', 'Product Masterfiling')
                dj_admation = App('Admation', 'Digital Asset Management')

                cobra >> dj_osm >> dj_isams
                dj_admation >> dj_isams % 'Images'

        if show_CRG:
            with CRG('onl'):
                crg_isams = App('iSAMS', 'eCommerce (CR,TR,WY,MI)')
                crg_gal = App('Gallery', 'DAM')
                crg_osm = App('OSM', 'Online Store Management')        

                crg_bv = App('BazaarVoice', 'Product Ratings & Reviews')
                crg_sli = App('SLI', 'Product Search')

                with Sg('Google Cloud Platform'):
                    crg_ga  = App('GA', 'Google Analytics')
                    crg_gmc = App('GMC', 'Google Merchant Centre')
                    crg_gad = App('Adwords', 'Google Adwords')
                    crg_gtag = App('GTM', 'Google Tag Manager')

                crg_fb  = App('Facebook', 'Social Audiences')
                crg_fbc = App('Facebook Connect', 'Social')

                crg_isams << [crg_gal, crg_osm]
                crg_isams >> [crg_sli, crg_bv]


        if show_PX:
            with PX('onl'):
                px_sfcc = App('SFCC', 'Saleforce Commerce Cloud')
                px_od = App('OrderDynamics', 'Order Management System')
                px_sfcc >> px_od

    with G('Marketing and CRM'):
        sfmc = App('SFMC', 'Salesforce Marketing Cloud')
        sfdc = App('SFDC', 'Salesforce.com')

        with G('Analytics'):
            if show_DJ:
                with DJ('analytics'):
                    analytics_r = App('R', 'R Studio')
            if show_CRG:
                with CRG('analytics'):
                    analytics_sas = App('SAS', 'SAS Enterprise')

        if show_PX:
            with PX('CRM'):
                px_sfmc = App('SFMC', 'Salesforce Marketing Cloud (PX)')

    with G('Finance'):
        if show_DJ:
            with DJ('fin'):
                with Sg('Oracle Financials (Cloud)'):
                    dj_orafin_gl = App('GL', 'General Ledger (DJ)')
                    dj_orafin_ar = App('AR (DJ)', 'Accounts Receivable')
                    dj_orafin_ap = App('AP (DJ)', 'Accounts Payable')

                    dj_orafin_gl << [dj_orafin_ar, dj_orafin_ap]

                #dj_orafin = App('Finacials', 'Oracle Financials (Cloud)')
                dj_epm = App('EPM', 'Financial Reporting')
                dj_eftrec = App('EFTREC', 'EFT Reconciliation')
                dj_tm1 = App('TM1', 'Financial Reporting')
                dj_quantum = App('Quantum', 'Treasury')

                dj_orafin_gl >> [dj_epm, dj_tm1, dj_quantum]

        if show_CRG:
            with CRG('fin'):
                # crg_orafin = App('Finacials', 'Oracle Financials (EBS)')
                with Sg('Oracle Financials') as crg_orafin:
                    crg_orafin_gl = App('GL', 'General Ledger (CRG)')
                    crg_orafin_ar = App('AR', 'Accounts Receivable (CRG)')
                    crg_orafin_ap = App('AP (DJ)', 'Accounts Payable')

                    crg_orafin_gl << [crg_orafin_ar, crg_orafin_ap]


                crg_epm = App('EPM', 'Financial Reporting')
                crg_orafin_gl >> crg_epm

    with G('Human Resources'):
        if show_DJ:
            with DJ('hr'):
                dj_empower = App('Empower', 'HR & Payroll')
                App('PageUp', 'Recruitment (DJ)')
                App('PACE', 'Employee Performance Management (DJ)')
                App('Workplace', 'Communication and Collaboration (DJ)')
                App('Sharepoint', 'Intranet (DJ)')

        if show_CRG:
            with CRG('hr'):
                crg_payglobal = App('PayGlobal', 'HR & Payroll')
                App('PageUp', 'Recruitment (CRG)')
                App('PACE', 'Employee Performance Management')
                App('eLearn', 'Training')
                App('Workplace', 'Communication and Collaboration')
                App('Sharepoint', 'Intranet')

    with G('Product Design'):
        if show_CRG:
            with CRG('pdd'):
                crg_plm = App('Lectra', 'Product Lifecycle Management')

    with G('Supply Chain'):
        if show_DJ:
            with DJ('sc'):
                dj_wms = App('Manhattan', 'Manhattan WMOS (DJ)')
                dj_edi = App('SPS', 'EDI Gateway')
                dj_axima = App('Axima', 'Third-Party Logistics')
                dj_sim_sc = App('SIM (SC)', 'Store Inventory Management for Supply Chain')

        if show_CRG:
            with CRG('sc'):
                crg_wms = App('Manhattan', 'Manhattan WMOS (CRG,PX)')
                crg_sc_wcs = App('Shaefer', 'Warehouse Control System')
                crg_sc_ff = App('Damco', 'Freight Forwarding')
                crg_sc_edi = App('IPT', 'EDI Gateway')

    with G('IT Administration'):
        App('ServiceNow', 'IT Service Management')
        App('JIRA', 'Project Management')
        App('Clarity', 'Time Management')

    with G('Customer Service'):
        if show_CRG:
            with CRG('cs'):
                crg_sfdc_sc = App('SFDC ServiceCloud', 'Case Management')

        if show_DJ:
            with DJ('cs'):
                dj_sfdc_sc = App('SFDC ServiceCloud', 'Case Management')


    # Links
    # Online
    if show_DJ:        
        dj_rms >> dj_isams
        dj_osm >> dj_rms
        cobra >> dj_rms
        sfdc   >> dj_isams

    if show_CRG:
        crg_rms >> crg_isams
        crg_osm >> crg_rms

    if show_PX:
        px_rms >> px_sfcc

    # HR
    if show_DJ:
        dj_empower >> dj_orafin_gl

    if show_CRG:
        crg_payglobal >> crg_orafin_gl

    # RMS
    if show_DJ:
        dj_rms >> sim  
        dj_rms >> dj_orafin_gl
        dj_pos >> dj_rms
        dj_rms >> sfdc

    if show_CRG:
        crg_rms >> crg_orafin_gl
        crg_pos >> crg_rms
        crg_plm >> crg_rms

    if show_PX:
        px_pos >> px_rms

    # WMS
    if show_DJ:
        dj_rms >> dj_wms
        dj_wms >> dj_edi

    if show_CRG:
        crg_rms >> crg_wms
        crg_wms >>  [crg_sc_wcs, crg_sc_ff, crg_sc_edi]


