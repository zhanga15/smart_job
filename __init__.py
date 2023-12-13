#call APIfy client to extract data from google job scraper
import json
from apify_client import ApifyClient
import pandas as pd
from opensearchpy import OpenSearch, helpers



# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_IY3hoxDRTo2d2iF7NoZXPIOtFlDb8J1cSkPQ")

def scrape_jobs():

    all_job_data = []
    job_titles = ['Data Analyst','Data Scientist']
    job_locations = ['w+CAIQICIIbW9udHJlYWw=', 'w+CAIQICIHdG9yb250bw==']


    for title, loc in zip(job_titles, job_locations):
        run_input = {
                "queries": str(title).strip(),
                "maxPagesPerQuery": 1,
                "csvFriendlyOutput": False,
                "countryCode": 'ca',
                "languageCode": "",
                "maxConcurrency": 30,
                "saveHtml": False,
                "saveHtmlToKeyValueStore": False,
                "includeUnfilteredResults": False,
                "locationUule":str(loc).strip(),
                }
            
        run = client.actor("dan.scraper/google-jobs-scraper").call(run_input=run_input)
    
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            job_data = pd.json_normalize(item['googleJobs'])
            all_job_data.append(job_data)

    if all_job_data:
        result_df = pd.concat(all_job_data, ignore_index=True)       
        return result_df
    else:
        return pd.DataFrame()


def save_data_os(scrape_data):
    
    scrape_data = scrape_jobs()
    scrape_data.drop(columns= ['metadata.postedAt', 'thumbnail', 
    'metadata.workFromHome'], inplace=True)
    
    host = 'search-swift-hire-dev-jfmldmym4cfbiwdhwmtuqq6ihy.us-west-2.es.amazonaws.com'
    port = 443
    auth = ('swift', 'Hire123!') # For testing only. Don't store credentials in code.

    client_os = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = auth,
        use_ssl = True,
        ssl_assert_hostname = False,
        ssl_show_warn = False)
    #create table in ES
    # Create index if it doesn't exist (optional)
    index_name = 'scrape_test'
    if not client_os.indices.exists(index=index_name):
        client_os.indices.create(index=index_name)

    # Index the data into OpenSearch
    actions = [
        {
            "_op_type": "index",
            "_index": index_name,
            "_source": data.to_dict()
        }
        for i, data in scrape_data.iterrows()
    ]

    success, failed = helpers.bulk(client_os, actions)
    
    if success:
        print (f"Successfully indexed: {success} documents")
    else:
        print (f"Failed to index: {failed} documents")

