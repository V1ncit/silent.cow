#!/bin/bash python3

import argparse
import sys
import configparser
import requests

#from googlesearch import search

# Check if googlesearch library is installed
try:
    from googlesearch import search
except ImportError:
    print("The 'googlesearch' library is not installed.")
    print("To install it on Linux, run the following command:")
    print("    pip install googlesearch-python")
    print("Exiting...")
    sys.exit(1)  # Exit the script since the library is required

# Function to load domains or queries from a file
def load_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to display help file
def display_helpfile():
    helpfile_path = 'help.txt'  # Hardcoded help file name
    try:
        with open(helpfile_path, 'r') as helpfile:
            print(helpfile.read())
    except FileNotFoundError:
        print(f"Help file '{helpfile_path}' not found. Please ensure the file exists in the same directory as this script.")

# Function to read API key and CSE ID from dorking.conf
def load_config(config_file='dorking.conf'):
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        api_key = config['google']['api_key']
        cse_id = config['google']['cse_id']
        return api_key, cse_id
    except KeyError as e:
        print(f"Missing configuration for {e} in {config_file}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Configuration file {config_file} not found.")
        sys.exit(1)

# Function to perform search using Google Custom Search JSON API
def google_search(query, api_key, cse_id, max_results=5):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': max_results  # Max number of results per query (limit 10 per API call)
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        search_results = response.json()
        return search_results.get('items', [])  # Return list of search items
    except requests.exceptions.RequestException as e:
        print(f"Error during the API request: {e}")
        sys.exit(1)

# Function to run Google dorking queries
def run_dorks(domain, queries, max_results=5):
    api_key, cse_id = load_config()  # Load credentials from config file
    for query in queries:
        dork_query = f"site:{domain} {query}"
        print(f"\nRunning query: {dork_query}\n")
        
        results = google_search(dork_query, api_key, cse_id, max_results)
        
        if results:
            for result in results:
                print(f"Title: {result['title']}")
                print(f"Link: {result['link']}")
                print(f"Snippet: {result.get('snippet', 'No description available')}\n")
        else:
            print("No results found.\n")

# Main execution flow
if __name__ == '__main__':
    # Argument parser for command-line flags
    parser = argparse.ArgumentParser(description="Automate Google Dorking with domain and query inputs")
    
    # Flags for single or list input for domains
    parser.add_argument('--single-domain', type=str, help="Provide a single domain for dorking")
    parser.add_argument('--domain-file', type=str, help="Provide a file with a list of domains (one per line)")
    
    # Flags for single or list input for queries
    parser.add_argument('--single-query', type=str, help="Provide a single query for dorking")
    parser.add_argument('--query-file', type=str, help="Provide a file with a list of queries (one per line)")
    
    # Flag for displaying the help file
    parser.add_argument('--helpfile', action='store_true', help="Display the help file with usage instructions")
    
    # Parse the arguments
    args = parser.parse_args()

    # Display help file if --helpfile flag is used
    if args.helpfile:
        display_helpfile()
        exit(0)

    # Handle domain input
    if args.single_domain:
        domains = [args.single_domain]
    elif args.domain_file:
        domains = load_from_file(args.domain_file)
    else:
        # Default to user input if no domain option is provided
        domain_input = input("No domain specified. Please enter a single domain: ")
        domains = [domain_input]
    
    # Handle query input
    if args.single_query:
        queries = [args.single_query]
    elif args.query_file:
        queries = load_from_file(args.query_file)
    else:
        # Default to user input if no query option is provided
        query_input = input("No query specified. Please enter a single query: ")
        queries = [query_input]
        
    # Clean the domain and query to remove extra quotes
    domain = args.domain.strip("'\"")
    query = args.query.strip("'\"")
    
    # Run dorks using the obtained domains and queries
    run_dorks(domains, queries)
