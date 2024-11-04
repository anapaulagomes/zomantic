# zomantic
From Zotero to Semantic Scholar library

## Usage

To use the functionality of fetching items from Zotero added in the current week and generating a list of recommendations from Semantic Scholar, follow the steps below:

1. Clone the repository:
    ```sh
    git clone https://github.com/anapaulagomes/zomantic.git
    cd zomantic
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project and add your Zotero API key, Zotero user ID, and Semantic Scholar API key:
    ```sh
    ZOTERO_API_KEY=your_zotero_api_key
    ZOTERO_USER_ID=your_zotero_user_id
    SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key
    ```

4. Run the script:
    ```sh
    python main.py
    ```

5. The script will print the list of recommendations based on the items added to Zotero in the current week.
