#!/bin/bash python3

import argparse
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

# Function to run Google dorking queries
def run_dorks(domains, queries):
    for domain in domains:
        print(f"\nRunning dorking queries for: {domain}\n")
        for query in queries:
            # Add "site:{domain}" in front of each query
            dork_query = f"site:{domain} {query}"
            print(f"Query: {dork_query}")

            try:
                # Run the search and return a limited number of results (e.g., 5)
                for result in search(dork_query, num_results=5):
                    print(f"Found: {result}")
            except Exception as e:
                print(f"Error while searching: {e}")

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

    # Run dorks using the obtained domains and queries
    run_dorks(domains, queries)
