# Mobile Phone Data Scraper

This Python script, **`scraper.py`**, is designed to scrape mobile phone data from the [91mobiles](https://www.91mobiles.com/top-10-mobiles-in-india) website. It extracts information such as phone name, image link, price, expert comment, and specifications including performance, display, camera, and battery details. The scraped data is then stored in a CSV file.

### Prerequisites
- **Python 3:** Ensure you have Python 3 installed on your system. If not, you can download and install it from [python.org](www.python.org).
- **Libraries:** This script uses the following Python libraries which can be installed using pip:
    - **requests:** For making HTTP requests.
    - **BeautifulSoup:** For parsing HTML content.

You can install them using the following command:

```
pip install requests beautifulsoup4
```

## Usage
1. Clone the Repository 
```
git clone <repository_url>
cd <repository_folder>
```

2. Run the Scraper:
``` 
python scraper.py
```
This will execute the script, scrape the data from the 91mobiles website, and save it to a CSV file.

## Output
After running the script, the scraped data will be saved in a CSV file named `<title>.csv` where `<title>` is the title of the webpage being scraped. The CSV file will contain the following columns:

- Phone Name
- Image Link
- Price
- Expert Comment
- Performance
- Display
- Camera
- Battery

## License
This project is licensed under the MIT License 
