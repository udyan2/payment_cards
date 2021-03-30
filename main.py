from selenium import webdriver
import gsinfo
import time
import sys

passw=input("Enter Password: ")
fobj=open("passw.txt","r")
if passw==fobj.readline():
    "Access Granted"
else:
    print("Access Denied: ")
    sys.exit()
    
main_start_time = time.time()

#input lists
cardno_list, exp_list, cvv_list, ipin_list, ilength = gsinfo.getinfo()

def pinwin():
    for handle in driver.window_handles: 
        if handle != main_page: 
            pin_page = handle
    return pin_page

#initialization of variables   
plink=input("Enter the payment Link: ")
pamount=input("Enter the payment amount: ")
name_1=input("Enter the name: ")
email_1=input("Enter the email: ")
phone_1=input("Enter the phone number: ")
mode=int(input("Enter Mode (1 = IPIN, 2 =  OTP): "))
start_index=int(input("Enter start index of the excel file (0 for default): "))
name=str(name_1)
email=str(email_1)
phone=str(phone_1)

#Output lists
o_cardno_list=[]
o_exp_list=[]
o_cvv_list=[]
o_ipin_list=[]
status=[]
transaction_id_list=[]
t_time_list=[]

#driver=webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe")

for i in range(start_index,ilength):
    
    payment_start_time=time.time()
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
    #driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div[3]/a").click()
    
    pn_but=driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div[3]/a")
    pn_but.click()
    
    driver.find_element_by_name("customerName").clear()
    name_el=driver.find_element_by_name("customerName")
    name_el.send_keys(name)
    email_el=driver.find_element_by_name("customerEmail")
    email_el.send_keys(email)
    phone_el=driver.find_element_by_name("customerNumber")
    phone_el.send_keys(phone)
    
    time.sleep(0.5)
    
    ctp_btn=driver.find_element_by_xpath('//*[@id="main_wrapper"]/div/div[2]/div/div[2]/div[1]/div[2]/div[4]/a')
    ctp_btn.click()
    
    time.sleep(0.5)
    
    dc_btn=driver.find_element_by_xpath('//*[@id="main_wrapper"]/div/div[2]/div/div[2]/div[2]/div[2]/ul/li[2]/a/span[2]')
    dc_btn.click()
   
    
    
    cardno=cardno_list[i]
    cardno_el=driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/input')
    cardno_el.send_keys(cardno)
    o_cardno_list.append(cardno)
    time.sleep(0.5)
    expmm=expmm
    expmm_el=driver.find_element_by_name('monthinput')
    expmm_el.send_keys(expmm)
    expyr=expyr
    expyr_el=driver.find_element_by_name('yearinput')
    expyr_el.send_keys(expyr)
    o_exp_list.append(expmm+'/'+expyr)
    time.sleep(0.5)
    cvv=cvv
    cvv_el=driver.find_element_by_name('cvvinput')
    cvv_el.send_keys(cvv)
    o_cvv_list.append(cvv)
    time.sleep(0.5)
    cardholder=name
    cardholder_el=driver.find_element_by_name('cardHolder')
    cardholder_el.send_keys(cardholder)
    
    time.sleep(1)
    
    paynow_el=driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/a')
    paynow_el.click()
    
    pin_win=pinwin()
    driver.switch_to.window(pin_win)
    
    if(mode==1):
        ipin=ipin_list[i]
        ipin_el=driver.find_element_by_name('txtipin') 
        time.sleep(1)
        ipin_el.send_keys(ipin)
        time.sleep(1)
        submit_btn=driver.find_element_by_id('btnverify')
        submit_btn.click()
        while "trans_id=" not in driver.current_url:
            if "failure" in driver.current_url:
                break
            pass
        url=driver.current_url
        print("\nPayment", i, "Details: ")
        print(url)
        #driver.switch_to.window(main_page)
    
    
    else:
        checkotp=input("Payment Completed (0:No, 1:Yes):")
        while "trans_id=" not in driver.current_url:
            pass
        url=driver.current_url
        print("\nPayment", i, "Details: ")
        print(url)
    
    
    payment_end_time=time.time()
    payment_time_elapsed=payment_end_time-payment_start_time
    
    if "success" in url:
        status.append("Success")
        print("Payment",i,"Success")
        transaction_id=url[((url.index("trans_id"))+15):]
        transaction_id_list.append(transaction_id)
    elif "Failure" or "failure" in url:
        status.append("Fail")
        print("Payment",i,"Fail")
        transaction_id=url[((url.index("trans_id"))+15):]
        transaction_id_list.append(transaction_id)
    else:
        status.append("Status Unknown")
        print("Payment",i,"Status Unknown")
        transaction_id="NA"
        transaction_id_list.append(transaction_id)
        
    print("Transaction ID:", transaction_id)
    #payment_id=driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[1]/div[2]').text
    t_time_list.append(payment_time_elapsed)
    print("Payment",i,"Time Elapsed: ",payment_time_elapsed)
    driver.close()
    
driver.quit()
main_end_time=time.time()
main_time_elapsed=main_end_time-main_start_time
gsinfo.sendinfo(o_cardno_list, o_exp_list, o_cvv_list, transaction_id_list, t_time_list, status, main_time_elapsed, pamount)
print("\nTotal time elapsed:", main_time_elapsed)


