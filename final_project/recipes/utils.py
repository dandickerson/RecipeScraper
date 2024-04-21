from bs4 import BeautifulSoup
import requests


def scrape(url):
    """
      Scrapes the title of a recipe from a given URL using BeautifulSoup.

      Args:
          url: The URL of the recipe webpage.

      Returns:
          The extracted title of the recipe, or None if not found.
      """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        title_element = soup.find('h2', class_='tasty-recipes-title')
        if title_element:
            return title_element.text.strip()
        else:
            return None
        description_element = soup.find('div', {'class': 'tasty-recipes-description'})
        if description_element:
            return description_element
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the recipe: {e}")
        return None


# Example usage
user_url = input("Enter the recipe URL: ")
scraped_title = scrape(user_url)

if scraped_title:
    print(f"Scraped recipe title: {scraped_title}")
    # Use scraped_title to set the 'title' field in your Recipe object
else:
    print("Failed to scrape recipe title.")