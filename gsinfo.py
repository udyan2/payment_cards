import pandas as pd
from openpyxl import load_workbook

def getinfo():
    import_file_path = 'cards.xlsx'
    df=pd.read_excel(import_file_path)
    cardno_list = df['CARDNO'].tolist()
    exp_list = df['EXP_DATE'].tolist()
    cvv_list = df['CVV'].tolist()
    ipin_list = df['IPIN'].tolist()
    ilength=(len(cardno_list))
    return(cardno_list, exp_list, cvv_list, ipin_list, ilength)

def sendinfo(o_cardno_list, o_exp_list, o_cvv_list, t_time_list, status, total_time, pamount):
    import_file_path = 'report.xlsx'
    sdf=pd.read_excel(import_file_path)
    sdf["CARDNO"] = o_cardno_list
    sdf.to_excel("report.xlsx",index=False)
    sdf["EXPDATE"] = o_exp_list
    sdf.to_excel("report.xlsx",index=False)
    sdf["CVV"] = o_cvv_list
    sdf.to_excel("report.xlsx",index=False)
    sdf["TIME TAKEN"] = t_time_list
    sdf.to_excel("report.xlsx",index=False)
    sdf["STATUS"] = o_cvv_list
    sdf.to_excel("report.xlsx",index=False)
    wb = load_workbook('report.xlsx')
    work_sheet = wb.active # Get active sheet
    work_sheet.append(['Successfull Payments', status.count(1)])
    work_sheet.append(['Failed Payments', status.count(0)])
    work_sheet.append(['Total Payments', status.count(1)+status.count(0)])
    work_sheet.append(['Total Amount Paid', pamount*status.count(1)])
    work_sheet.append(['Total Time Taken', total_time])
    wb.save('report.xlsx')