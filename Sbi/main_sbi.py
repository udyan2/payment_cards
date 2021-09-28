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
cardno_list, exp_list, cvv_list, ipin_list, ilength, name_list, email_list, phone_list, amount_list, invoice_list, dob_list= gsinfo.getinfo()

#Creating Report Output Headers
gsinfo.repheader() 

#initialization of variables   
plink=input("Enter the payment Link: ")

mode=int(input("Enter Mode (1 = IPIN, 2 =  OTP, 3 = PNB, 4 = YES BANK, 5 - EBIXOTP): "))
start_index=int(input("Enter start index of the excel file (0 for default): "))
tamount=0

#Output lists
o_cardno_list=[None for x in range(ilength)]
o_exp_list=[None for x in range(ilength)]
o_cvv_list=[None for x in range(ilength)]
o_ipin_list=[None for x in range(ilength)]
o_amount_list=[None for x in range(ilength)]
status=[None for x in range(ilength)]
transaction_id_list=[None for x in range(ilength)]
t_time_list=[None for x in range(ilength)]
error_msg_list=[None for x in range(ilength)]

driver=webdriver.Chrome()

for i in range(start_index,ilength):
    
    name=str(name_list[i])
    email=str(email_list[i])
    phone=str(phone_list[i])
    pamount=str(amount_list[i])
    invoice=str(invoice_list[i])
        
    #driver=webdriver.Chrome()
    exp=str(exp_list[i])
    expmm=exp[0:2]
    expyr=exp[3:7]
    
    cvv=str(cvv_list[i])
    if len(cvv)==1:
        cvv='00'+cvv
    elif len(cvv)==2:
        cvv='0'+cvv
    
    dob=dob_list[i]
    dobdd=dob[0:2]
    dobmm=dob[3:5]
    dobyr=dob[6:]    
    if '0' in dobdd:
        dobdd=dobdd[1:]
    elif '0' in dobmm:
        dobmm=dobmm[1:]
    dobmm=int(dobmm)
    driver.get(plink)
    main_page=driver.current_window_handle
    driver.implicitly_wait(20)
    payment_start_time=time.time()
    
    terms_chk=driver.find_element_by_id('proceedcheck_english')
    terms_chk.click()
    proceed_btn=driver.find_element_by_css_selector('[value="Proceed"]')
    proceed_btn.click()
    
    category_btn=driver.find_element_by_xpath('/html/body/div/section/div/div/div[1]/form/div/div/div[2]/div/div[2]/div/button')
    category_btn.click()
    category_drp=driver.find_element_by_xpath('/html/body/div/section/div/div/div[1]/form/div/div/div[2]/div/div[2]/div/div/ul/li[2]')
    category_drp.click()
    time.sleep(1)
    
    name_el=driver.find_element_by_name("outref11")
    name_el.send_keys(name)
    phone_el=driver.find_element_by_name("outref12")
    phone_el.send_keys(phone)
    invoice_el=driver.find_element_by_name("outref13")
    invoice_el.send_keys(invoice)
    email_el=driver.find_element_by_name("outref14")
    email_el.send_keys(email)
    amount_el=driver.find_element_by_name("outref15")
    amount_el.send_keys(pamount)
    
    name_el2=driver.find_element_by_id("cusName")
    name_el2.send_keys(name)
    invoice_el2=driver.find_element_by_name("mobileNo")
    invoice_el2.send_keys(phone)
    email_el=driver.find_element_by_name("emailId")
    email_el.send_keys(email)
    
    #Calender Input
    calender_img=driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div/form[2]/div[2]/div/div[3]/div[2]/div/div[2]/img')
    calender_img.click()
    dobyr_select=Select(driver.find_element_by_xpath('/html/body/div[2]/div/div/select[2]'))
    dobyr_select.select_by_value(dobyr)
    dobmm=dobmm-1
    dobmm_select=Select(driver.find_element_by_xpath('/html/body/div[2]/div/div/select[1]'))
    dobmm_select.select_by_value(str(dobmm)) 
    dateWidget = driver.find_element_by_id("ui-datepicker-div")
    rows = dateWidget.find_elements_by_tag_name("tr")
    columns = dateWidget.find_elements_by_tag_name("td")
    for cell in columns:
        if cell.text == dobdd:
            cell.find_element_by_link_text(dobdd).click()
            break
    
    #time.sleep(8)   #captcha time     
    
    #cptch_el_cursor=driver.find_element_by_id("passline")
    #cptch_el_cursor.send_keys("")
    
    captch_el=driver.find_element_by_id("captchaValue")
    captch_el.send_keys("")
    
    while "confirmpayment" not in driver.current_url:
        pass

    confirm_btn=driver.find_element_by_css_selector('[value="Confirm"]')
    driver.execute_script("arguments[0].click();", confirm_btn)
    
    clickhere_btn=driver.find_element_by_xpath('/html/body/div/form/section/div[2]/div/div[4]/div/a')
    clickhere_btn.click()
    
    print("\nPayment", i, "Details: ")
    cardno=str(cardno_list[i])
    cardno_el=driver.find_element_by_id('cardNumber')
    cardno_el.send_keys(cardno)
    o_cardno_list[i]="'"+cardno
    print("\nCard Number:",cardno)
    #time.sleep(0.4)
    cardholder=name
    cardholder_el=driver.find_element_by_id('cardholderName')
    cardholder_el.send_keys(cardholder)
    #time.sleep(0.7)
    expmm_select = Select(driver.find_element_by_id('expMnthSelect'))
    expmm_select.select_by_visible_text(expmm)
    expyr_select = Select(driver.find_element_by_id('expYearSelect'))
    expyr_select.select_by_visible_text(expyr)
    o_exp_list[i]=expmm+'/'+expyr
    #time.sleep(0.9)
    cvv=cvv
    cvv_el=driver.find_element_by_id('cvd2')
    cvv_el.send_keys(cvv)
    o_cvv_list[i]=cvv
    
    cptch_el_cursor=driver.find_element_by_id("passline")
    cptch_el_cursor.send_keys("")
    
    if mode==1 or mode==2 or mode==5:
        while 'txtipin' not in driver.page_source or 'otp' not in driver.page_source or 'authenticate' not in driver.current_url:
            if('txtipin' in driver.page_source):
                break
            if('otp' in driver.page_source):
                break
            if('authenticate' in driver.current_url):
                break
            pass
    # driver.implicitly_wait(15)

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

        while "responseredirect" not in driver.current_url:
            pass
        payment_end_time=time.time()
        if "successfully" in driver.page_source:
            fstatus="Successful"
        elif "pending" in driver.page_source:
            fstatus="Failed"

#OTP CARDS 
    elif mode==2:
        while "responseredirect" not in driver.current_url:
            pass
        payment_end_time=time.time()
        if "successfully" in driver.page_source:
            fstatus="Successful"
        elif "pending" in driver.page_source:
            fstatus="Failed"
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
        while "responseredirect" not in driver.current_url:
            pass
        payment_end_time=time.time()
        if "successfully" in driver.page_source:
            fstatus="Successful"
        elif "pending" in driver.page_source:
            fstatus="Failed"    
        print(fstatus)
        
#YES BANK CARDS
    elif mode==4:
        ipin=str(ipin_list[i])
        if len(ipin)==1:
            ipin='000'+ipin
        elif len(ipin)==2:
            ipin='00'+ipin
        elif len(ipin)==3:
            ipin='0'+ipin
        time.sleep(0.4)
        # submit_btn=driver.find_element_by_css_selector('[value="ATM PIN"]')
        # driver.execute_script("arguments[0].click();", submit_btn)
        atm_pin_el=driver.find_element_by_xpath('/html/body/div/div/div/div[4]/section/label[2]/span')
        atm_pin_el.click()
        expdate_el = driver.find_element_by_id('expDate')
        expdate=expmm+expyr
        for ch in expdate:
            expdate_el.send_keys(ch)
        ipin_el=driver.find_element_by_name('pin') 
        ipin_el.send_keys(ipin)
        o_ipin_list[i]=ipin
        submit_btn=driver.find_element_by_id('submitButtonIdForPin')
        submit_btn.click()
        payment_end_time=time.time()
        while "responseredirect" not in driver.current_url:
            pass
        payment_end_time=time.time()
        if "successfully" in driver.page_source:
            fstatus="Successful"
        elif "pending" in driver.page_source:
            fstatus="Failed"    
        print(fstatus)
        
#EBIXCASHOTP
    elif mode==5:
        while "responseredirect" not in driver.current_url:
            pass
        payment_end_time=time.time()
        if "successfully" in driver.page_source:
            fstatus="Successful"
        elif "pending" in driver.page_source:
            fstatus="Failed"
        print(fstatus)


    payment_time_elapsed=payment_end_time-payment_start_time
    
    if "Successful" in fstatus:
        status[i]="Success"
        print("Payment",i,"Success")
        transaction_id=driver.find_element_by_xpath('//*[@id="printdetailsformtop"]/div/div/div[2]/span/strong').text
        transaction_id_list[i]=transaction_id 
        tamount=tamount+amount_list[i]
    elif "Failed" in fstatus:
        status[i]="Fail"
        print("Payment",i,"Fail")
        transaction_id=driver.find_element_by_xpath('//*[@id="collect"]/div[2]/div/div[2]/span/strong').text        
        transaction_id_list[i]=transaction_id 
    print("Transaction ID:", transaction_id)
    t_time_list[i]=payment_time_elapsed
    
    gsinfo.exwrite(o_cardno_list[i], o_exp_list[i], o_cvv_list[i], o_ipin_list[i], transaction_id_list[i], t_time_list[i], status[i], amount_list[i], name, email, phone, dob, invoice, i)
    
    print("Payment",i,"Time Elapsed: ",payment_time_elapsed)
    
driver.quit()
main_end_time=time.time()
main_time_elapsed=sum(t_time_list)
gsinfo.summary(status, tamount, main_time_elapsed)
print("\nTotal time elapsed:", main_time_elapsed)