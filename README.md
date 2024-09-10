# ahrefs API testing
Testing use of ahrefs api for common SEO workflows

# Keyword Mapping Script

This repository contains a Python script to automate keyword research for URLs using the Ahrefs API. The script fetches organic keywords, ranks them based on various metrics, and outputs the best keyword for each URL.

## Requirements

- **Python 3.x**: A programming language needed to run the script.
- **Ahrefs API Key**: An authentication key from Ahrefs to access their API.
- **Required Libraries**: Additional Python packages (`requests`, `pandas`, `python-dotenv`) to help handle web requests, data manipulation, and environment variables.

## Instructions

### 1. Install Python

- **Mac**:
  - Open Terminal and install Homebrew (if not already installed):
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
  - Install Python:
    ```bash
    brew install python
    ```

- **Windows**:
  - Download Python from [python.org](https://www.python.org/downloads/).
  - During installation, **check the box "Add Python to PATH"**.

### 2. Set Up a Virtual Environment

A virtual environment isolates your project’s dependencies from other Python projects on your system.

1. **Create a Virtual Environment**:
   - Run this command in the terminal/command prompt to create an isolated environment:
     ```bash
     python -m venv env
     ```
2. **Activate the Virtual Environment**:
   - **Mac**:
     ```bash
     source env/bin/activate
     ```
   - **Windows**:
     ```bash
     .\env\Scripts\activate
     ```

3. **Install Required Libraries**:
   - Once the environment is activated, install the necessary Python libraries:
     ```bash
     pip install requests pandas python-dotenv
     ```

### 3. Configure the Ahrefs API Key

1. **Obtain an Ahrefs API Key**:
   - Sign up for Ahrefs and obtain an API key.

2. **Set Up the `.env` File**:
   - Create a file called `.env` in the same folder as the script and add the following line:
     ```plaintext
     AHREFS_API_KEY=your_ahrefs_api_key
     ```
   - Replace `your_ahrefs_api_key` with the actual API key you obtained from Ahrefs.

### 4. Running the Script

1. **Add URLs**:
   - Open the `keyword_mapping_script.py` file in any text editor.
   - Modify the `urls` list to include the URLs or domains you want to analyze.

2. **Run the Script**:
   - In Terminal (Mac) or Command Prompt (Windows), navigate to the folder where the script is saved:
     ```bash
     python keyword_mapping_script.py
     ```

3. **Check the Results**:
   - The script will create a file named `url_keyword_mapping.csv` containing the best keywords for each URL.
   - You can open this file in Excel or any spreadsheet application.

### 5. Deactivate the Virtual Environment (Optional)

***If you want to stop using the virtual environment after running the script, deactivate it by typing***:
    ```bash
    deactivate

## Customizing for Different Domains
1. **Open the keyword_mapping_script.py file.**
2. **Edit the urls list to include the new URLs/domains you want to analyze.**
3. **Save and re-run the script using the instructions above.**

## Output
**The script generates a CSV file (url_keyword_mapping.csv) with the best keywords for each URL based on volume, difficulty, and relevance.**