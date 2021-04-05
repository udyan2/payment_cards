from selenium import webdriver
import gsinfo
import time
import licn

inp=input("Enter The Password: ")
licn.checkp(inp)
    
main_start_time = time.time()

#input lists
cardno_list, exp_list, cvv_list, ipin_list, ilength, name_list, email_list, phone_list = gsinfo.getinfo2()

#Creating Report Output Headers
gsinfo.repheader() 

#initialization of variables   
plink=input("Enter the payment Link: ")
pamount=input("Enter the payment amount: ")
# name_1=input("Enter the name: ")
# email_1=input("Enter the email: ")
# phone_1=input("Enter the phone number: ")
mode=int(input("Enter Mode (1 = IPIN, 2 =  OTP): "))
start_index=int(input("Enter start index of the excel file (0 for default): "))
# name=str(name_1)
# email=str(email_1)
# phone=str(phone_1)

#Output lists
o_cardno_list=[None for x in range(ilength)]
o_exp_list=[None for x in range(ilength)]
o_cvv_list=[None for x in range(ilength)]
o_ipin_list=[None for x in range(ilength)]
status=[None for x in range(ilength)]
transaction_id_list=[None for x in range(ilength)]
t_time_list=[None for x in range(ilength)]

#driver=webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe")

# def pinwin():
#     for handle in driver.window_handles: 
#         if handle != main_page: 
#             pin_page = handle
#     return pin_page


for i in range(start_index,ilength):
    
    name=str(name_list[i])
    email=str(email_list[i])
    phone=str(phone_list[i])
        
    driver=webdriver.Chrome()
    payment_start_time=time.time()
    exp=str(exp_list[i])
    expmm=exp[0:2]
    expyr=exp[5:7]
    
    cvv=str(cvv_list[i])
    if len(cvv)==1:
        cvv='00'+cvv
    elif len(cvv)==2:
        cvv='0'+cvv
    driver.get(plink)
    main_page=driver.current_window_handle
    driver.implicitly_wait(20)
    #driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div[3]/a").click()
    
    name_el=driver.find_element_by_name("Applicant Name")
    name_el.send_keys(name)
    email_el=driver.find_element_by_name("Email")
    email_el.send_keys(email)
    phone_el=driver.find_element_by_name("Mobile Number")
    phone_el.send_keys(phone)
    amount_el=driver.find_element_by_name("Payable Amount")
    amount_el.send_keys(pamount)
    
    time.sleep(0.6)
    
    ctp_btn=driver.find_element_by_xpath('/html/body/div[3]/form/div[3]/ul/div[6]/div/span/button')
    ctp_btn.click()
    
    time.sleep(0.8)
    
    rdc_btn=driver.find_element_by_xpath('/html/body/app-root/div/div/app-payment-method/div/div[1]/div[3]/a')
    rdc_btn.click()
    
    print("\nPayment", i, "Details: ")
    cardno=str(cardno_list[i])
    cardno_el=driver.find_element_by_id('cc-number')
    cardno_el.send_keys(cardno)
    o_cardno_list[i]="'"+cardno
    print("\nCard Number:",cardno)
    time.sleep(0.7)
    expmm=expmm
    exp_el=driver.find_element_by_id('cc-exp-date')
    expf=expmm+expyr
    for ch in expf:
        exp_el.send_keys(ch)
    
    o_exp_list[i]=expmm+'/'+expyr
    time.sleep(0.4)
    cardholder=name
    cardholder_el=driver.find_element_by_id('card-holder-name')
    cardholder_el.send_keys(cardholder)
    time.sleep(0.9)
    cvv=cvv
    cvv_el=driver.find_element_by_id('cc-cvc')
    cvv_el.send_keys(cvv)
    o_cvv_list[i]=cvv
    
    time.sleep(1.2)
    
    paynow_el=driver.find_element_by_xpath('/html/body/app-root/div/div/app-rupay-debit-card/div/form/div[4]/div/button')
    paynow_el.click()
    driver.implicitly_wait(20)
    # pin_win=pinwin()
    # driver.switch_to.window(pin_win)
    
    
    if(mode==1):
        ipin=str(ipin_list[i])
        if len(ipin)==1:
            ipin='000'+ipin
        elif len(ipin)==2:
            ipin='00'+ipin
        elif len(ipin)==3:
            ipin='0'+ipin
        time.sleep(0.2)
        ipin_el=driver.find_element_by_name('txtipin') 
        ipin_el.send_keys(ipin)
        o_ipin_list[i]=ipin
        time.sleep(0.3)
        submit_btn=driver.find_element_by_id('btnverify')
        submit_btn.click()
        time.sleep(4)
        
        # while "SUCCESS" or "FAILED" not in driver.find_element_by_xpath('/html/body/div[2]/form/div/table/tbody/tr[10]/td[2]').text:
        #     pass
        # fstatus=driver.find_element_by_xpath('/html/body/div[2]/form/div/table/tbody/tr[10]/td[2]').text
        # print("\nPayment", i, "Details: ")
        # print(fstatus)
    
    else:
        while "ViewClientResponse?" not in driver.current_url:
            if "FAILED" in driver.find_element_by_xpath('/html/body/div[2]/form/div/table/tbody/tr[10]/td[2]').text:
                break
            pass
        fstatus=driver.find_element_by_xpath('/html/body/div[2]/form/div/table/tbody/tr[10]/td[2]').text
        print("\nPayment", i, "Details: ")
        print(fstatus)
    
    fstatus=driver.find_element_by_xpath('/html/body/div[2]/form/div/table/tbody/tr[10]/td[2]').text
    payment_end_time=time.time()
    payment_time_elapsed=payment_end_time-payment_start_time
    
    if "SUCCESS" in fstatus:
        status[i]="Success"
        print("Payment",i,"Success")
        transaction_id=driver.find_element_by_xpath('/html/body/div[2]/form/div/table/tbody/tr[2]/td[2]').text
        transaction_id_list[i]=transaction_id
    elif "FAILED" in fstatus:
        status[i]="Fail"
        print("Payment",i,"Fail")
        transaction_id=driver.find_element_by_xpath('/html/body/div[2]/form/div/table/tbody/tr[2]/td[2]').text
        transaction_id_list[i]=transaction_id
    else:
        status[i]="Status Unknown"
        print("Payment",i,"Status Unknown")
        transaction_id="NA"
        transaction_id_list[i]=transaction_id
        
    print("Transaction ID:", transaction_id)
    #payment_id=driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[1]/div[2]').text
    t_time_list[i]=payment_time_elapsed
    
    gsinfo.exwrite(o_cardno_list[i], o_exp_list[i], o_cvv_list[i], o_ipin_list[i], transaction_id_list[i], t_time_list[i], status[i], pamount)
    
    print("Payment",i,"Time Elapsed: ",payment_time_elapsed)
    driver.close()
    driver.quit()
    
#driver.quit()
main_end_time=time.time()
main_time_elapsed=main_end_time-main_start_time
#gsinfo.sendinfo(o_cardno_list, o_exp_list, o_cvv_list, transaction_id_list, t_time_list, status, main_time_elapsed, pamount)
gsinfo.summary(status, pamount, main_time_elapsed)
print("\nTotal time elapsed:", main_time_elapsed)


