from selenium import webdriver
import gsinfo
import time
import passchk
import getpass
usern=getpass.getuser()

ipass=input("Enter The Password: ")
passchk.checkp(ipass)
    
main_start_time = time.time()

#input lists
cardno_list, exp_list, cvv_list, ipin_list, ilength, name_list, email_list, phone_list, amount_list, invoice_list, dob_list= gsinfo.getinfo()

#Creating Report Output Headers
gsinfo.repheader() 

#initialization of variables   
plink=input("Enter the payment Link: ")

mode=int(input("Enter Mode (1 = IPIN): "))
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
t_time_list=[0 for x in range(ilength)]
error_msg_list=[None for x in range(ilength)]
comhead="Flourized Solutions Pvt Ltd"

opt=webdriver.ChromeOptions()
opt.add_argument('--ignore-certificate-errors-spki-list')
driver=webdriver.Chrome(options=opt)

for i in range(start_index,ilength):
    
    
    name=str(name_list[i])
    email=str(email_list[i])
    phone=str(phone_list[i])
    pamount=str(amount_list[i])
    invoice=str(invoice_list[i])
        
    exp=str(exp_list[i])
    expmm=exp[0:2]
    expyr=exp[5:7]
    
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
    if comhead in driver.page_source:
        pass
    else:
        break
    amount_el=driver.find_element_by_id("customerAmount")
    amount_el.send_keys(pamount)
    iphone_el=driver.find_element_by_id("customerPhoneNumber")
    iphone_el.send_keys(phone)
    emailid_el=driver.find_element_by_id("customerEmail")
    emailid_el.send_keys(email)
    namein_el=driver.find_element_by_id("Name")
    namein_el.send_keys(name)
    pay_btn=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div/form/div[2]/div[1]/button')
    pay_btn.click()

    time.sleep(0.6)
    print("\nPayment", i, "Details: ")
    cardno=str(cardno_list[i])
    cardno_el=driver.find_element_by_id('CardNumber1')
    cardno_el.send_keys(cardno)
    o_cardno_list[i]="'"+cardno
    print("\nCard Number:",cardno)
    # time.sleep(0.4)
    cardholder=name
    cardholder_el=driver.find_element_by_id('CardHolderName1')
    cardholder_el.send_keys(cardholder)
    # time.sleep(0.7)
    exp_el = driver.find_element_by_id('CardDate1')
    exp_el.send_keys(expmm+expyr)
    o_exp_list[i]=expmm+'/'+'20'+expyr
    # time.sleep(0.9)
    cvv=cvv
    cvv_el=driver.find_element_by_id('CVVFormatter1')
    cvv_el.send_keys(cvv)
    o_cvv_list[i]=cvv
    
    paynow_btn=driver.find_element_by_xpath('/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div/form/div[9]/div/button')
    paynow_btn.click()
#     cptch_el_cursor=driver.find_element_by_id("passline")
#     cptch_el_cursor.send_keys("")
    
    if mode==1 or mode==2:
        while 'txtipin' not in driver.page_source or 'otp' not in driver.page_source:
            if(mode==1 and 'txtipin' in driver.page_source):
                break
            if(mode==2 and 'otp' in driver.page_source):
                break
            pass


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
        #time.sleep(4)

        while "response" not in driver.current_url:
            pass
        time.sleep(1)
        if "successful" in driver.page_source:
            fstatus="Successful"
        elif "failed" in driver.page_source:
            fstatus="Failed"
            
    payment_end_time=time.time()
    payment_time_elapsed=payment_end_time-payment_start_time
    
    if "Successful" in fstatus:
        status[i]="Success"
        print("Payment",i,"Success")
        transaction_id=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div/div/div/div[1]/div[3]/div[2]/p[2]').text
        transaction_id_list[i]=transaction_id 
        tamount=tamount+amount_list[i]
    elif "Failed" in fstatus:
        status[i]="Fail"
        print("Payment",i,"Fail")
        transaction_id=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div/div/div/div[1]/div[3]/div[2]/p[2]').text        
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
