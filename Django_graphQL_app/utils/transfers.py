import pandas as pd
import numpy as np
from .. import views

def mis_match_in_updated_new( bnr,bk):
    bnr = bnr[bnr['Credit Account '].str.contains('1240100').fillna(False)]
    bnr = bnr[bnr['Type']=='pacs.008. 001.08']
    bk_ledger = bk[bk['DEBIT_ACCT_NO']=='RWF1701400041002'] 

#     bk_ledger.reset_index(level=0, inplace=True)
    bk_ledger['new'] = bk_ledger[bk_ledger['TRANSACTION_TYPE']=='ACLJ']['PAYMENT_DETAILS']

#     bk_ledger['new'].value_counts()
    df = bk_ledger['new'].str.split(' ', expand=True, n=1)
    bk_ledger['new'] = df[0]
    bk_ledger.loc[bk_ledger['new'].notna(),'DEBIT_THEIR_REF']=bk_ledger['new']
#     bk_ledger.loc[bk_ledger['DEBIT_THEIR_REF'].isnull(),'DEBIT_THEIR_REF']= bk_ledger['API_UNIQUE_ID']
    
    
    bnr.Amount = bnr.Amount.astype(str).str.replace(',', '')
    bnr.Amount = pd.to_numeric(bnr.Amount, errors='coerce')

    bk_ledger.LOC_AMT_DEBITED = pd.to_numeric(bk_ledger.LOC_AMT_DEBITED, errors='coerce')

##############################################insert '-' on DEBIT_THEIR_REF to make it similar to BNR Reference########################################
    string_ref = bk_ledger[(bk_ledger['TRANSACTION_TYPE']=='ACLJ')&(bk_ledger['new'].notna())
             &(bk_ledger['DEBIT_THEIR_REF'].str.startswith('FT'))]['DEBIT_THEIR_REF'] 

    bk_ledger.loc[(bk_ledger['TRANSACTION_TYPE']=='ACLJ')&(bk_ledger['new'].notna())
         &(bk_ledger['DEBIT_THEIR_REF'].str.startswith('FT')), 'DEBIT_THEIR_REF'] = string_ref.str.slice(stop=12)+ '-'+ string_ref.str[12:]
       
##########################Converting reference with digit to numeric format ##################################   
    bk_ledger.loc[bk_ledger['DEBIT_THEIR_REF'].str.isdigit().fillna(False), 'DEBIT_THEIR_REF']= pd.to_numeric(bk_ledger[bk_ledger['DEBIT_THEIR_REF'].str.isdigit().fillna(False)]['DEBIT_THEIR_REF'],downcast ='signed').fillna(False)
    bnr.loc[bnr['Reference'].str.isdigit().fillna(False),'Reference']=pd.to_numeric(bnr[bnr['Reference'].str.isdigit().fillna(False)]['Reference'],downcast ='signed').fillna(False)
##########################################################################################################################
#############################################Merging FT references########################################################    
    bk_ledger.loc[(bk_ledger['new'].notna())&
                    (bk_ledger['DEBIT_THEIR_REF'].str.startswith('FT').fillna(False))&
                  (bk_ledger['DEBIT_THEIR_REF'].str.endswith('-').fillna(False)), 'DEBIT_THEIR_REF']= bk_ledger[(bk_ledger['new'].notna())&
                    (bk_ledger['DEBIT_THEIR_REF'].str.startswith('FT').fillna(False))&
                  (bk_ledger['DEBIT_THEIR_REF'].str.endswith('-').fillna(False))]['new']

    single_tr =bnr[bnr['Credit Account ']=='1240100-RWF\n(BKIGRWRW)']

    #####################Bulk details#####################################################################

    bulk_tr_det = bnr[(bnr['Credit Account ']=='1240100-RWF-CL-CR\n(BKIGRWRW)')
                                &(bnr['Reference_new'].notna())]

    ####################Single bulk transfer##########################################################

    single_bulk=bnr[(bnr['Batch_no'].is_unique)&bnr['Reference_new'].isnull()&(bnr['Credit Account ']=='1240100-RWF-CL-CR\n(BKIGRWRW)')]


    bnr_cleaned = pd.concat([single_tr,bulk_tr_det,single_bulk],axis=0, ignore_index=True)
    ####################################################################################################
    Rejected = bnr_cleaned[(bnr_cleaned['Debit Account'].str.contains('1240100').fillna(False))|
                                     (bnr_cleaned['Status'].str.contains('rejected').fillna(False))]
    #####Removing rejected transactions##########################
    bnr_cleaned_new = bnr_cleaned[~(bnr_cleaned['Debit Account'].str.contains('1240100').fillna(False))&
                                     ~(bnr_cleaned['Status'].str.contains('rejected').fillna(False))]
    ####################################################################################################

    bnr_cleaned_new['Datenum'] = pd.to_datetime(bnr_cleaned_new['Value Date'],dayfirst=True)
    bnr_cleaned_new['Datenum'] = bnr_cleaned_new['Datenum'].dt.strftime('%Y%m%d')
    bnr_cleaned_new['Datenum'] = pd.to_numeric(bnr_cleaned_new['Datenum'].astype(int))
    
    bk_ledger['DEBIT_VALUE_DATE'] =pd.to_numeric(bk_ledger['DEBIT_VALUE_DATE'].astype(int))
    ###################################################################################################
    print('Input data size bk:{}, bnr:{}'.format(bk_ledger.shape,  bnr_cleaned_new.shape))


########################################################################Preparation of ripps#####################

    bnr_cleaned_new1 = bnr_cleaned_new[~bnr_cleaned_new['Batch_no'].str.startswith('FT').fillna(False)&
           (bnr_cleaned_new['Reference'].duplicated())&(bnr_cleaned_new['Reference_new'].isnull()
                                                            &~(bnr_cleaned_new['Reference'].astype(str).str.startswith('220')))]

    bnr_cleaned_new2 = bnr_cleaned_new[bnr_cleaned_new['Batch_no'].str.startswith('FT').fillna(False)
                   &bnr_cleaned_new['Reference'].duplicated()&(bnr_cleaned_new['Reference_new'].isnull())]
    
    bnr_cleaned_new3 = pd.concat([bnr_cleaned_new1,bnr_cleaned_new2], axis=0, ignore_index=True)
    bnr_cleaned_new3_new = bnr_cleaned_new3.drop_duplicates('Reference', keep='first')###drop duplicates where ledger appears once

    bnr_data = bnr_cleaned_new.copy()
    print('bnr data after removing duplicates',bnr_data.shape)
 ####################################################################################################   
    Final_merge_bk= pd.merge(bk_ledger, bnr_data, how='left', left_on='DEBIT_THEIR_REF', right_on='Reference')

#     Final_merge_bk = Final_merge_bk.drop_duplicates(subset='RECID', keep='last')

    print('Merged data on Bk side',Final_merge_bk.shape)

      
    Final_merge_bnr= pd.merge(bk_ledger, bnr_data, how='right',left_on='DEBIT_THEIR_REF', right_on='Reference')


    Final_merge_bnr_new =Final_merge_bnr.copy()

    print('Merged data on BNR side',Final_merge_bnr_new.shape)
    
    
    ############################################################################################################################
#     Final_merge_bk['Days_diff'] = (pd.to_datetime(Final_merge_bk['Date'])-pd.to_datetime(Final_merge_bk['Value Date'])).dt.days
    Final_merge_bk['Date_diff'] = Final_merge_bk['DEBIT_VALUE_DATE']-Final_merge_bk['Datenum']
    Final_merge_bnr_new['Date_diff'] = Final_merge_bnr_new['DEBIT_VALUE_DATE']-Final_merge_bnr_new['Datenum']

    
    match_bk1 = Final_merge_bk[(Final_merge_bk['RECID'].notna())
                              &(Final_merge_bk['DEBIT_THEIR_REF'] ==Final_merge_bk['Reference'])
                              &(Final_merge_bk['Amount']==Final_merge_bk['LOC_AMT_DEBITED'])
#                                &(Final_merge_bk['Date_diff']>=0)
                              ]

    match_bnr1= Final_merge_bnr_new[(Final_merge_bnr_new['RECID'].notna())
                              &(Final_merge_bnr_new['DEBIT_THEIR_REF'] ==Final_merge_bnr_new['Reference'])
                              &(Final_merge_bnr_new['Amount']==Final_merge_bnr_new['LOC_AMT_DEBITED'])
#                                    &(Final_merge_bnr_new['Date_diff']>=0)
                                   ]
####################################Handling the duplicates on bk side and on bnr side#######################    
    pos =match_bk1[match_bk1['Date_diff']>=0].sort_values('Date_diff').drop_duplicates('RECID')
    match_bk_final =pos
    
    neg =match_bk1[match_bk1['Date_diff']<0].sort_values('Date_diff', ascending=False).drop_duplicates('RECID')
    neg_new =neg[~neg['RECID'].isin(pos['RECID'])]

    mismatch_bk_new1 = Final_merge_bk[Final_merge_bk['Reference'].isnull()]
    mismatch_bk_new2 = Final_merge_bk[Final_merge_bk['Reference'].notna()&
                                            (Final_merge_bk['Reference']==Final_merge_bk['DEBIT_THEIR_REF'])&
                                (Final_merge_bk['Amount']!=Final_merge_bk['LOC_AMT_DEBITED'])
#                                      &(Final_merge_bk['Date_diff']>=0)
                                     ]
    
    mismatch_bk_new = pd.concat([mismatch_bk_new1,mismatch_bk_new2], axis=0, ignore_index=True)

    misbk = mismatch_bk_new[~mismatch_bk_new['RECID'].isin(match_bk_final['RECID'])]
#     mismatch_bk_up_new1 =mismatch_bk_up_new[~mismatch_bk_up_new['RECID'].isin(match_up_new['RECID'])]

#     mismatch_bk_final = pd.concat([misbk,neg_new],axis=0,ignore_index=True)
    mismatch_bk_final=misbk
    mismatch_bnr_new1 = Final_merge_bnr_new[Final_merge_bnr_new['RECID'].isnull()]
    mismatch_bnr_new2 = Final_merge_bnr_new[Final_merge_bnr_new['RECID'].notna()&
                                            (Final_merge_bnr_new['Reference']==Final_merge_bnr_new['DEBIT_THEIR_REF'])&
                                (Final_merge_bnr_new['Amount']!=Final_merge_bnr_new['LOC_AMT_DEBITED'])
#                                            &(Final_merge_bnr_new['Date_diff']>=0)
                                           ]
    mismatch_bnr_new3 =bnr_cleaned_new3.drop_duplicates('Reference', keep='last') 
    mismatch_bnr_new = pd.concat([mismatch_bnr_new1,mismatch_bnr_new2], axis=0, ignore_index=True)
    
    pos_bnr = match_bnr1[match_bnr1['Date_diff']>=0].sort_values('Date_diff').drop_duplicates('RECID')
    neg_bnr = match_bnr1[match_bnr1['Date_diff']<0].sort_values('Date_diff', ascending=False).drop_duplicates('RECID')
    neg_bnr_new =neg_bnr[~neg_bnr['RECID'].isin(pos_bnr['RECID'])]
    misbnr = mismatch_bnr_new[~mismatch_bnr_new['RECID'].isin(match_bnr1['RECID'])]

    bk0=pos_bnr[(pos_bnr['Reference_new'].notna())]
    bk1 = pos_bnr[(pos_bnr['Reference_new'].isnull())&(pos_bnr['Reference'].duplicated())]
    bk2 = pos_bnr[pos_bnr['Reference'].duplicated()&(pos_bnr['Reference_new'].notna())&(pos_bnr['Batch_no'].str.startswith('RT'))]
    # bk3 =pos_bnr[(pos_bnr['Batch_no']=='T133008924020627')]
    bk_duplicates = pd.concat([bk1,bk2],axis=0, ignore_index=True)

    bknew =bk_duplicates.sort_values('Date_diff').drop_duplicates('RECID').drop_duplicates('Reference')
    bk7 = bk0[~bk0['Reference'].duplicated()]
    bk8 =bk0[bk0['Reference'].duplicated()&~bk0['Batch_no'].str.startswith('RT')]
    # bk9 =bk0[bk0['Reference'].duplicated()&bk0['Batch_no'].str.startswith('RT')]

    bk3 =pos_bnr[(pos_bnr['Reference_new'].isnull())]
    bk3 =bk3[~bk3['Reference'].duplicated()]
    match_bnr_final = pd.concat([bk7+bk8+bk3+bknew], axis=0, ignore_index=True)
    mismatch_bnr_final = pd.concat([neg_bnr_new,misbnr], axis=0, ignore_index=True)


    print('Matched data on bk side:\n', match_bk_final.shape)
    print('Mismatched data on bk side:\n', mismatch_bk_final.shape)
    print('Mismatched data on bnr side:\n', mismatch_bnr_final.shape)
    

    return match_bk_final, mismatch_bk_final, mismatch_bnr_final 

def mis_match_out(bnr,bk):

    bnr = bnr[bnr['Debit Account'].str.contains('1240100').fillna(False)]
    bnr = bnr[bnr['Type']=='pacs.008. 001.08']
    df = bk.RECID.str.split(';', expand=True, n=1)
    bk['Reference_rip'] = df[0]
    bk_ledger = bk[bk['CREDIT_ACCT_NO']=='RWF1701400801002']  
    print('Input data size:{}'.format((bnr.shape, bnr.shape, bk_ledger.shape)))


#     onepart_merge = pd.merge(bk_ledger,bnr1, how='left', left_on='Reference_rip', right_on='Reference')
    Final_merge_bk= pd.merge(bk_ledger, bnr, how='left',left_on='Reference_rip', right_on='Reference')
    print('Merged data on Bk side',Final_merge_bk.shape)
    
    Final_merge_bnr= pd.merge(bk_ledger, bnr, how='right',left_on='Reference_rip', right_on='Reference')
    print('Merged data on BNR side',Final_merge_bnr.shape)
    
    match_bk =Final_merge_bk[(Final_merge_bk['Reference_rip']==Final_merge_bk['Reference'])]

    
    mismatch_bk = Final_merge_bk[(Final_merge_bk['Reference_rip']!=Final_merge_bk['Reference'])]
#                                          &(Final_merge_bk['DEBIT_THEIR_REF']!=Final_merge_bk['Batch_no'])]
    
    match_bnr = Final_merge_bnr[(Final_merge_bnr['Reference_rip']==Final_merge_bnr['Reference'])]
#                                           |(Final_merge_bnr['DEBIT_THEIR_REF']==Final_merge_bnr['Batch_no'])]
    
    mismatch_bnr =  Final_merge_bnr[(Final_merge_bnr['Reference_rip']!=Final_merge_bnr['Reference'])]
#                                          &(Final_merge_bnr['DEBIT_THEIR_REF']!=Final_merge_bnr['Batch_no'])]

    
    print('Matched data on bk side:\n', match_bk.shape)
    print('Mismatched data on bk side:\n', mismatch_bk.shape)
    
    print('Matched data on bnr side:\n', match_bnr.shape)
    print('Mismatched data on bnr side:', mismatch_bnr.shape)   

    return match_bk, mismatch_bk, mismatch_bnr
