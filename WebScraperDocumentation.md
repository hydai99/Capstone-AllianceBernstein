# Documentation of Web Scraper

## Idea of Web Scraper

The web scraper is designed to automate the process of downloading data from websites. Here is an overview of the main steps involved:

1. Manual Inspection: Begin by manually inspecting the website to understand how to download the desired data. Take note of the following:

   - Identify the link format closest to the download page.
   - Determine the required information for each step of the download process.
   - Observe if the link changes after interacting with any options or buttons.

2. Simulate Human Action: Once the manual inspection is complete, use code to simulate actions and navigate to the desired download page. This may involve:

   - Programmatically inputting the required information for each step.
   - Clicking buttons or selecting options to proceed to the download page.

3. Save to Folders: After reaching the download page, extract the download link and save the downloaded files to the appropriate folders. Ensure the files are saved in an organized manner.


## Usage
The web scraper is divided into three main types based on the characteristics of our target website. Each type requires a specific approach and set of instructions to perform the scraping effectively. The types are as follows:

1. Type 1: Scraping websites with consistent download link formats using _Requests_ library.
2. Type 2: Scraping websites using the _Selenium_ library.
3. Type 3: Scraping require information from a specified webpage using the _Beautiful Soup_ library.

Detailed instructions and code examples for each type are provided below.


### Type 1: Scraping websites with consistent download link formats using _Requests_ library.

This type of web scraping is applicable to websites that have a consistent format for their download links. By understanding the structure of the download links, we can use the Requests library to automate the process of downloading data. 

Here is an example from the last chunk of `00_TX_initial_crawler.ipynb`.

1. Manually identify the steps required to download the files from the website. For example, consider the following steps:
   - Start at the URL: `https://rptsvr1.tea.texas.gov/perfreport/tprs/tprs_srch.html`.
   - Input the required information, such as:
     - Level: District
     - Method: District ID
     - District ID: _Enter the district ID number_
   - Click the search button (Note: The link remains the same after clicking)
   - Choose each report and click the "View Report" button.
2. On the report page, there will usually be a download button that can be clicked to initiate the download.
   - To obtain the download link, you can use Developer Tools in your browser (press `Fn + F12`) and inspect the network requests.
   - Look for the request associated with the download button and find the download link in the request details.
   - The download link may be in the form of a JavaScript redirect, for example:

     ```javascript
     location.href='/cgi/sas/broker?_service=marykay&_program=perfrept.perfmast.sas&_debug=0&lev=D&id=057905&prgopt=reports/tapr/performance.sas&ccyy_value=2021&dest=E'
     ```
     Note that sometimes you may need to add the main domain link (`https://rptsvr1.tea.texas.gov`) before the given download link to obtain the complete download link, as shown in the example.
   - Analyze multiple instances of download links to identify commonalities and variables.
   - If the download link does not provide a year, try selecting a different year on the page and observe if the link changes.
   - Based on the analysis, you can create a template for the download link with variables, such as:
     ```python
     'https://rptsvr1.tea.texas.gov/cgi/sas/broker?_service=marykay&_program=perfrept.perfmast.sas&_debug=0&lev=D&id={}&prgopt=reports/tapr/performance.sas&ccyy_value={}&dest=E'.format(id, year)
     ```
3. Utilize a loop to repeat the process for each district ID and year to download the data. Here's an example code snippet:
   ```python
   years = ['2019', '2021', '2022']
   for name, id in zip(Ktx['district_name'], Ktx['district_id']):
       for year in years:
           download_link = 'https://rptsvr1.tea.texas.gov/cgi/sas/broker?_service=marykay&_program=perfrept.perfmast.sas&_debug=0&lev=D&id={}&prgopt=reports/tapr/performance.sas&ccyy_value={}&dest=E'.format(id, year)
           response = requests.get(download_link)

           folder_name = name
           folder = os.path.join('excel report', folder_name)
           file_name = id + '_' + year + '.xlsx'
           file = os.path.join(folder, file_name)
           os.makedirs(folder, exist_ok=True)

           with open(file, 'wb') as f:
               f.write(response.content) 
    ```


### Type 2: Scraping websites using the _Selenium_ library.

This type of web scraping is suitable for websites where the final data page does not provide a download button or where it is challenging to find a common pattern from the URL. Selenium is a powerful library that allows automation of browser actions and interaction with web elements. Here are the steps to set up and use Selenium for web scraping:

1. Set up Selenium by installing the library and configuring the webdriver for your chosen browser. For example, to set up Selenium with Chrome:

   ```python
   !pip install selenium==4.2.0 

   from selenium import webdriver
   from selenium.webdriver.support.ui import Select
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   from selenium.webdriver.common.by import By

   chrome_options = webdriver.ChromeOptions()
   prefs = {'download.default_directory' :  'output/path'}
   chrome_options.add_experimental_option('prefs', prefs)
   chrome_options.add_argument('--headless')  # allows the browser to run without a visible user interface
   driver = webdriver.Chrome(executable_path='/your/path/to/chromedriver', options=chrome_options)
   ```

2. Familiarize yourself with some commonly used commands in Selenium:
- Navigate to a specified link using `driver.get(link)`.
- Click on elements such as buttons or radio buttons. To do this, you need to identify the XPath corresponding to the element you want to click using the browser's Developer Tools. Once you have the XPath, you can define it as a variable and use the `.click()` method to click the button. For example:

    ```python
    continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue']")))
    continue_button.click()

    nonchar_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@value="Y"]'))
    )
    nonchar_button.click()

    char_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@value="N"]'))
    )
    char_button.click()
    ```

    Similar actions can be performed for other buttons by modifying the XPath and value.

 - When dealing with `<select>` elements, use its class and name to interact with them. For example, if the HTML source code includes `<select name="dsname" size="20">`, you can get all the option values and then iterate through each option and click on it using a loop. Here are code snippet:

    ```python
    dsname_select = Select(driver.find_element_by_name("dsname"))
    option_values = [option.get_attribute("value") for option in dsname_select.options]
    for option in option_values:
            driver.find_element_by_xpath(f"//option[@value='{option}']").click()
    ```

 - To handle checkboxes, you can use the `find_elements_by_xpath` method to find all elements of type `checkbox` and extract their values.

    ```python
    checkboxes = driver.find_elements_by_xpath("//input[@type='checkbox']")

    # get all value of checkbox
    data_element=[]
    for checkbox in checkboxes:
        data_element.append(checkbox.get_attribute("value"))
    ```

 - Similarly, you can find elements using other attributes like `cChoice`, `<h>`, `<table>`, or `<form>` tags using `find_elements` methods and perform actions accordingly. Here are code snippet:

    ```python
    report_select =  driver.find_elements(by=By.XPATH, value='//input[@name="cChoice"]')
    m=[report_select[i].get_attribute('value') for i in range(len(report_select))]

    driver.find_elements(by=By.TAG_NAME, value='h1')

    driver.find_elements(by=By.TAG_NAME, value="table")
    for table in tables:  
        df = pd.read_html(table.get_attribute("outerHTML"), header=0)[0]

    form = driver.find_element(by=By.TAG_NAME, value="form")
    text = driver.execute_script("return arguments[0].textContent;", form)
    ```

 - You can open collapsed sections on the page by finding `<a>` tags with the attribute `data-toggle="collapse"` and using the `ActionChains` class to move to the element and perform a click action. 

    ```python
    a_tags = driver.find_elements(by=By.XPATH, value='//a[@data-toggle="collapse"]')
    for a in a_tags:
        ActionChains(driver).move_to_element(a).click().perform()
        time.sleep(2)
    ```

 - You can navigate back to the previous page using `driver.back()`.

 - To quit the browser and release system resources, use `driver.quit()`.

These commands provide a starting point for interacting with web elements using Selenium. By combining them strategically and based on the specific website's structure, you can scrape data effectively even from websites with complex layouts or limited direct download options.



### Type 3: Scraping require information from a specified webpage using the _Beautiful Soup_ library.

This type of web scraping involves extracting specific information from a webpage using the Beautiful Soup library. 

Here is an example from `11.1_CA_preprocess.py`.

1. Fetch the webpage source code using the Requests library:

    ```python
    url = 'https://dq.cde.ca.gov/dataquest/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    ```

    In this step, the URL of the webpage is specified, and the Requests library is used to retrieve the source code. The Beautiful Soup library is then employed to parse the HTML content.

2. Inspect the webpage using Developer Tools or any browser's inspect mode to identify the required information. Once the target elements are identified, Beautiful Soup can used to extract the desired information.
   
    ```python
    for select in soup.find_all('select'):
        for option in select.find_all('option'):
            label = option.get('label')
    ```

    In the given example, a loop is used to find all `select` elements in the webpage source code, and within each `select` element, another loop finds all `option` elements. The `label` attribute of each `option` element is then extracted to obtain the required information.

    Please refer to the [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for more details on how to navigate and extract data from HTML using Beautiful Soup.

## File Organization

The file organization for the Texas and California web scraping projects is as follows:

```bash
├── 00_TX_initial_crawler.ipynb
├── 10+20_TX_WebScraper+Map.ipynb
├── 11_CA_WebScraper.ipynb
├── 11.1_CA_preprocess.py
├── 11.2_CA_webscraper.py
```

### Texas

- `00_TX_initial_crawler.ipynb`: This Jupyter Notebook file contains code to map district names and their IDs. It also includes code to download reports from the website https://rptsvr1.tea.texas.gov/perfreport/tprs/tprs_srch.html based on district ID and year. However, it is mentioned that this code was later abandoned in favor of downloading from another entry point.

- `10+20_TX_WebScraper+Map.ipynb`: This Jupyter Notebook file combines web scraping and mapping functionalities. It includes the following steps:
  1. Web scraping to download all reports and integrate them into corresponding years.
  2. Web scraping to retrieve all metrics and elements, identifying their existence in each year and the elements corresponding to the metrics.
  3. Web scraping to obtain the datadict file (PDF) and convert it to CSV using **Azure Form Recognizer**. Two sets of code are provided, one for the paid key version and one for the free key version.
  4. Processing the datadict file to transform unstructured data into structured data.
  5. Writing functions to search for metrics and explanation from datadict.


### California


- `11_CA_WebScraper.ipynb`: This Jupyter Notebook combines the functionality of `11.1_CA_preprocess.py` and `11.2_CA_webscraper.py`. It provides more detailed examples of the code for the California web scraping project.

- `11.1_CA_preprocess.py`: This Python script is used to gather required information and save it for use in `11.2_CA_webscraper.py`. It performs the following tasks:
  1. Obtaining all report and county information.
  2. Gathering all subject/topic options.

- `11.2_CA_webscraper.py`: This Python script contains the web scraping code for downloading reports. The code is categorized into three classes based on the download method and the number of subpages. The code for each category of report is adjusted accordingly to improve download speed. It also performs the following tasks:
  1. After running the code and obtaining the data, the script will output information about reports that were not successfully downloaded. The code also provides a convenient way to re-download the missing parts
  2. Defines functions for downloading the source code and processing tables. These functions are used to retrieve the necessary data from the web pages.