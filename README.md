# booking-com-reviews-scraper-by-search-term-and-property-type

For English, Please Scroll Down. ###############################################################################################

Scraper-ი, რომელიც საშუალებას გვაძლევს საძიებო ფრაზის/ფრაზების მითითებით მივიღოთ booking.com-ზე შესაბამისი ძიების განხორციელების შემდეგ გამოჩენილი შედეგების შესახებ ინფორმაცია. პროგრამა შექმნილია ერთ-ერთი საგანმანათლებლო ტიპის აქტივობის ხელშესაწყობად, კომპანია WSAA-ის მიერ (Facebook გვერდის ლინკი - https://www.facebook.com/Web-Scraping-And-Automation-477842576055490/).

გამოყენების ერთ-ერთი მაგალითი მოცემულია test.py-ფაილში.

მაგალითად თუ ავირჩევთ საძიებო ფრაზებს "Tbilisi" და "London", პროგრამა მიმდევრობით ჩატვირთავს ძიების შედეგად მიღებულ დაწესებულებათა ლინკებს და შეინახავს მათ საძიებო ფრაზის სახელით შექმნილ ცხრილში(თითო საძიებო ფრაზის მონაცემი შეინახება ფრაზის შესაბამისი სახელით შექმნილ ცხრილში), ბაზების სახელებს ჩვენ ვირჩევთ(იხილეთ სატესტო ფაილი). აღნიშნულ საფეხურზე, ხდება ინფორმაციის შენახვა დაწესებულების property type ტიპის გარჩევით, რისთვისაც გამოიყენება შედეგების ჩვენების შემდეგ მარცხენა მხარეს არსებული property type ფილტრი.

წინა საფეხურის გავლის შემდეგ, ხდება მიღებული ლინკების გამოყენებით შეფასებების გვერდებზე გადასვლა და თუ შეფასების რაოდენობა მეტია 5-ზე(რაც ამ ეტაპზე აუცილებელია შეფასებათა ქულის დასაგენერირებლად მარცხენა ზედა კუთხეში), მოხდება ყველა შეფასების შესახებ ინფორმაციის შენახვა შედეგების მონაცემთა(ახალ) ბაზაში წინა შემთხვევის ანალოგიური ცხრილის სახელებით. ინფორმაცია ინახება 20 სვეტში, რომელთა მნიშვნელობებსაც იმედია მარტივად გაარჩევთ.

ფუნქციები სწრაფადაა დაწერილი და საჭიროების შემთხვევაში შესაძლოა მათი მნიშვნელოვნად ოპტიმიზაცია(სიჩქარის თვალსაზრისით). ფუნქციების ბოლოს გამოყენებიდან მათში რამდენიმე სასარგებლო ცვლილება შევიტანეთ, თუმცა ყველაფრის სრულად დატესტვას დიდი დრო არ აქვს დათმობილი.

აუცილებელი მოთხოვნები: Python - 3.6 + & chromedriver | ბიბლიოთეკები: selenium & bs4

კითხვების შემთხვევაში, დაგვიკავშირდით.

############################################################################################### Scraper allows us to get information from booking.com using given search terms. Program is created by WSAA to support one of the educational activities (Facebook page link of company - https://www.facebook.com/Web-Scraping-And-Automation-477842576055490/).

One example uf its usage is given in test.py file.

For example, if we choose "Tbilisi" and "London" as our search terms, program will sequentially load pages that will show up after searching these terms and will save links of individual properties in a table with search term as name(there will be created separate table for each search term). We choose the names of databases(see test file). In this step, information is saved based on property type filter that is visible on upper left side of search results page.

After previous step, program continues loading each individual page and saves actual reviews data in new database, only if the number of reviews is greater than 5(this is the minimum number of reviews, that needs to be available to generate review score for property which is visible on upper left side). Information will be saved in 20 columns, hope their meanings will be clear for you.

Functions are written in a fast manner and if needed its possible to significantly optimize their performance. After their latest use, we made few helpful changes, but we have not spent much time to test everything.

Minimum requirements: Python - 3.6 + & chromedriver | Libraries: selenium & bs4

If you have any questions, feel free to contact us.

###############################################################################################
