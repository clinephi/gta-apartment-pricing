# TEST CODE DISASSEMBLED
import requests # for HTML requests
from bs4 import BeautifulSoup # HTML parsing
import pandas as pd # For output data.
import re  # Parsing a few strings

# SETUP PARAMS
base_search = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/apartment/page-"
secondary_search = "/k0c37l1700273?sort=relevancyDesc&ad=offering"
new_ads = []
continue_search = True
page_num = 1

# LOOP THROUGH ADS
while continue_search:
    # STIR THE SOUP
    url = base_search + str(page_num) + secondary_search
    page = requests.get(url)  # Returns response object from url.
    soup = BeautifulSoup(page.content, "html.parser")

    # CHECK END CONDITION
    scraped_page_num = int( soup.find( "span", class_="selected" ).text )
    if scraped_page_num < page_num:
        continue_search = False  # we've maxed out pages and are getting redirected to max page.
        break  # kinda gross but whatever

    # LOG ITERS:
    print("Results for Page Number {0}".format(page_num))

    # GRAB ADS
    kijiji_ads = soup.find_all("div", {"class": "search-item regular-ad"})
    # SEARCH PROCEDURE
    for num, ad in enumerate(kijiji_ads):
        # ==== REQUEST AD  ==== #
        link = ad.get("data-vip-url")
        ad_url = "https://www.kijiji.ca" + link + "?null&siteLocale=en_CA"
        ad_page = requests.get(ad_url)
        ad_soup = BeautifulSoup(ad_page.content, "html.parser")
        print ( ad_url )
        # ==== IDENTIFY VARYING CLASSES ==== #
        # Price and address classes
        price_class, address_class, alternate_prop_class, h_class, description_class = None, None, None, None, None
        for span in ad_soup.find_all("span"):
            if span.has_attr("class"):
                if "currentPrice" in span["class"][0]:
                    price_class = span["class"][0]
                elif "address-" in span["class"][0]:
                    address_class = span["class"][0]
                elif "Bedrooms:" in span.text:  # TODO: make this more efficient.
                    alternate_prop_class = span["class"][0]

        # header class:
        for h in ad_soup.find_all("h3"):
            if h.has_attr("class"):
                if "attributeCardTitle-" in h["class"][0]:
                    h_class = h["class"][0]

        # Description class:
        for div in ad_soup.find_all("div"):
            if div.has_attr("class"):
                if "descriptionContainer-" in div["class"][0]:
                    description_class = div["class"][0]

        # ==== SCRAPE PROPS ==== #
        # Grab title
        title = ad.find('a', class_="title").text  # Done above right now to invalidate credit card ads.
        # Grab Images
        imgs = ad_soup.find_all("img")
        try:
            img1 = imgs[0]["src"]
            img2 = imgs[1]["src"]
            img3 = imgs[2]["src"]
        except:
            img1 = None
            img2 = None
            img3 = None
        # Grab price
        try:
            price = ad_soup.find( class_= price_class ).span.text
            price = float(
                price[1:].replace(",", "")
            )  # convert raw price string to float
        except:
            price = None

        # Grab address
        try:
            address = ad_soup.find(class_=address_class).text  # No idea why this isn't a span
        except:
            address = None

        # ==== Find properties in "Overview", "The Unit", and "The Building" Sections ==== #
        props = {}
        hydro_included, heat_included, water_included, laundry_included, backyard_included, gym_included = 0.0,0.0,0.0,0.0,0.0,0.0
        for hh in ad_soup.find_all("h3", class_=h_class):
            for li in hh.parent.ul:
                if li.has_attr("class"):
                    if "twoLinesAttribute-" in li["class"][0]:  # Pull all other attributes.
                        if li.dl.dt.text == "Furnished" or li.dl.dt.text == "Air Conditioning":
                            if li.dl.dd.text == "No":
                                props[li.dl.dt.text] = 0.0
                            else:
                                props[li.dl.dt.text] = 1.0
                        elif li.dl.dt.text == "Size (sqft)":
                            if li.dl.dd.text == "Not Available":
                                pass
                            else:
                                props[li.dl.dt.text] = li.dl.dd.text
                        else:
                            props[li.dl.dt.text] = li.dl.dd.text
                    elif "attributeGroupContainer-" in li["class"][0]:
                        # Utils case
                        if "Utilities Included" in li.div.h4.text:
                            for util_li in li.div.ul:
                                if util_li == "Not Included":
                                    pass  # Utils set to false
                                elif util_li.svg.has_attr("aria-label"):
                                    if util_li.svg["aria-label"] == "Yes: Hydro":
                                        hydro_included = 1.0
                                    elif util_li.svg["aria-label"] == "Yes: Heat":
                                        heat_included = 1.0
                                    elif util_li.svg["aria-label"] == "Yes: Water":
                                        water_included = 1.0

                        # Appliances case
                        if "Appliances" in li.div.h4.text:
                            for app_li in li.div.ul:
                                if app_li == "Not Included":
                                    pass  # Set to false
                                elif "Laundry" in app_li.text:
                                    laundry_included = 1.0

                        # Backyard case
                        if "Personal Outdoor Space" in li.div.h4.text:
                            if li.div.ul.text != "Not Included":
                                backyard_included = 1.0

                        # Amenities case:
                        if "Amenities" in li.div.h4.text:
                            for amenity in li.div.ul:
                                if amenity == "Not Included":
                                    pass  # no extra props to add
                                elif "Gym" in amenity.text:
                                    gym_included = 1.0

        # ==== Pull full text description ==== #
        # Don't bother pulling description rn.
        #ad_description_text = ""
        #for des_p in ad_soup.find("div", class_=description_class).div:
        #    ad_description_text += ("/n" + str(des_p))

        # ==== CATCH PULL TYPE 2 IF NECESSARY ==== #
        # Occasionally kijiji returns an html tree of a different
        # structure. I have no idea why, but we need to catch this general case
        # if the first failed. The affected attributes are Unit Type, # Bedrooms
        # , and # Bathrooms.
        # ------------------------------------------
        if "Unit Type" not in props or "Bedrooms" not in props or "Bathrooms" not in props:
            for span in ad_soup.find_all("span", class_=alternate_prop_class):
                if "Apartment" in span.text or "Basement" in span.text or "House" in span.text or "Condo" in span.text:
                    props["Unit Type"] = span.text
                elif "Bedrooms:" in span.text:
                    val = span.text.split( ":", 1)[1][1:]  # string of form "Bedrooms: [int]"
                    if val == "Bachelor/Studio":
                        props["Bedrooms"] = 1
                    elif " + Den" in val:
                        props["Bedrooms"] = int(val[0]) + 0.5 # Add .5 of a bed for den.
                    else:
                        props["Bedrooms"] = val
                elif "Bathrooms" in span.text:
                    props["Bathrooms"] = int("".join(filter(str.isdigit, span.text)))

        # Parse description for more info ???
        # Nothing right now

        # Pull lat/lon straight from site:
        apartment_lon, apartment_lat = None, None
        for meta in ad_soup.find_all("meta"):
            if meta.has_attr("property"):
                if meta["property"] == "og:latitude":
                    apartment_lat = meta["content"]
                elif meta["property"] == "og:longitude":
                    apartment_lon = meta["content"]

        # Instead, parse our walkscore site with Beautiful Soup bc their API only gives me
        # Walk not transit score.
        walk_score, transit_score, bike_score = None, None, None  # this is also gross.
        try:
            wk_score_call = (
                    "https://www.walkscore.com/score/loc/lat=" + str(apartment_lat) +
                    "/lng=" + str(apartment_lon)
            )
            wkscore_response = requests.get(wk_score_call)
            wkscore_soup = BeautifulSoup(wkscore_response.content, "html.parser")
            for img in wkscore_soup.find_all("img"):
                if img.has_attr("alt"):
                    if " Walk Score of " in img["alt"]:
                        walk_score = int(img["alt"][0:2])  # first two chars of string are score
                    elif " Transit Score of " in img["alt"]:
                        transit_score = int(img["alt"][0:2])
                    elif " Bike Score of " in img["alt"]:
                        bike_score = int(img["alt"][0:2])
        except:
            walk_score = None # i know this is gross just lazy.
            transit_score = None
            bike_score = None

        # ===== Check integrity of data ==== #
        # The following attributes are not optional:
        #       - price
        #       - sqr feet
        #       - A minimum of 3 images
        #       - Number of Bedrooms
        #       - Location
        #       - Number of bathrooms
        #       Any other parameters may be left out and will be assume to be False (e.g. backyard included..)
        good_ad = False
        if (   # TODO clean up logic with np.all()
                price is not None and
                apartment_lon is not None and
                apartment_lat is not None and
                props.get("Size (sqft)") is not None and
                # imgs is not None and  # Allow non-image data until we're using the CNN.
                props.get("Bedrooms") is not None and
                props.get("Bathrooms") is not None and
                walk_score is not None and
                transit_score is not None and
                bike_score is not None and
                props.get("Unit Type") is not None
        ):
            good_ad = True

        # Gather all our data and append to the master list which will go into our dataset
        if good_ad == True :
            ad_scraped_data = [
                title,
                address,
                props["Unit Type"],
                price,
                props["Bedrooms"],
                props["Bathrooms"],
                apartment_lat,
                apartment_lon,
                hydro_included,
                heat_included,
                water_included,
                laundry_included,
                backyard_included,
                props["Parking Included"],
                gym_included,
                props["Size (sqft)"],
                props["Furnished"],
                props["Air Conditioning"],
                walk_score,
                transit_score,
                bike_score,
                img1,
                img2,
                img3
            ]
            new_ads.append ( ad_scraped_data )

            # LOG
            print ( "Scraped ad....{0}".format( num ) )
            print ("        {0}".format(title))
            # print ("        {0}".format(ad_url))

    page_num += 1
# ==========================================================

# FORMAT OUR OUTPUT WITH PANDAS
headers = [
    "title",
    "address",
    "unit_type",
    "price",
    "bedrooms",
    "bathrooms",
    "apartment_lat",
    "apartment_lon",
    "hydro_included",
    "heat_included",
    "water_included",
    "laundry_included",
    "backyard_included",
    "parking_included",
    "gym_included",
    "sqft",
    "furnished",
    "air_conditioning",
    "walk_score",
    "transit_score",
    "bike_score",
    "img_1",
    'img_2"',
    "img_3",
]
ads_df = pd.DataFrame(
    new_ads,
    columns= headers
)
ads_df.to_excel ( "new_ads.xlsx" )
