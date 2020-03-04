from pydiagrams.Architecture import ArchitectureContext, Namespace

ug = Namespace() #Namespace for user groups

with ArchitectureContext() as a:            


	#================================================================================
	# Systems
	
	# iSAMS -------------------------------------------------------------------------
	es = a.Application('iSAMS'
			,entities = ['Customer Promo', 'Customers', 'Dispatch', 'Dispatch Locations', 'Inventory', 'Orders', 'Prices', 'Product Images', 'Products', 'Promotions', 'Sales', 'Stores', 'Wishlists']
			,modules  = ['Find In Store', 'Fulfilment', 'Gift Cards', 'Gift Registry', 'Order Management', 'Payment Gateway', 'Product Reviews', 'Promotion Management', 'RM Profiler', 'Websites']
			)
	
	# RMS ---------------------------------------------------------------------------
	rms = a.Application('RMS'
			,entities = ['Inventory', 'Inventory Adjustments', 'Orders', 'Prices', 'Product Images', 'Products', 'Sales', 'Shipments', 'Stores', 'Suppliers', 'Transactions', 'Transfers']
			,modules  = ['Data Enrichment', 'Dispatch', 'Find In Store', 'Inventory Management', 'Merchandising', 'OMS', 'SIM']
			)
	# Integrations
	rms.Data_Enrichment >> rms.Products
	rms.Find_In_Store >> rms.Orders
	rms.Inventory_Management >> [rms.Inventory, rms.Inventory_Adjustments, rms.Shipments, rms.Transfers]
	rms.Merchandising >> [rms.Inventory, rms.Prices, rms.Product_Images, rms.Products, rms.Sales, rms.Stores]
	rms.OMS >> [rms.Dispatch, rms.Orders]
	
	# Manhattan WMoS ----------------------------------------------------------------
	wms = a.Application('Manhattan WMoS'
			,entities = ['ASNs', 'Inventory Transactions', 'Items', 'Picks', 'Stores', 'Suppliers', 'Transfers']
			,modules  = ['Despatch', 'Foundation Data', 'Inventory Management', 'Picking', 'Putaway', 'Receiving', 'Wave Processing']
			)
	# Integrations
	wms.Foundation_Data >> [wms.Items, wms.Stores, wms.Suppliers]
	wms.Inventory_Management >> [wms.Inventory_Transactions, wms.Transfers]
	wms.Picking >> wms.Picks
	wms.Receiving >> wms.ASNs
	
	# Salesforce --------------------------------------------------------------------
	sf = a.Application('Salesforce'
			,entities = ['Customer Promo', 'Customers', 'Products', 'Promotions', 'Transactions']
			,modules  = ['Salesforce', 'Salesforce Marketing Cloud']
			)
	# Integrations
	sf.Salesforce >> [sf.Customer_Promo, sf.Customers, sf.Promotions, sf.Transactions]
	sf.Salesforce_Marketing_Cloud >> [sf.Customer_Promo, sf.Customers, sf.Products, sf.Promotions, sf.Transactions]
	
	# EDW ---------------------------------------------------------------------------
	edw = a.Application('EDW'
			,entities = ['Customer Promo', 'Customers', 'Products', 'Promotions', 'Staff', 'Transactions', 'Wishlists']
			)
	# Integrations
	edw.Staff >> edw.Customers
	
	# DPS ---------------------------------------------------------------------------
	dps = a.Application('DPS'
			,entities = ['Payments']
			,modules  = ['Web Services', 'pxPay']
			)
	# Integrations
	dps.Web_Services >> dps.Payments
	dps.pxPay >> dps.Payments
	
	# Payment Acquirers -------------------------------------------------------------
	pay = a.Application('Payment Acquirers'
			,entities = ['AMEX Cards AU', 'AMEX Cards NZ', 'Credit Plans', 'Mastercard AU', 'Mastercard NZ', 'Pay With Points', 'VISA AU', 'VISA NZ']
			,modules  = ['AMEX', 'CBA', 'China Union Pay', 'Paypal']
			)
	# Integrations
	pay.AMEX >> [pay.AMEX_Cards_AU, pay.Credit_Plans, pay.Pay_With_Points]
	pay.CBA >> [pay.Mastercard_AU, pay.VISA_AU]
	
	# Images ------------------------------------------------------------------------
	img = a.Application('Images'
			,entities = ['Product Images', 'Products']
			,modules  = ['Admation', 'Mondo']
			)
	# Integrations
	img.Admation >> img.Mondo
	img.Mondo >> img.Product_Images
	
	# Freight Providers -------------------------------------------------------------
	fr = a.Application('Freight Providers'
			,modules  = ['Aus Post', 'StarTrack']
			)
	
	# Givex -------------------------------------------------------------------------
	gc = a.Application('Givex'
			,entities = ['Accounts', 'Customers', 'Journals']
			,modules  = ['Card Services', 'Corporate Clients']
			)
	# Integrations
	gc.Card_Services >> [gc.Accounts, gc.Customers, gc.Journals]
	gc.Corporate_Clients >> gc.Card_Services
	
	# Gift Card Fulfilment ----------------------------------------------------------
	gcf = a.Application('Gift Card Fulfilment'
			,modules  = ['AB Note', 'Blackhawk']
			)
	
	# Oracle EBS --------------------------------------------------------------------
	ebs = a.Application('Oracle EBS'
			,entities = ['Journals']
			,modules  = ['General Ledger']
			)
	# Integrations
	ebs.General_Ledger >> ebs.Journals
	
	# Suppliers ---------------------------------------------------------------------
	sup = a.Application('Suppliers'
			,entities = ['Inventory', 'Product Images', 'Products', 'Shipments']
			,modules  = ['Drop Ship', 'Supplier']
			)
	# Integrations
	sup.Supplier >> [sup.Drop_Ship, sup.Product_Images, sup.Products, sup.Shipments]
	
	# Point Of Sale -----------------------------------------------------------------
	pos = a.Application('Point Of Sale'
			,entities = ['Customer Promo', 'Customers', 'Gift Registry', 'Orders', 'Promotions', 'Transactions']
			,modules  = ['EFT Client', 'POS', 'VBS', 'VOD']
			)
	# Integrations
	pos.POS >> [pos.EFT_Client, pos.Orders, pos.Transactions]
	pos.VBS >> pos.Promotions
	pos.VOD >> [pos.Customer_Promo, pos.Customers, pos.VBS]
	
	# PC EFTPOS ---------------------------------------------------------------------
	eft = a.Application('PC EFTPOS'
			,entities = ['Bank Tenders', 'Gift Card Tenders']
			,modules  = ['Tender Handler']
			)
	# Integrations
	eft.Tender_Handler >> [eft.Bank_Tenders, eft.Gift_Card_Tenders]
	
	# SPS Commerce ------------------------------------------------------------------
	sps = a.Application('SPS Commerce'
			,modules  = ['Orders', 'Products', 'Shipments']
			)
	
	# Data Enrichment ---------------------------------------------------------------
	de = a.Application('Data Enrichment'
			,modules  = ['BOA', 'COBRA']
			)
	
	# Web ---------------------------------------------------------------------------
	web = a.Application('Web'
			,modules  = [('AV', 'Kleber (Address Validation)')
						, ('Analytics', 'Google Anayltics')
						, ('BV', 'BazaarVoice (Product Reviews)')
						, ('Customer', 'Customer Browser')
						, ('Optimizely', 'Optimizely (A/B Testing)')
						, ('PI', 'SFMC Predictive Intelligence')
						, ('Search', 'SLI (Product Search)')
						, ('Tag', 'Google Web Tag Management')
						]
			)
	# Integrations
	web.Customer >> [web.AV, web.BV, web.Search, web.Tag]
	web.Tag >> [web.Analytics, web.Optimizely, web.PI]
	
	# EFTREC ------------------------------------------------------------------------
	eftrec = a.Application('EFTREC'
			,entities = ['Transactions']
			,modules  = ['Reconciliation']
			)
	# Integrations
	eftrec.Reconciliation >> eftrec.Transactions
	
	#================================================================================
	# Integrations
	
	with a.IntegrationSet('Informatica'):
	# Integrations
		edw.Transactions >> sf.Transactions
		sf.Customer_Promo >> edw.Customer_Promo
		sf.Customers >> edw.Customers
		sf.Promotions >> edw.Promotions
	
	with a.IntegrationSet('Middleware', isMiddleware=True):
	# Integrations
		dps.Payments >> eftrec.Transactions                     % '#33 CUP Online Transactions'
		edw.Customer_Promo >> es.Customer_Promo                 % '#12 Customer Promo'        & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100113033/12+Promotion+Customer+EDW+-+iSAMS'}
		edw.Customers >> es.Customers                           % '#5 Customers'              & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100112338/05+Customers+EDW+-+iSAMS'}
		edw.Transactions >> es.Orders                           % '#34 Save the Sale and GR'  & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/101792031/34+Save+The+Sale+Gift+Registry+Sales+EDW+-+iSAMS'}
		edw.Transactions >> gc.Accounts                         % '#35 Offline Gift Card Purchases' & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/101982207/35+Offline+Gift+Card+Purchases+EDW-+GiveX'}
		edw.Transactions >> gc.Card_Services                    % '#32 Layby/POD Payments'
		es.Customers >> edw.Customers                           % '#29 Customers'             & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100373326/29+Customers+iSAMS+-+EDW'}
		es.Dispatch >> rms.Dispatch                             % '#13 Dispatch Request'      & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100113082/13+Order+Dispatch+Request+iSAMS+-+RMS'}
		es.Find_In_Store >> rms.Find_In_Store                   % '#11 Find In Store'         & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100112958/11+Find+In+Store+iSAMS+-+RMS'}
		es.Orders >> rms.Orders                                 % '#4 Orders'
		es.Sales >> edw.Transactions                            % '#6 Sales'                  & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100112498/06+Sales+iSAMS+-+EDW'}
		es.Wishlists >> edw.Wishlists                           % '#31 Wishlists'
		gc.Journals >> ebs.General_Ledger                       % '#7 Journals'
		gc.Journals >> eftrec.Transactions                      % '#30 Gift Card Tenders'
		img.Product_Images >> rms.Product_Images                % '#28 Product Image Filenames' & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100400426/28+Product+Images+Admation-+RMS'}
		pos.Promotions >> es.Promotions                         % '#8 Promotions'             & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100112464/08+Promotions+VBS+-+iSAMS'}
		rms.Dispatch >> es.Dispatch                             % '#14 Dispatch Response'     & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100113142/14+Order+Dispatch+Response+RMS+-+iSAMS'}
		rms.Inventory >> es.Inventory                           % '#9 Inventory'              & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100112609/09+Availability+RMS+-+iSAMS'}
		rms.OMS >> wms.Picks                                    % '#23 Pickticket'            & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100400109/23+Pick+Tickets+Orders+RMS+-+WMS'}
		rms.Orders >> es.Orders                                 % '#3 Orders'
		rms.Prices >> es.Prices                                 % '#10 Prices'                & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100112671/10+Prices+RMS+-+iSAMS'}
		rms.Products >> es.Products                             % '#1 Products'               & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100111916/01+Products+RMS+-+iSAMS'}
		rms.Products >> wms.Items                               % '#18 Item Master'           & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100373747/18+WMS+Item+Master+Products+RMS+-+WMS'}
		rms.Products >> wms.Items                               % '#19 Item Cross Ref'
		rms.Shipments >> wms.ASNs                               % '#21 ASNs'                  & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100399001/21+ASNs+Shipments+RMS+-+WMS'}
		rms.Stores >> es.Stores                                 % '#2 Stores'                 & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100112000/02+Stores+RMS+-+iSAMS'}
		rms.Stores >> wms.Stores                                % '#27 Stores'                & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100400333/27+Stores+RMS+-+WMS'}
		rms.Suppliers >> wms.Suppliers                          % '#20 Vendor Master'         & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100395142/20+WMS+Vendor+Master+Suppliers+RMS+-+WMS'}
		rms.Transfers >> wms.Transfers                          % '#22 Store Distro'          & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100399872/22+Store+Distros+Transfers+RMS+-+WMS'}
		wms.Inventory_Transactions >> rms.Inventory_Adjustments % '#25 PIX_TRAN'              & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100400006/25+PIX+TRAN+Inventory+Adjustments+WMS+-+RMS'}
		wms.Transfers >> rms.Transfers                          % '#26 Shipment Confs'        & {'url': 'https://davidjones.atlassian.net/wiki/spaces/OR1/pages/100400228/26+Shipment+Confirmations+WMS+-+RMS'}
	
	with a.IntegrationSet('Internal'):
	# Integrations
		de.COBRA >> rms.Data_Enrichment
		edw.Customer_Promo >> pos.Customer_Promo
		edw.Customers >> pos.Customers           % 'Customers'                 & {'direction': 'both'}
		edw.Products >> img.Products
		edw.Products >> sf.Products
		edw.Promotions >> pos.Promotions
		edw.Transactions >> eftrec.Transactions
		edw.Transactions >> rms.Sales
		es.Fulfilment >> fr.Aus_Post             % 'Aus Post Dispatch'
		es.Fulfilment >> fr.StarTrack            % 'StarTrack Dispatch'
		es.Payment_Gateway >> dps.Payments       % 'Transactions'              & {'url': 'x', 'direction': 'both'}
		es.Payment_Gateway >> pay.Paypal
		es.Websites >> web.Customer
		img.Product_Images >> es.Product_Images
		pos.Transactions >> edw.Transactions
		rms.Products >> edw.Products
		sps.Orders >> rms.OMS                    % '#15,16 Orders'             & {'direction': 'both'}
		sps.Products >> rms.Products             % '#17 Products'
		sps.Shipments >> rms.Shipments
		sup.Drop_Ship >> sps.Orders              % 'Orders'                    & {'direction': 'both'}
		sup.Product_Images >> img.Admation
		sup.Products >> de.COBRA
		sup.Products >> sps.Products
		sup.Shipments >> sps.Shipments
	
	with a.IntegrationSet('Third Party'):
	# Integrations
		eft.Gift_Card_Tenders >> gc.Card_Services % 'Gift Card Tenders'         & {'direction': 'both'}
		es.Gift_Cards >> gc.Card_Services         % 'Gift Cards'                & {'direction': 'both'}
		es.Gift_Registry >> pos.Gift_Registry     % 'Gift Registries'
		es.Order_Management >> pos.Orders         % 'Delivery Options'
		es.Products >> web.Search                 % 'Search Integration'
		gc.Card_Services >> gcf.AB_Note           % 'AB Note'
		gc.Card_Services >> gcf.Blackhawk         % 'Blackhawk'
		pos.EFT_Client >> eft.Tender_Handler      % 'Tenders'                   & {'direction': 'both'}
		wms.Despatch >> fr.Aus_Post               % 'Aus Post Dispatch'
		wms.Despatch >> fr.StarTrack              % 'StarTrack Dispatch'
	

# Generate all diagrams            
from pydiagrams.ArchitectureDiagrams import generate_all
import os.path
generate_all(a, os.path.join(os.path.dirname(__file__), 'Architecture-demo-Ecomm'))            
            
