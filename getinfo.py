import pandas as pd


def info():
    import_file_path = 'cards.xlsx'
    rf=pd.read_excel(import_file_path)
    cardno_list = rf['CARDNO'].tolist()
    exp_list = rf['EXP_DATE'].tolist()
    cvv_list = rf['CVV'].tolist()
    ipin_list = rf['IPIN'].tolist()
    ilength=(len(cardno_list))
    return(cardno_list, exp_list, cvv_list, ipin_list, ilength)
