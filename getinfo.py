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


# i=3
# exp=str(exp_list[i])
# expyr=exp[0:2]
# expmm=exp[3:8]
# print(expyr)
# print(expmm)


# cvv=str(cvv_list[i])
# if len(cvv)==1:
#     cvv='00'+cvv
# elif len(cvv)==2:
#     cvv='0'+cvv
# print(cvv)