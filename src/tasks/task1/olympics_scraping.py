import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://olympics.com"

def fetch_page_content(url, headers):
    """Fetches the HTML content of a web page given its URL and headers."""
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch page:", url)
            return None
    except Exception as e:
        print("Error occurred:", e)
        return None

def parse_venue_page(page_content):
    """Parses the HTML content of a venue page to extract venue information."""
    soup = BeautifulSoup(page_content, "html.parser")
    elements = soup.find_all(attrs={"data-cy": "list-item"})
    return elements

def parse_sport_page(page_content):
    """Parses the HTML content of a sport page to extract sport cards."""
    soup = BeautifulSoup(page_content, "html.parser")
    sports_cards = soup.find_all(attrs={"data-cy": "discipline-card-container"})
    return sports_cards


def extract_sport_data(card):
    """Extracts sport name and URL from a sport card element."""
    sport_name = card.find("h3").text.strip()
    sport_url = card.find(attrs={"data-cy": "link"})["href"]
    return sport_name, sport_url

def extract_date_from_event_block(block):
    """Extracts and formats the date from an event block."""
    date_span = block.find(attrs={"data-cy": "sport-schedule-date"})
    if date_span:
        day = date_span.find("h2").text.strip()
        month = date_span.find(class_="text--body").text.strip()
        months_map = {
            "Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04",
            "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08",
            "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"
        }
        month_number = months_map.get(month)
        formatted_date = f"{day}/{month_number}/2024"
        return formatted_date
    else:
        return None


def parse_events_page(page_content):
    """Parses the HTML content of an events page to extract event blocks."""
    soup = BeautifulSoup(page_content, "html.parser")
    event_blocks = soup.find_all(attrs={"data-cy": "event-list"})
    return event_blocks


def crawl_schedules(sports_urls, headers):
    """Crawls the schedule data for each sport and saves it to a CSV file."""
    schedules_df = pd.DataFrame(columns=["Event", "Sport", "Date", "Time", "Competitors"]) 
    for sport, url in sports_urls.items():
        page_content = fetch_page_content(base_url + url, headers)

        event_blocks = parse_events_page(page_content)
        
        for block in event_blocks:
            date = extract_date_from_event_block(block)
            events_containers = block.find_all(attrs={"data-cy": "videos-hero"})
            
            for event_info in events_containers:
                time_container = event_info.find(attrs={"class": "text--sm-body"})
                time = time_container.text.strip() if time_container else None
                event_name_container = event_info.find(class_="text--sm-text")
                event_name = (
                    event_name_container.text.strip() if event_name_container else None
                )
                competitor_containers = event_info.find_all(class_="text--sm-text")
                
                competitors = []
                for competitor in competitor_containers:
                    if competitor != event_name_container:
                        cmptr = competitor.text.strip()
                        if cmptr != '-': competitors.append(cmptr)

                new_entry = {
                    "Event": event_name,
                    "Sport": sport,
                    "Date": date,
                    "Time": time,
                    "Competitors": competitors,
                }
                
                schedules_df = schedules_df._append(new_entry, ignore_index=True)

    schedules_df.to_csv("schedulesA.csv", index=False)


def crawl_venues(url, headers):
    """Crawls the main venue page to extract venue data and sports URLs."""
    venues_df = pd.DataFrame(columns=["Venue", "Sports"])
    sports_urls = {}
    page_content = fetch_page_content(url, headers)
    if not page_content:
        return

    venues_content = parse_venue_page(page_content)
    for venue in venues_content:
        title = venue.find("h3").text.strip()
        venue_url = venue.find("a")["href"]
        venue_page_content = fetch_page_content(venue_url, headers)
        if not venue_page_content:
            continue

        sports_cards = parse_sport_page(venue_page_content)
        venue_sports = []
        for card in sports_cards:
            sport_name, sport_url = extract_sport_data(card)
            venue_sports.append(sport_name)
            if sport_name not in sports_urls:
                sports_urls[sport_name] = sport_url

        new_entry = {"Venue": title, "Sports": venue_sports}
        venues_df = venues_df._append(new_entry, ignore_index=True)

    venues_df.to_csv("venuesA.csv", index=False)
    return sports_urls


if __name__ == "__main__":
    url = f"{base_url}/fr/paris-2024/sites"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    }
    sports_urls= crawl_venues(url, headers)
    print("Venue data collection completed")
    crawl_schedules(sports_urls, headers)
    print("Schedule data collection completed")

