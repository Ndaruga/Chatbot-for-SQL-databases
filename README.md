# Build-a-Chatbot-for-an-SQL-database-with-Streamlit-and-Vanna
Building a chatbot for an SQL database with Streamlit and Vanna is a fun and easy way to interact with your data using natural language


https://github.com/Ndaruga/Build-a-Chatbot-for-an-SQL-database-with-Streamlit-and-Vanna/assets/68260816/d5726d65-bcc7-4376-bece-026bdcc52708


**See [Project Link Here](https://sql-database-chat-bot.streamlit.app/)**

---

## Local Execution
Streamlit is a Python library that allows you to create interactive Python web applications with minimal code. Vanna is a Python package that uses AI to generate SQL queries from natural language questions. 

Together, they can help to build a chatbot for your SQL database.

### To build a chatbot for your SQL database with Streamlit and Vanna, you will need to:
- Clone the repository
- Install Streamlit and Vanna using
  ```
  pip install streamlit vanna
  ```
- Get a **Vanna API key** from [here](https://vanna.ai/)
- For testing purposes, comment line 4 of the `sql-chat.py` with the following code `vn.set_api_key(st.secrets["vanna_api_key"])` and replace it with
  ```
  vn.set_api_key(<api key here>)
  ```
  However, during deployment, ensure you get rid of the new line since pushing sensitive data to GitHub or deployment platforms is not recommended.

- Run the code below to execute
 ```
  streamlit run app.py
  ```
- Deploy your app to Streamlit Cloud or your preferred platform
