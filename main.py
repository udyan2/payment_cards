from selenium import webdriver
import gsinfo
import time
import sys

passw=input("Enter Password: ")
fobj=open("C:/Users/AVITA/Documents/payment_cards/passw.txt","r")
if passw==fobj.readline():
    "Access Granted"
else:
    print("Access Denied: ")
    sys.exit()
    
main_start_time = time.time()

#input lists
cardno_list, exp_list, cvv_list, ipin_list, ilength, name_list, email_list, phone_list = gsinfo.getinfo()

#Creating Report Output Headers
gsinfo.repheader() 

def pinwin():
    for handle in driver.window_handles: 
        if handle != main_page: 
            pin_page = handle
    return pin_page

#initialization of variables   
plink=input("Enter the payment Link: ")
pamount=input("Enter the payment amount: ")
mode=int(input("Enter Mode (1 = IPIN, 2 =  OTP): "))
start_index=int(input("Enter start index of the excel file (0 for default): "))

#Output lists
o_cardno_list=[None for x in range(ilength)]
o_exp_list=[None for x in range(ilength)]
o_cvv_list=[None for x in range(ilength)]
o_ipin_list=[None for x in range(ilength)]
status=[None for x in range(ilength)]
transaction_id_list=[None for x in range(ilength)]
t_time_list=[None for x in range(ilength)]

for i in range(start_index,ilength):
    
    name=str(name_list[i])
    email=str(email_list[i])
    phone=str(phone_list[i])
        
    
    driver=webdriver.Chrome()
    exp=str(exp_list[i])
    expmm=exp[0:2]
    expyr=exp[3:8]
    
    cvv=str(cvv_list[i])
    if len(cvv)==1:
        cvv='00'+cvv
    elif len(cvv)==2:
        cvv='0'+cvv
        
        
    driver.get(plink)
    main_page=driver.current_window_handle
    driver.implicitly_wait(20)

    payment_start_time=time.time()
    pn_but=driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div[3]/a")
    pn_but.click()
    
    driver.find_element_by_name("customerName").clear()
    name_el=driver.find_element_by_name("customerName")
    name_el.send_keys(name)
    email_el=driver.find_element_by_name("customerEmail")
    email_el.send_keys(email)
    phone_el=driver.find_element_by_name("customerNumber")
    phone_el.send_keys(phone)
    
    time.sleep(0.8)
    
    ctp_btn=driver.find_element_by_xpath('//*[@id="main_wrapper"]/div/div[2]/div/div[2]/div[1]/div[2]/div[4]/a')
    ctp_btn.click()
    
    time.sleep(0.6)
    
    dc_btn=driver.find_element_by_xpath('//*[@id="main_wrapper"]/div/div[2]/div/div[2]/div[2]/div[2]/ul/li[2]/a/span[2]')
    dc_btn.click()
   
    
    print("\nPayment", i, "Details: ")
    cardno=str(cardno_list[i])
    cardno_el=driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/input')
    cardno_el.send_keys(cardno)
    o_cardno_list[i]="'"+cardno
    print("\nCard Number:",cardno)
    time.sleep(0.7)
    expmm=expmm
    expmm_el=driver.find_element_by_name('monthinput')
    expmm_el.send_keys(expmm)
    expyr=expyr
    expyr_el=driver.find_element_by_name('yearinput')
    expyr_el.send_keys(expyr)
    o_exp_list[i]=expmm+'/'+expyr
    time.sleep(0.4)
    cvv=cvv
    cvv_el=driver.find_element_by_name('cvvinput')
    cvv_el.send_keys(cvv)
    o_cvv_list[i]=cvv
    time.sleep(0.9)
    cardholder=name
    cardholder_el=driver.find_element_by_name('cardHolder')
    cardholder_el.send_keys(cardholder)
    
    time.sleep(2)
    
    paynow_el=driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/a')
    paynow_el.click()
    
    pin_win=pinwin()
    driver.switch_to.window(pin_win)
    
    if(mode==1):
        ipin=str(ipin_list[i])
        if len(ipin)==1:
            ipin='000'+ipin
        elif len(ipin)==2:
            ipin='00'+ipin
        elif len(ipin)==3:
            ipin='0'+ipin
        ipin_el=driver.find_element_by_name('txtipin') 
        ipin_el.send_keys(ipin)
        o_ipin_list[i]=ipin
        submit_btn=driver.find_element_by_id('btnverify')
        submit_btn.click()
        while "trans_id=" not in driver.current_url:
            if "failure" in driver.current_url:
                break
            pass
        url=driver.current_url
        print(url)
        #driver.switch_to.window(main_page)
    
    
    else:
        while "trans_id=" not in driver.current_url:
            pass
        url=driver.current_url
        print("\nPayment", i, "Details: ")
        print(url)
    
    
    payment_end_time=time.time()
    payment_time_elapsed=payment_end_time-payment_start_time
    
    if "success" in url:
        status[i]="Success"
        print("Payment",i,"Success")
        transaction_id=url[((url.index("trans_id"))+15):]
        transaction_id_list[i]=transaction_id
    elif "Failure" or "failure" in url:
        status[i]="Fail"
        print("Payment",i,"Fail")
        transaction_id=url[((url.index("trans_id"))+15):]
        transaction_id_list[i]=transaction_id
    else:
        status[i]="Status Unknown"
        print("Payment",i,"Status Unknown")
        transaction_id="NA"
        transaction_id_list[i]=transaction_id
        
    print("Transaction ID:", transaction_id)
    t_time_list[i]=payment_time_elapsed
    
    gsinfo.exwrite(o_cardno_list[i], o_exp_list[i], o_cvv_list[i], o_ipin_list[i], transaction_id_list[i], t_time_list[i], status[i], pamount)
    
    print("Payment",i,"Time Elapsed: ",payment_time_elapsed)
    driver.close()
    driver.quit()
    
main_end_time=time.time()
main_time_elapsed=main_end_time-main_start_time
gsinfo.summary(status, pamount, main_time_elapsed)
print("\nTotal time elapsed:", main_time_elapsed)


