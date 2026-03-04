# Drug Information Search Using WHO Stems

This project provides a Python-based tool to identify pharmacological properties of drugs using WHO International Nonproprietary Name (INN) stems.

The World Health Organization (WHO) maintains a list of common stems used in INNs to indicate pharmacological classification. This application leverages that classification system and enriches it with additional pharmacological data retrieved from PubChem.

## Project Overview

1. Given a drug's International Nonproprietary Name (INN), the application:
2. Extracts and matches its WHO stem using a local JSON database (WHO 2024 Common Stems List).
3. Determines the pharmacological classification based on the stem.
4. Queries the PubChem API to retrieve detailed pharmacological information.
5. Stores the collected data in a local SQL database.
6. Uses an AI agent to translate English pharmacological descriptions into French.

## Features

* WHO stem recognition from INN names
* Pharmacological classification lookup
* Integration with PubChem API
* Structured data storage in SQL database
* Automated English-to-French translation using AI
* Web framework support (Flask or Django)

## Technologies Used

* Python
* Flask or Django
* JSON (WHO stems database)
* PubChem API
* OpenAI API
* SQL database (e.g., SQLite or PostgreSQL)

## Data Sources

* WHO 2024 List of Common Stems (INN classification)
* PubChem REST API

## Potential Use Cases

* Educational pharmacology tools
* Drug classification systems
* Research data enrichment
* Multilingual pharmacological databases
