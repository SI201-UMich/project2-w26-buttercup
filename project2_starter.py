# SI 201 HW4 (Library Checkout System)
# Your name: Jessica Smith and Sophia Buzzo
# Your student id: 21377559 and 41403841
# Your email: jesmithx@umich.edu and sbuzzo@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): we worked on our own
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
# yes
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    my_list = []
    html_file = "search_results.html"
    with open(html_file, 'r', encoding="utf-8-sig") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tags = soup.findall('div', class_='t1jojoys dir dir-ltr')
    id_tags = soup.findall('a', class_='l1j9v1wn bn2bl2p dir dir-ltr')
    for i in range(len(title_tags)):
        listing_id = re.find(r"\d{7,8}", id_tags[i].get('href', None).text())
        listing_tup = (title_tags[0].text(), listing_id)
        my_list.append(listing_tup)
    return my_list
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listing_details = {
        listing_id:{
            "policy_number": "",
            "host_type": "regular",
            "host_name": "",
            "room_type": "",
            "location_rating": 0.0

        }
    }
    html_file = f"listing_{listing_id}.html"
    if not os.path.exists(html_file):
        print(f"Error: File {html_file} does not exist.")
        return listing_details
    with open(html_file, 'r', encoding="utf-8-sig") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    policy_number_tag = soup.find('li', class_='ll4r3nl dir dir-ltr').text()
    if policy_number_tag:
        policy_number = policy_number_tag.get_text(strip=True)
        listing_details[listing_id]['policy_number'] = policy_number
    host_type_tag = soup.find('div', class_='_1mhorg9').text()
    if host_type_tag and 'Superhost' in host_type_tag.get_text():
        listing_details[listing_id]['host_type'] = 'Superhost'
    else:
        listing_details[listing_id]['host_type'] = 'regular'
    host_name_tag = soup.find('div', class_='_14i3z6h')
    if host_name_tag:
        host_name = host_name_tag.get_text(strip=True)
        listing_details[listing_id]['host_name'] = re.search(r'by\s(.*\s?a?n?d?[.*]?)', host_name)
    room_type_tag = soup.find('div', class_='ll4r2nl').text()
    if room_type_tag:
        room_type = room_type_tag.get_text(strip=True)
        if re.search(r'[Pp]?rivate', room_type):
            listing_details[listing_id]['room_type'] = 'Private Room'
        if re.search(r'[Ss]?hared', room_type):
            listing_details[listing_id]['room_type'] = 'Shared Room'
        else:
            listing_details[listing_id]['room_type'] = 'Entire Room'
    location_rating_tag = soup.find('span', class_='_17p6nbba')
    if location_rating_tag:
        try:
            location_rating = location_rating_tag.get_text(strip=True)
            try:
                rating = float(re.search(r'\d\.\d{1,2}', location_rating))
                listing_details[listing_id]['location_rating'] = rating
            except:
                pass
        except ValueError:
            pass
    return listing_details
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listing_database = []
    title_and_id = load_listing_results(html_path)
    for listing in title_and_id:
        title, listing_id = listing
        details = get_listing_details(listing_id)
        policy_number = details[listing_id]["policy_number"]
        host_type = details[listing_id]["host_type"]
        host_name = details[listing_id]["host_name"]
        room_type = details[listing_id]["room_type"]
        location_rating = details[listing_id]["location_rating"]
        listing_tup = title, listing_id, policy_number, host_type, host_name, room_type, location_rating
        listing_database.append(listing_tup)
    return listing_database
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        pass

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)