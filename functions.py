
def download_and_save_links(search_terms, db_file, executable_path="/usr/lib/python3.6/chromedriver"):
    '''
        Function loads chrome browser and gets individual links of results using given search terms.
        For each search term, results data will be saved in new table with search term as name in same database.
        
        Arguments:
            1. search_terms     - what to search. could be list or string, if it is a list, all string results will be searched
            2. db_file          - where to save information(new tables will be created for each term)
            3. executable_path  - where is chromedriver located(if you use chrome)
                                  (default is location in my case)

        -- Later added -- 
            also get property type. for this, click on filter of each type and get all results 
            that way(because, in other places this information seems not to be visible)
    '''

    ############################################
    def wait_to_load_page_num(br):

        from time import sleep as s

        while True:
            try:
                br.find_element_by_css_selector('''div[class="sr-usp-overlay__loading"]''')
                s(0.05)
            except:
                break
            
    ############################################

    # import 
    import re
    import sqlite3
    from selenium import webdriver
    from time import sleep as s

    base_url = "https://booking.com"
    # 1 term case
    if not isinstance(search_terms, list): search_terms = [search_terms]


    # GO
    for index, search_term in enumerate(search_terms):
        # define
        br = webdriver.Chrome(executable_path = executable_path)

        print("-"*70 + "\n", f"Process Started for search term {index + 1}/{len(search_terms)}| {search_term} |".center(70) + "\n", "-"*70 + "\n", sep="")
        # search
        br.get(base_url)
        br.find_element_by_css_selector("input[name='ss']").send_keys(search_term)
        br.find_element_by_css_selector("button[class='sb-searchbox__button  ']").click()
        print("-"*70 + "\n", "Getting Search Results".center(70) + "\n", "-"*70 + "\n", sep="")

        title_ = br.find_element_by_css_selector(".sorth1").text.strip()
        results_num = int(re.search(r":\s?([0-9,]+)", title_).group(1).replace(",", ""))
        print("-"*70 + "\n", f"Found {results_num} results".center(70) + "\n", "-"*70 + "\n", sep="")

        # import pdb; pdb.set_trace()

        # save * here
        results_dict = {}

        # click to see all types(if needed)
        types_ = br.find_elements_by_css_selector("div#filter_hoteltype div.collapsed_partly_link.collapsed_partly_more")
        if types_: types_[0].click()

        # -- edited -- search by categories
        property_types = {i.get_attribute("href"): i.text.split("\n")[0] for i in br.find_elements_by_css_selector("div[data-id='filter_hoteltype'] a")}
        
        for property_type_link, property_type_text in property_types.items():
            print(" | " + f"start getting property type | {property_type_text}".rjust(60))
            br.get(property_type_link)
        
            # get result pages number
            pages_num = 1

            pagination_items = br.find_elements_by_css_selector("li[class='bui-pagination__item sr_pagination_item']")
            recommendation = br.find_elements_by_css_selector("span.sr_autoextend_divider__icon")

            if not recommendation and pagination_items:
                pages_num = int(pagination_items[-1].text.strip())
           
            # we use this index, to see if results are above this in page source
            temp = "sr_autoextend_divider__icon"
            rec_index = len(br.page_source) 

            if temp in br.page_source:
                rec_index = br.page_source.index("sr_autoextend_divider__icon")

            # search results num            | it turns out, that site generates these numbers not very accurately for specific place
            title_ = br.find_element_by_css_selector(".sorth1").text.strip()

            try: # we had 2 different cases(maybe it is more)
                sub_results_num = int(re.search(r"^([0-9,]+)", title_).group(1).replace(",", ""))
            except:
                sub_results_num = int(re.search(r":\s?([0-9,]+)", title_).group(1).replace(",", ""))

            print("-"*70 + "\n", f"Pages Number: {pages_num}, results number: {sub_results_num}".center(70) + "\n", "-"*70 + "\n", sep="")

            for page_num in range(pages_num):
                # go to next page from second
                if page_num > 0: 
                    br.find_element_by_css_selector('''a[title='Next page']''').click()
                    wait_to_load_page_num(br)
                    s(1)

                # get info
                for i in br.find_elements_by_css_selector("a[class='hotel_name_link url']")[:sub_results_num]:
                    link = i.get_attribute('href'); link = link[:link.find("?")]
                    name = i.find_element_by_css_selector("span.sr-hotel__name").text.strip()

                    # import pdb; pdb.set_trace()
                    # add only if it is showing upper than possible yellow recommendation part
                    if rec_index > br.page_source.index(link[link.find("/hotel/"):]):
                        results_dict[link] = [name, property_type_text]

                # info
                print(" | " + str(page_num + 1).rjust(60), " | +")
            print(" | " + f" Completed | {property_type_text} ".center(60, "="))
        br.quit()
        

        conn = sqlite3.connect(db_file); c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS `{search_term}`(Link TEXT, Name TEXT, Property_Type)''')

        print("-"*70 + "\n", f'{search_term} download and table creation completed successfully '.center(70) + "\n", "-"*70 + "\n", sep="")

        for url, (name, property_type) in results_dict.items():
            c.execute(f'''INSERT INTO `{search_term}` VALUES (?, ?, ?)''', (url, name, property_type))
            conn.commit()
        print(" Completed! ".center(70, "="))
        br.quit()

    return True

################################################################################################################

def get_reviews(links_db, results_db):

    '''
        After using previous step, we can use generated database to retrieve
        individual reviews and store them in new databases 20 columns

        arguments:
            1. link_db - database generated from previous function(download_and_save_links)
            2. results_db - where to store results(new database)
    '''

    # # import
    import sqlite3
    from pprint import pprint as pp
    from selenium import webdriver
    from bs4 import BeautifulSoup as bs

    conn_0 = sqlite3.connect(links_db); c_0 = conn_0.cursor()
    # get table names from links tables
    search_terms = [i[0] for i in c_0.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    # start
    for index_, search_term in enumerate(search_terms):
        # get data
        url_names = {i:[j,k] for i, j, k in c_0.execute(f'''SELECT * FROM `{search_term}`''').fetchall()}

        print(f" Data retreived, start working on term N {index_ + 1}/{len(search_terms)} {search_term}".center(70, "="))
        print(f" | number of links: {len(url_names)}".center(70))
        # # load browser
        br = webdriver.Chrome(executable_path='/usr/lib/python3.6/chromedriver')
        # create new connection to save data
        conn = sqlite3.connect(results_db); c = conn.cursor()                               
        c.execute(f'''CREATE TABLE IF NOT EXISTS `{search_term}`(url TEXT,                  hotel_name TEXT,            type TEXT,
                                                                 address TEXT,              rank TEXT,                  reviews_number TEXT,
                                                                 average_score TEXT,        sub_review_scores TEXT,     review_date TEXT,
                                                                 reviewer TEXT,             country TEXT,               local_reviews_number TEXT,
                                                                 age_group TEXT,            review_local_score TEXT,    review_header_text TEXT,
                                                                 tags TEXT,                 review_neg TEXT,            review_pos TEXT,
                                                                 stay_date TEXT)''')

        # for each individual hotel link
        for index, (url, (name, type_ )) in enumerate(url_names.items()):
            try:
                # get all language reviews
                reviews_url_for_hotel = url.replace('/hotel/ge', "/reviews/ge/hotel") + "?page=1&r_lang=all" 
                br.get(reviews_url_for_hotel);   soup = bs(br.page_source, "html.parser")

                print("\n", f'''  {index + 1}  |  {name} | Started '''.center(70, "="), sep="")
                inner_page_counter = 0

                while soup.find("a", {"id":'review_next_page_link'}) or inner_page_counter == 0 :
                    if inner_page_counter: 
                        next_page = reviews_url_for_hotel.replace("?page=1", f"?page={inner_page_counter + 1}")
                        br.get(next_page);   soup = bs(br.page_source, "html.parser")

                    # get data from page we want
                    # address info & rank & number of reviews(top left)
                    address = soup.find('p', {'class': 'hotel_address'}).text.strip()
                    rank = int(soup.find('p', {'class': 'hotel_rank'}).text.strip().split(" ")[0].replace("#", ""))
                    reviews_number = int(soup.find('p', {'class': 'review_list_score_count'}).text.strip().split(" ")[2])

                    print("\n", "-" * 70, sep="")
                    print(f"Working on local page {inner_page_counter + 1}/{reviews_number // 75 + 1} (approximate number)".center(70))
                    print("-" * 70, sep="")
                    
                    # review scores from left panel
                    average_score = float(soup.find('div', {'id': 'review_list_score'}).find("span", {"class": "review-score-badge"}).text.strip())
                    sub_categories = [i.text.strip() for i in soup.select('ul#review_list_score_breakdown p.review_score_name')]
                    sub_scores     = [i.text.strip() for i in soup.select('ul#review_list_score_breakdown p.review_score_value')]
                    sub_review_scores = {category:score for category, score in zip(sub_categories, sub_scores)}

                    # reviews info from all pages (use pressing next button method, before it appears)
                    # get info
                    review_items = soup.select('li.review_item.clearfix')
                    
                    for inner_index, container in enumerate(review_items):                          #  Reviewed: November 22, 2018
                        review_date = container.select('p.review_item_date')[0].text.strip().split(":")[1].strip()
                        # reviewer_info (some elements may not be visible, like age group, count ... (?))
                        reviewer = container.select('p.reviewer_name')[0].text.strip()
                        country = container.select("span[itemprop='nationality']")[0].text.strip()
                        try:
                            local_reviews_number = int(container.select("div.review_item_user_review_count")[0].text.strip().replace(" Reviews", ""))
                        except:
                            local_reviews_number = ""
                        age_group = container.select("div.user_age_group")[0].text.strip().replace("Age group: ", "")
                        review_count = container.select("div.review_item_user_review_count")[0].text.strip().replace(" Reviews", "")
                        # review headers
                        inner_head = container.select('div.review_item_review div.review_item_review_header')
                        review_local_score = float(inner_head[0].select('div.review_item_header_score_container')[0].text.strip())
                        # review_header_text = inner_head.select('div.review_item_header_content').text.strip()
                        review_header_text = inner_head[0].select("span[itemprop='name']")[0].text 
                        # tags
                        tags_ = container.select('div.review_item_review ul.review_item_info_tags .review_info_tag ')
                        tags = [i.text.strip().replace("• ", "") for i in tags_]
                        
                        # positive & negative review text
                        # not all have negative or positive reviews together
                        
                        review_neg, review_pos = "", ""
                        review_neg_ = container.select('div.review_item_review div.review_item_review_content p.review_neg')
                        review_pos_ = container.select('div.review_item_review div.review_item_review_content p.review_pos')

                        if review_neg_: review_neg = review_neg_[0].text.strip()
                        if review_pos_: review_pos = review_pos_[0].text.strip()

                        # stayed info
                        try:
                            stay_date = container.select('div.review_item_review div.review_item_review_content p.review_staydate ')[0].text.replace("Stayed in ", "")
                        except:
                            stay_date = ""
                            
                        print(str(inner_index + 1).rjust(3), end="|")

                        c.execute(f'''INSERT INTO {search_term} values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                                                                         str(reviews_url_for_hotel if inner_page_counter == 0 else next_page) ,
                                                                         str(name),   str(type_),     str(address), 
                                                                         str(rank),                   str(reviews_number),
                                                                         str(average_score),          str(sub_review_scores),
                                                                         str(review_date),            str(reviewer),
                                                                         str(country),                str(local_reviews_number),
                                                                         str(age_group),              str(review_local_score),
                                                                         str(review_header_text),     str(tags),
                                                                         str(review_neg),             str(review_pos),
                                                                         str(stay_date)) )

                    conn.commit();  inner_page_counter += 1               
            except:
                continue
    br.quit()
