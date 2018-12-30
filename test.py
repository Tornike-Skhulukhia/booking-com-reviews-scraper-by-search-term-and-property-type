
# place needs at least 5 review, to work ...
# do not truly rely on numbers (including printed), because site does not show things as we may expect...

# import
from functions import download_and_save_links, get_reviews
# what to find
search_terms = ['tbilisi']
# where to save data
links_db = "links.db"
results_db ="results.db"


################################################
#######              GO                 ########
################################################

# at first, get results links
download_and_save_links(search_terms, links_db)
# get individual reviews data
get_reviews(links_db, results_db)