import pandas as pd
import time
import os

# selenium==4.2.0 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Load the variables from the file
import pickle
with open("CA_data/variables.pickle", "rb") as f:
    df1,cCountys = pickle.load(f)

def download_ca_SpecEd(step3,subject,year,cCounty):
    driver.get(step3)
    
    report_select =  driver.find_elements(by=By.XPATH, value='//input[@name="cChoice"]')
    m=[report_select[i].get_attribute('value') for i in range(len(report_select))]

    for option in m:
        option_element = driver.find_element(by=By.XPATH, value=f"//input[@value='{option}']")
        option_element.click()

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Submit']"))
        )
        submit_button.click()
        
        # Step4: Get into the last website
        folder_path=os.path.join('./CA_data/',subject,option,year)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Write the table to an Excel file
        df = pd.read_html(driver.page_source)
        df[0].to_excel(os.path.join(folder_path,cCounty+'.xlsx'), index=False)

        with open(os.path.join(folder_path,cCounty+'.html'), 'w') as f:
            f.write(driver.page_source)
        time.sleep(1) 
        driver.back()
        
        
def download_ca_s4(step4,subject,cCounty,year,report=None): 
    driver.get(step4)

    # Step4: Get into the last website  # take all tables
    tables = driver.find_elements(by=By.TAG_NAME, value="table")

    # 将每个表格及其标题存储在不同的DataFrame中
    dfs = []
    for table in tables:  
        # convert table to DataFrame 
        df = pd.read_html(table.get_attribute("outerHTML"), header=0)[0]
        # add DataFrame into list
        if not df.empty:
            dfs.append(df)
            
    folder_path=os.path.join('./CA_data/',subject)  
    if report:
        folder_path=os.path.join(folder_path,report)
        
    folder_path=os.path.join(folder_path,year)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filepath=os.path.join(folder_path,cCounty+'.xlsx')
    
    sheet_names=['Sheet{}'.format(i+1)  for i in range(len(dfs))]
    if report and len(dfs)>=2:
        sheet_names[-2:]=[report,'ReportTotals']

    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')  
    for i, df in enumerate(dfs):
        df.to_excel(writer, index=False,sheet_name=sheet_names[i])
    writer.save()

    # Make sure all downaload have been finished
    time.sleep(1) 


def table_download(driver,filepath):
    tables = driver.find_elements(by=By.TAG_NAME, value="table")
    dfs = []
    for table in tables:  
        df = pd.read_html(table.get_attribute("outerHTML"), header=0)[0]
        if not df.empty:
            dfs.append(df)
    
    h_tags = driver.find_elements(by=By.TAG_NAME, value='h1') + \
                driver.find_elements(by=By.TAG_NAME, value='h2') 
                
    header=[]
    for h in h_tags:
        header.append(h.text) 
    header=[i for i in header if i != '']

    try:
        if len(header[0]+'-'+header[1])>31:
            sheet_names=[(header[0]+'-'+header[1]).replace(' ','')[0:31]]
            sheet_names.extend(header[2:])
        else:
            sheet_names=[header[0]+'-'+header[1]]
            sheet_names.extend(header[2:])
            
        if len(sheet_names) != len(dfs):
            #for i in range(abs(len(sheet_names)-len(dfs))):
            for i in range(len(sheet_names), len(dfs)):
                sheet_name = f"sheet{i+1}"
                sheet_names.insert(0, sheet_name)
    except:
        sheet_names=['Sheet{}'.format(i+1)  for i in range(len(dfs))]
                            
    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')  
    for i, df in enumerate(dfs):
        df.to_excel(writer, index=False,sheet_name=sheet_names[i])
    writer.save()

def download_ca_t2(step3,subject,cCounty,year): 
    driver.get(step3)

    report_select =  driver.find_elements(by=By.XPATH, value='//input[@name="cChoice"]')
    m=[report_select[i].get_attribute('value') for i in range(len(report_select))]

    form = driver.find_element(by=By.TAG_NAME, value="form")
    text = driver.execute_script("return arguments[0].textContent;", form)
    text=[t.strip('\t') for t in text.split('\n') if t.strip()]  
    text=[s.strip().replace('\xa0', '') for s in text]
    text=text[-len(m):]
    text=[i.lower() for i in text]

    dict_option={key: value for key, value in zip( m,text)}
    values_list = list(dict_option.values())
    for option, value in dict_option.items():
        if value+' (with district data)' in values_list or value+' (with dist. data)' in values_list:
            pass
        else:  # web scarping
            folder_path=os.path.join('./CA_data/',subject,option,year)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            option_element = driver.find_element(by=By.XPATH, value=f"//input[@value='{option}']")
            option_element.click()

            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Submit']"))
            )
            submit_button.click()
            
            a_tags = driver.find_elements(by=By.XPATH, value='//a[@data-toggle="collapse"]')
            for a in a_tags:
                ActionChains(driver).move_to_element(a).click().perform()
                time.sleep(0.5)

            # check if there are school filter option
            if driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'School Type')]") and driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Charter')]"):
                
                # non-char school
                nonchar_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@value="Y"]'))
                )
                nonchar_button.click()
                wait = WebDriverWait(driver, 4)
                filepath_nochar=os.path.join(folder_path,cCounty+'_no_char.xlsx')
                table_download(driver,filepath_nochar)
                
                # char shool
                char_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@value="N"]'))
                )
                char_button.click()
                filepath_char=os.path.join(folder_path,cCounty+'_char.xlsx') 
                table_download(driver,filepath_char)
                
                # download individual charter school data 
                tables = driver.find_elements(by=By.TAG_NAME, value="table")
                href_list=[]
                for table in tables:  
                    a_list = table.find_elements(by=By.XPATH, value='.//a')
                    href_list.append([a.get_attribute('href') for a in a_list])
                #href_list=max(href_list[1:-1], key=len)
                href_list = [sublist for sublist in href_list if not any('https://www.cde.ca.gov/' in element or 'agglevel=State' in element for element in sublist)]
                href_list = [sublist for sublist in href_list if any('agglevel=school' in element for element in sublist)]
                href_list = [item for sublist in href_list if sublist for item in sublist if item is not None]

                if len(href_list)>0:
                    for charschool in href_list:
                        download_ca_s4(charschool,subject,cCounty,year,report=None,char=True,option=option)
            else:
                filepath=os.path.join(folder_path,cCounty+'.xlsx') # no_char
                table_download(driver,filepath)

        time.sleep(1.5)
        driver.get(step3)
    

def download_url(subject,year,cCounty,level,cds):
    if subject=='SpecEd':
        step3='https://dq.cde.ca.gov/dataquest/SearchName.asp?rbTimeFrame=oneyear&rYear={}&cCounty={}&Topic={}&Level={}&submit1=Submit'.format(year,cCounty,subject,level) 
        #https://dq.cde.ca.gov/dataquest/SearchName.asp?rbTimeFrame=oneyear&rYear=2018-19&cCounty=01+ALAMEDA&Topic=SpecEd&Level=County&submit1=Submit
        download_ca_SpecEd(step3,subject,year,cCounty)  
    elif subject=='Foster':
        reports=['fosterGrdEnrl','fosterGrdRace']
        for report in reports:
            step4='https://dq.cde.ca.gov/dataquest/{}/{}.aspx?level={}&cds={}&year={}'.format(subject,report,level,cds,year)
            #https://dq.cde.ca.gov/dataquest/foster/fosterGrdEnrl.aspx?level=County&cds=01&year=2020-21
            #https://dq.cde.ca.gov/dataquest/foster/fosterGrdRace.aspx?level=County&county=01&year=2020-21
            download_ca_s4(step4,subject,cCounty,year,report)      
    elif subject =='Paif':
        reports=['StfFteClassified','StfFteClassifiedLevels']
        for report in reports:
            step4='https://dq.cde.ca.gov/dataquest/dqcensus/{}.aspx?cds={}&agglevel={}&year={}'.format(report,cds,level,year)
            #https://dq.cde.ca.gov/dataquest/dqcensus/StfFteClassified.aspx?cds=01&agglevel=County&year=2021-22
            #https://dq.cde.ca.gov/dataquest/dqcensus/StfFteClassifiedLevels.aspx?cds=01&agglevel=County&year=2021-22
            download_ca_s4(step4,subject,cCounty,year,report)
    elif subject=='FPRM':
        step4='https://dq.cde.ca.gov/dataquest/Cbeds2.asp?FreeLunch=on&cChoice=CoProf2&cYear={}&TheCounty={}&cLevel=County&cTopic={}&myTimeFrame=S&submit1=Submit'.format(year,cCounty,subject)
        #https://dq.cde.ca.gov/dataquest/Cbeds2.asp?FreeLunch=on&cChoice=CoProf2&cYear=2021-22&TheCounty=01%2CALAMEDA&cLevel=County&cTopic=FRPM&myTimeFrame=S&submit1=Submit
        download_ca_s4(step4,subject,cCounty,year,report=None)
    elif subject=='Hires':
        #https://dq.cde.ca.gov/dataquest/dqcensus/StfTchHires.aspx?cdcode=01&agglevel=County&year=2022-23
        step4='https://dq.cde.ca.gov/dataquest/dqcensus/StfTchHires.aspx?cdcode={}&agglevel={}&year={}'.format(cds,level,year)
        download_ca_s4(step4,subject,cCounty,year,report=None)
    else:    
        step3='https://dq.cde.ca.gov/dataquest/SearchName.asp?rbTimeFrame=oneyear&rYear={}&cCounty={}&Topic={}&Level={}&submit1=Submit'.format(year,cCounty,subject,level) 
        download_ca_t2(step3,subject,cCounty,year)


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

level='County'
for ind in df1.iloc[list(range(1,14))+[-2],:].index:
    subject=df1.loc[ind,'subject']
    years=df1.loc[ind,'exist_year']
    for year in years:
        for cCounty in cCountys[39:]:
            cds=cCounty.split('+')[0]
            
            try:
                download_url(subject,year,cCounty,level,cds)
                time.sleep(1)    
            except:
                print(subject,year,cCounty)
                #time.sleep(40) 
                driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)
                download_url(subject,year,cCounty,level,cds)
                