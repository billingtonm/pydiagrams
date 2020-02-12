# Demonstration of pydigrams, using the "Views" diagram style

# 1: Import the library to draw the type of diagram (Views)
from pydiagrams.Views  import ViewContext

# 2: Import the Helper that draws the diagram in a certain graph language (PUML or Graphviz)
from pydiagrams.helpers.Graphviz import Helper

# 3: Import all the constants (colour names, attribute names) 
from pydiagrams.helpers.constants import *

# Set up a Diagram using 'd' as the global namespace
with ViewContext(Helper, label="Data Architecture") as d:

    # Create a subgraph 'rms'
    with d.Cluster("RMS") as rms:
        # Allocate objects to rms
        saC     = rms.Table('sa_customer')
        s       = rms.Table('store')
        saTH    = rms.Table('sa_tran_head')
        saSD    = rms.Table('sa_store_day')
        saTI    = rms.Table('sa_tran_item')
        sul     = rms.Table('cr_store_uda_lovs_v')

        if Helper.name == 'Graphviz':
            rms.passthrough('{rank=min s saTH saC saSD saTI sul} #Align')
        
        with rms.Cluster("RMS: INFOCRM", style='filled', fillcolor=grey2) as inf:
            inf.node_attrs = {'fixedsize':'true', 'width':'3.5'}

            inf.node_attrs.update(fillcolor=color1)
            vgaF    = inf.View('v_google_ads_Feed')
            vgaLRH  = inf.View('v_google_ads_loyalty_rate_hdr')

            vgaLR   = inf.View('v_google_ads_loyalty_rate *', fillcolor=color2)
            vgaC    = inf.View('v_google_ads_Customers *',  fillcolor=color3)

            vCI     = inf.View('v_customers_in', fillcolor=color4)

            vgaT    = inf.View('v_google_ads_Trans *')
            vgaTH   = inf.View('v_google_ads_Tran_Headers *')

            vgaS    = inf.View('v_google_ads_Stores *', fillcolor=color7)
            vgaD    = inf.View('v_google_ads_dates *', fillcolor=color9)

            sth     = inf.Table('sales_trans_head', fillcolor=color6)
            stl     = inf.Table('sales_trans_lines', fillcolor=color6)

            gabr    = inf.Table('cr_google_ads_brand_regions *', fillcolor=color8)
            gbp     = inf.Table('cr_google_batch_process', fillcolor=color10, fontcolor='white')

            # Relationships

            #vgaF.Sources = [vgaC, vgaT]
            # << = 'Sources'
            vgaF << [vgaC, vgaT]  # translation: Data for vgaF 'comes from' vgaC, vgaT
            vCI >> vgaC           # translation: Data in vCI 'goes to' vgaC

            vgaTH << [sth, vgaS, vgaD]

            vgaS << gabr
            gbp >> vgaD

            vgaT  << [vgaTH, stl]

            vgaLR >> vgaLRH
        
        vgaLR << [saTH, saC, saSD, sul, vgaD, vgaS]

        saC >> vCI
        s   >> vgaS

        rms.edge_attrs = {color:'red', fontcolor:'red', label:'Exported to'}
        saTH >> sth
        saTI >> stl

    with d.Cluster('Informatica', fillcolor=grey1, style='filled') as infm:
        sch =  infm.Task('ST')

        with infm.Cluster("Taskflow: GoogleAdwords.<brand>", style='filled', fillcolor=grey2) as tf:
            tf.node_attrs.update(width='3.0')

            trx         = tf.Task('Task: adwords_<brand>_body')
            trx_header  = tf.Task('Task: adwords_<brand>_head')

            trx >> trx_header

        with infm.Cluster("adwords.bat", fillcolor=grey3, style='filled') as aw:
            fc = aw.Task('File Concatenation')
            fu = aw.Task('File Upload: gsutil')
            fc >> fu

        inf_schtask = infm.Task("Scheduled Task:\\nAdwords <brand>")

        sch >> tf # link a Task item to a Subgraph

        inf_schtask >> aw

        f  = infm.File('Transaction File')
        h  = infm.File('Header File')
        gf = infm.File('Google File')

        infm.edge_attrs = {color:'blue', fontcolor:'blue', label:'Read By'}
        fc << [f, h]

        tf.edge_attrs= {color:'blue', fontcolor:'blue', label:'Creates'}
        trx >> f 
        trx_header >> h

        #infm.aw.edge_attrs= {color:'blue', fontcolor:'blue', label:'Produces'}
        fc >> gf % 'Produces'

        gf >> fu        

    with d.Cluster('Google Cloud Platform') as gcp:
        gcp.node_attrs = {fillcolor:'11'}

        with gcp.Cluster('Storage', fillcolor=grey2, style='filled') as gcst:
            gcs = gcst.File('crg-ads-uploads/<brand>')

        with gcp.Cluster('BigQuery', fillcolor=grey2, style='filled') as gbq:
            gbqf = gbq.File('ssd_uploads.ssd_upload_logs')

        drd_util = gcp.Task('DRD Utility')

        gcp.edge_attrs = {color:'blue', fontcolor:'blue', label:'Read By'}
        gcs >> drd_util >> gbqf

    with d.Cluster('Google Adwords') as gmc:
        gaw = gmc.System('Google Adwords', fillcolor='12')


    vgaF >> trx
    vgaLRH >> trx_header

    fu >> gcst % 'gsutil cp'

    drd_util >> gaw % 'Uploads to'
