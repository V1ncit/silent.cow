#!/bin/bash

# Domæne, som du vil tjekke certifikater for
DOMAIN="eksempel.dk"

# CertSpotter API base URL
API_URL="https://api.certspotter.com/v1/issuances?domain=$DOMAIN&include_subdomains=true&expand=dns_names"

# Variabel til at gemme alle resultater
all_results=""

# Start med at hente den første side
next_url=$API_URL

# Så længe der er en næste side, fortsæt
while [[ -n "$next_url" ]]; do
  # Foretag API kald og gem svaret i variablen response
  response=$(curl -s $next_url)

  # Tilføj de nuværende resultater til den samlede liste
  all_results+=$(echo "$response" | jq '.')

  # Tjek om der er en næste side (pagination)
  next_url=$(echo "$response" | jq -r '.[] | select(.next) | .next')

  # Hvis der ikke er flere sider, sæt next_url til tom (stopper løkken)
  if [[ "$next_url" == "null" ]]; then
    next_url=""
  fi
done

# Tjek om vi har samlet resultater
if [[ -z "$all_results" ]]; then
  echo "Ingen data modtaget fra CertSpotter API'en."
  exit 1
fi

# Udskriv alle resultaterne
echo "Certifikater for $DOMAIN:"
echo "$all_results"
