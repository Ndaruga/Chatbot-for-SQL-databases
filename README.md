# Chatbot-for-SQL-databases
An SQL Chatbot powered by LLM for generating SQL queries and their graphical analysis using natural language questions.


For now, this application works well with **PostgreSQL** and I am working to make sure the other databases are also functional.

https://github.com/Ndaruga/Build-a-Chatbot-for-an-SQL-database-with-Streamlit-and-Vanna/assets/68260816/d5726d65-bcc7-4376-bece-026bdcc52708

**See [Project Link Here](https://chatbot-for-sql-databases.streamlit.app/)**



If you have a locally hosted database, use a tool like [ngrok](https://ngrok.com) on your terminal to expose it to the internet.

Your exposed host should look like this:

![image](https://github.com/Ndaruga/Chatbot-for-SQL-databases/assets/68260816/07874a8f-86a7-40f5-adbc-afb7a711aa3a)



Use the provided credentials to log in to your database as shown
![image](https://github.com/Ndaruga/Chatbot-for-SQL-databases/assets/68260816/54546284-e693-4e14-9b18-68462c824455)


---

**This app does not collect any user data or any other credentials.**


## Local Execution
To run this project locally, 
  1. Clone the repository
  2. Install all requirements using
    ```
     pip install -r requirements.txt
    ```
  3. Get a **Vanna API key** from [here](https://vanna.ai/)
  4. For testing purposes, replace the `vanna_api_key` variable in line 13 of the `app.py` with the **Vanna API key**.
      > However, during deployment, ensure you get rid of the new line since pushing sensitive data to GitHub or deployment platforms is not recommended.

  5. Run the code below to execute
     ```
      streamlit run app.py
      ```
  6. Deploy your app to Streamlit Cloud or your preferred platform
