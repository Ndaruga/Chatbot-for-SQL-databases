# Build-a-Chatbot-for-an-SQL-database-with-Streamlit-and-Vanna
Building a chatbot for an SQL database with Streamlit and Vanna is a fun and easy way to interact with your Database using natural language


https://github.com/Ndaruga/Build-a-Chatbot-for-an-SQL-database-with-Streamlit-and-Vanna/assets/68260816/d5726d65-bcc7-4376-bece-026bdcc52708


**See [Project Link Here](https://sql-database-chat-bot.streamlit.app/)**

---

## Local Execution
Streamlit is a Python library that allows you to create interactive Python web applications with minimal code. Vanna is a Python package that uses AI to generate SQL queries from natural language questions. 

Together, they can help to build a chatbot for your SQL database with the following steps.
  1. Clone the repository
  2. Install all requirements using
    ```
     pip install -r requirements.txt
    ```
  3. Get a **Vanna API key** from [here](https://vanna.ai/)
  4. For testing purposes, replace the `vanna_api_key` variable in line 13 of the `app.py` with the **vanna api key**.
      > However, during deployment, ensure you get rid of the new line since pushing sensitive data to GitHub or deployment platforms is not recommended.

  5. Run the code below to execute
     ```
      streamlit run app.py
      ```
  6. Deploy your app to Streamlit Cloud or your preferred platform
