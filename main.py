from selenium import webdriver
import getinfo


cardno_list, exp_list, cvv_list, ipin_list, ilength = getinfo.info()

def pinwin():
    for handle in driver.window_handles: 
        if handle != main_page: 
            pin_page = handle
    return pin_page

      
plink=input("Enter the payment Link: ")
pamount=input("Enter the payment amount: ")
name_1=input("Enter the name: ")
email_1=input("Enter the email: ")
phone_1=input("Enter the phone number: ")
name=str(name_1)
email=str(email_1)
phone=str(phone_1)

#driver=webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe")
ilength=2

for i in range(ilength):
    
    driver=webdriver.Chrome()
    exp=str(exp_list[i])
    expyr=exp[0:2]
    expmm=exp[3:8]
    
    cvv=str(cvv_list[i])
    if len(cvv)==1:
        cvv='00'+cvv
    elif len(cvv)==2:
        cvv='0'+cvv
    driver.get(plink)
    main_page=driver.current_window_handle
    driver.implicitly_wait(10)
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
    
    ctp_btn=driver.find_element_by_xpath('//*[@id="main_wrapper"]/div/div[2]/div/div[2]/div[1]/div[2]/div[4]/a')
    ctp_btn.click()
    
    dc_btn=driver.find_element_by_xpath('//*[@id="main_wrapper"]/div/div[2]/div/div[2]/div[2]/div[2]/ul/li[2]/a/span[2]')
    dc_btn.click()
    driver.close()

    
    #cardno=cardno_list[i]
    
    
    # cardno=cardno_list[i]
    # cardno_el=driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/input')
    # cardno_el.send_keys(cardno)
    # expmm=expmm
    # expmm_el=driver.find_element_by_name('monthinput')
    # expmm_el.send_keys(expmm)
    # expyr=expyr
    # expyr_el=driver.find_element_by_name('yearinput')
    # expyr_el.send_keys(expyr)
    # cvv=cvv
    # cvv_el=driver.find_element_by_name('cvvinput')
    # cvv_el.send_keys(cvv)
    # cardholder=name
    # cardholder_el=driver.find_element_by_name('cardHolder')
    # cardholder_el.send_keys(cardholder)
    
    # paynow_el=driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/a')
    # paynow_el.click()
    
    # pin_win=pinwin()
    # driver.switch_to.window(pin_win)
    
    # ipin=ipin_list[i]
    # ipin_el=driver.find_element_by_name('txtipin') 
    # ipin_el.send_keys(ipin)
    
    # submit_btn=driver.find_element_by_id('btnverify')
    # submit_btn.click()
    # driver.switch_to.window(main_page)
    
    # payment_status=driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[1]/div[1]').text
    # payment_id=driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[1]/div[2]').text
    # print(payment_status,payment_id)

driver.quit()

