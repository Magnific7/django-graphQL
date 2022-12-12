import pandas as pd
import numpy as np

def deposit(bnr_ripps,bk_ledger_df):

#     deposit on bnr ripps
    deposit_ripps = bnr_ripps[bnr_ripps['Credit Account '].str.contains('1240100').fillna(False)]
    deposit_ripps = deposit_ripps[deposit_ripps['Type']=='pacs.009. 001.08']
    deposit_ripps = deposit_ripps[deposit_ripps['Reference'].str.startswith('FT').fillna(False)]
    deposit_ripps = deposit_ripps[deposit_ripps['Remittance infos'].str.contains('PTR/003').fillna(False)]
    print('deposit ripps',deposit_ripps.shape)
    
#     deposit on bk ledger 
    bk_ledger = bk_ledger_df[bk_ledger_df['DEBIT_ACCT_NO']=='RWF1701400901002']
    bk_ledger = bk_ledger[bk_ledger['PAYMENT_DETAILS'].str.contains('TT').fillna(False)]
    bk_ledger = bk_ledger[bk_ledger['PAYMENT_DETAILS'].str.contains('FT').fillna(False)]
    print('deposit bk ledger',deposit_ripps.shape, 'deposit ledger', bk_ledger.shape)
    
#     Maching bk bnr combined 
    rec_id = bk_ledger.PAYMENT_DETAILS.str.split(' ', expand=True, n=1)
    bk_ledger['log_recid'] = rec_id[1]
    
    merge_bnr_bk = pd.merge(deposit_ripps, bk_ledger, how='outer',left_on='Reference',right_on='log_recid',)
    print('deposit merged both sides ',merge_bnr_bk.shape)
    
    deposit_matching = merge_bnr_bk[merge_bnr_bk['Reference'] == merge_bnr_bk['log_recid']]
    print('deposit matching', deposit_matching.shape)
#     deposit_matching.to_excel('july_deposit_matching.xlsx')

#     mismatch on bnr side 
    merge_bnr_ripps = pd.merge(deposit_ripps, bk_ledger, how='left',left_on='Reference',right_on='log_recid',)
    print('deposit merged on bnr ripps ',merge_bnr_ripps.shape)
    
    deposit_mismatching_bnr_ripps = merge_bnr_ripps[merge_bnr_ripps['Reference'] != merge_bnr_ripps['log_recid']]
    print('deposit mismatch on bnr ripps ', deposit_mismatching_bnr_ripps.shape)
#     deposit_mismatching_bnr_ripps.to_excel('july_deposit_bnr_mismatching.xlsx')

    #     mismatch on bk side 
    merge_bk_ledger = pd.merge(deposit_ripps, bk_ledger, how='right',left_on='Reference',right_on='log_recid',)
    print('deposit merged on bk ledger ',merge_bk_ledger.shape)
    
    deposit_mismatching_bk_ledger = merge_bk_ledger[merge_bk_ledger['Reference'] != merge_bk_ledger['log_recid']]
    print('deposit mismatch on bk ledger ', deposit_mismatching_bk_ledger.shape)
#     deposit_mismatching_bk_ledger.to_excel('july_deposit_bk_mismatching.xlsx')

    return deposit_matching,deposit_mismatching_bk_ledger,deposit_mismatching_bnr_ripps
