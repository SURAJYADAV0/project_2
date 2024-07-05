import requests
import pandas as pd
import json
from datetime import datetime, timedelta

# Define your state code and date range
state_code = "himachalpradesh"
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 6, 30)

# URL base and headers
base_url = "http://vegetablemarketprice.com/api/dataapi/market/{state}/daywisedata"
header = {
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,mr;q=0.7,hi;q=0.6",
    "cookie": "_ga=GA1.1.503742203.1720070934; _ga_2RYZG7Y4NC=GS1.1.1720074942.2.1.1720076437.0.0.0; FCNEC=%5B%5B%22AKsRol8wFKsNEYImWro2VGPkz9rY13RtrxwoeAZpzP04rLMUV8upySv02N6bXxIlt-6wQWW9yMP5He1f90RDpTXGbTqCEiIm9z39PUMyhMKkKKoTytWtFAyKdrVDX247yNgFRmCpz8ou-0hx4Ipj8mVZqX4Eca_m0Q%3D%3D%22%5D%5D",
    "Referer": f"http://vegetablemarketprice.com/market/{state_code}/today",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

# List to store data
all_data = []

# Iterate over each day in the range
current_date = start_date
while current_date <= end_date:
    # Format date as required by the API
    formatted_date = current_date.strftime("%Y-%m-%d")
    
    # Construct URL with the formatted date
    url = base_url.format(state=state_code) + f"?date={formatted_date}"
    
    # Request data from the API
    response = requests.get(url, headers=header)
    
    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON data
        js_data = json.loads(response.text)
        
        # Process each entry in the data
        for api in js_data["data"]:
            new_entry = {
                "date": formatted_date,
                "veg_name": str(api["vegetablename"]),
                "whole_price": str(api["price"]),
                "retail_price": str(api["retailprice"]),
                "shoping_mall_price": str(api["shopingmallprice"]),
                "unit": str(api["units"])
            }
            all_data.append(new_entry)
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
    
    # Move to the next day
    current_date += timedelta(days=1)

# Create DataFrame from collected data
df = pd.DataFrame(all_data)

# Save DataFrame to CSV
df.to_csv("vegetable_market_data.csv", index=False)
print("Data saved to 'vegetable_market_data.csv' successfully.")
