from selenium import webdriver
from selenium.webdriver.support.ui import Select
import gsinfo
import time
import licn
import getpass
usern=getpass.getuser()

inp=input("Enter The Password: ")
licn.checkp(inp)
    
main_start_time = time.time()

#input lists
cardno_list, exp_list, cvv_list, ipin_list, ilength, name_list, email_list, phone_list = gsinfo.getinfo()

#Creating Report Output Headers
gsinfo.repheader() 

#initialization of variables   
#plink=input("Enter the payment Link: ")
plink="file:///C:/Users/" + usern + "/Documents/Cards_safexpay/payment.html"
pamount=input("Enter the payment amount: ")
mode=int(input("Enter Mode (1 = IPIN, 2 =  OTP, 3 = PNB): "))
start_index=int(input("Enter start index of the excel file (0 for default): "))

#Output lists
o_cardno_list=[None for x in range(ilength)]
o_exp_list=[None for x in range(ilength)]
o_cvv_list=[None for x in range(ilength)]
o_ipin_list=[None for x in range(ilength)]
status=[None for x in range(ilength)]
transaction_id_list=[None for x in range(ilength)]
t_time_list=[None for x in range(ilength)]
error_msg_list=[None for x in range(ilength)]

driver=webdriver.Chrome()

for i in range(start_index,ilength):
    
    name=str(name_list[i])
    email=str(email_list[i])
    phone=str(phone_list[i])
        
    #driver=webdriver.Chrome()
    exp=str(exp_list[i])
    expmm=exp[0:2]
    expyr=exp[3:7]
    
    cvv=str(cvv_list[i])
    if len(cvv)==1:
        cvv='00'+cvv
    elif len(cvv)==2:
        cvv='0'+cvv
    driver.get(plink)
    main_page=driver.current_window_handle
    driver.implicitly_wait(20)
    payment_start_time=time.time()
    initiate_btn=driver.find_element_by_css_selector('[value="start"]')
    initiate_btn.click()
    
    name_el=driver.find_element_by_name("custName")
    name_el.send_keys(name)
    email_el=driver.find_element_by_name("emailId")
    email_el.send_keys(email)
    phone_el=driver.find_element_by_name("mobileNo")
    phone_el.send_keys(phone)
    submit_btn=driver.find_element_by_css_selector('[value="Submit"]')
    driver.execute_script("arguments[0].click();", submit_btn)
    
    # amount_el=driver.find_element_by_name("Payable Amount")
    # amount_el.send_keys(pamount)
    
#     #time.sleep(0.6)
    
#     ctp_btn=driver.find_element_by_xpath('/html/body/div[3]/form/div[3]/ul/div[6]/div/span/button')
#     ctp_btn.click()
    
#     #time.sleep(0.8)
    
#     rdc_btn=driver.find_element_by_xpath('/html/body/app-root/div/div/app-payment-method/div/div[1]/div[3]/a')
#     rdc_btn.click()
    
    print("\nPayment", i, "Details: ")
    cardno=str(cardno_list[i])
    cardno_el=driver.find_element_by_id('cdCardNumber')
    cardno_el.send_keys(cardno)
    o_cardno_list[i]="'"+cardno
    print("\nCard Number:",cardno)
    #time.sleep(0.4)
    cardholder=name
    cardholder_el=driver.find_element_by_id('name')
    cardholder_el.send_keys(cardholder)
    #time.sleep(0.7)
    expmm_select = Select(driver.find_element_by_id('cdExpiryMonth'))
    expmm_select.select_by_value(expmm)
    expyr_select = Select(driver.find_element_by_id('cdExpYear'))
    expyr_select.select_by_value(expyr)
    o_exp_list[i]=expmm+'/'+expyr
    #time.sleep(0.9)
    cvv=cvv
    cvv_el=driver.find_element_by_id('cdCVV')
    cvv_el.send_keys(cvv)
    o_cvv_list[i]=cvv
    #time.sleep(1.2)
    paynow_el=driver.find_element_by_xpath('/html/body/form/section/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[5]/div/button')
    paynow_el.click()
    driver.implicitly_wait(20)
    # pin_win=pinwin()
    # driver.switch_to.window(pin_win)
    
    # order_no=driver.find_element_by_xpath('/html/body/form/section/div/div/div/div[1]/div[3]/span[2]').text
    # print("Order Number: "+order_no)

#IPIN CARDS
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
        #time.sleep(0.3)
        submit_btn=driver.find_element_by_id('btnverify')
        submit_btn.click()
        payment_end_time=time.time()
        #time.sleep(4)
        
        while "mediaTransactionResponse" not in driver.current_url:
            if "YES" in driver.page_source:
                no_btn=driver.find_element_by_xpath('/html/body/form/div/div[1]/div/div/div/div/div/button[2]')
                no_btn.click()
                break
            pass
        if "Successful" in driver.page_source:
            fstatus=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[9]/div/div/div[2]/label').text
        else:
            fstatus=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[11]/div/div/div[2]/label').text
        # if "Successful" in driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[9]/div/div/div[2]/label').text:
        #     fstatus=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[9]/div/div/div[2]/label').text
        # else:
        #     fstatus=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[11]/div/div/div[2]/label').text
        # print("\nPayment", i, "Details: ")
        print(fstatus)

#OTP CARDS 
    elif mode==2:
        while "mediaTransactionResponse" not in driver.current_url:
            if "YES" in driver.page_source:
                no_btn=driver.find_element_by_xpath('/html/body/form/div/div[1]/div/div/div/div/div/button[2]')
                no_btn.click()
                break
            pass
        payment_end_time=time.time()
        if "Successful" in driver.page_source:
            fstatus=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[9]/div/div/div[2]/label').text
        else:
            fstatus=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[11]/div/div/div[2]/label').text
        print(fstatus)
        
#PNB CARDS
    elif mode==3:
        ipin=str(ipin_list[i])
        if len(ipin)==1:
            ipin='000'+ipin
        elif len(ipin)==2:
            ipin='00'+ipin
        elif len(ipin)==3:
            ipin='0'+ipin
        time.sleep(0.2)
        ipin_el=driver.find_element_by_name('pin') 
        ipin_el.send_keys(ipin)
        o_ipin_list[i]=ipin
        expmm_select = Select(driver.find_element_by_id('month'))
        expmm_select.select_by_value(expmm)
        expyr_select = Select(driver.find_element_by_id('expYear'))
        expyr_select.select_by_value(expyr[2:])
        submit_btn=driver.find_element_by_id('submitButton')
        submit_btn.click()
        payment_end_time=time.time()
        while "mediaTransactionResponse" not in driver.current_url:
            if "YES" in driver.page_source:
                no_btn=driver.find_element_by_xpath('/html/body/form/div/div[1]/div/div/div/div/div/button[2]')
                no_btn.click()
                break
            pass
        if "Successful" in driver.page_source:
            fstatus=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[9]/div/div/div[2]/label').text
        else:
            fstatus=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[11]/div/div/div[2]/label').text
        print(fstatus)
    
    payment_time_elapsed=payment_end_time-payment_start_time
    
    if "Successful" in fstatus:
        status[i]="Success"
        print("Payment",i,"Success")
        transaction_id=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[5]/div/div/div[2]').text
        transaction_id_list[i]=transaction_id
    elif "Failed" in fstatus:
        status[i]="Fail"
        print("Payment",i,"Fail")
        errormsg=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[4]/div/div/div[2]').text
        print("Error Message: ", errormsg)
        error_msg_list[i]=errormsg
        transaction_id=driver.find_element_by_xpath('/html/body/section/div/div/div/div/div/div[6]/div/div/div[2]').text
        transaction_id_list[i]=transaction_id
    else:
        status[i]="Status Unknown"
        print("Payment",i,"Status Unknown")
        transaction_id="NA"
        transaction_id_list[i]=transaction_id
        
    print("Transaction ID:", transaction_id)
    t_time_list[i]=payment_time_elapsed
    
    gsinfo.exwrite(o_cardno_list[i], o_exp_list[i], o_cvv_list[i], o_ipin_list[i], transaction_id_list[i], t_time_list[i], status[i], pamount, error_msg_list[i])
    
    print("Payment",i,"Time Elapsed: ",payment_time_elapsed)
    
driver.quit()
main_end_time=time.time()
main_time_elapsed=sum(t_time_list)
gsinfo.summary(status, pamount, main_time_elapsed)
print("\nTotal time elapsed:", main_time_elapsed)

