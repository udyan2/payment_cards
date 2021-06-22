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