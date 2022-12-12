import pandas as pd
import numpy as np

def withdraws( bnr_ripps,bk_ledger_df):

#     withdraws on bnr ripps
    withdraws_ripps = bnr_ripps[bnr_ripps['Debit Account'].str.contains('1240100').fillna(False)]
    withdraws_ripps = withdraws_ripps[withdraws_ripps['Type']=='pacs.009. 001.08']
    withdraws_ripps = withdraws_ripps[withdraws_ripps['Reference'].str.startswith('FT').fillna(False)]
    # withdraws_ripps = withdraws_ripps[withdraws_ripps['Remittance infos'].str.contains('PTR/002').fillna(False)]
    print('withdraws ripps',withdraws_ripps.shape)
    
#     withdraws on bk ledger 
    bk_ledger = bk_ledger_df[bk_ledger_df['DEBIT_ACCT_NO']=='RWF1701400901002']
    bk_ledger = bk_ledger[bk_ledger['PAYMENT_DETAILS'].str.contains('TT').fillna(False)]
    bk_ledger = bk_ledger[bk_ledger['PAYMENT_DETAILS'].str.contains('FT').fillna(False)]
    print('withdraws bk ledger',withdraws_ripps.shape, 'withdraws ledger', bk_ledger.shape)
    
#     Maching bk bnr combined 
    rec_id = bk_ledger.PAYMENT_DETAILS.str.split(' ', expand=True, n=1)
    bk_ledger['log_recid'] = rec_id[1]
    
    merge_bnr_bk = pd.merge(withdraws_ripps, bk_ledger, how='outer',left_on='Reference',right_on='log_recid',)
    print('withdraws merged both sides ',merge_bnr_bk.shape)
    
    withdraws_matching = merge_bnr_bk[merge_bnr_bk['Reference'] == merge_bnr_bk['log_recid']]
    print('withdraws matching', withdraws_matching.shape)
    withdraws_matching.to_excel('july_withdraws_matching.xlsx')

#     mismatch on bnr side 
    merge_bnr_ripps = pd.merge(withdraws_ripps, bk_ledger, how='left',left_on='Reference',right_on='log_recid',)
    print('withdraws merged on bnr ripps ',merge_bnr_ripps.shape)
    
    withdraws_mismatching_bnr_ripps = merge_bnr_ripps[merge_bnr_ripps['Reference'] != merge_bnr_ripps['log_recid']]
    print('withdraws mismatch on bnr ripps ', withdraws_mismatching_bnr_ripps.shape)
    withdraws_mismatching_bnr_ripps.to_excel('july_withdraws_bnr_mismatching.xlsx')

    #     mismatch on bk side 
    merge_bk_ledger = pd.merge(withdraws_ripps, bk_ledger, how='right',left_on='Reference',right_on='log_recid',)
    print('withdraws merged on bk ledger ',merge_bk_ledger.shape)
    
    withdraws_mismatching_bk_ledger = merge_bk_ledger[merge_bk_ledger['Reference'] != merge_bk_ledger['log_recid']]
    print('withdraws mismatch on bk ledger ', withdraws_mismatching_bk_ledger.shape)
    withdraws_mismatching_bk_ledger.to_excel('july_withdraws_bk_mismatching.xlsx')

    return withdraws_matching,withdraws_mismatching_bk_ledger, withdraws_mismatching_bnr_ripps
