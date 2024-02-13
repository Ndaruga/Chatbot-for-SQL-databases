# Build-a-Chatbot-for-an-SQL-database-with-Streamlit-and-Vanna
Building a chatbot for an SQL database with Streamlit and Vanna is a fun and easy way to interact with your data using natural language
Here is a demo of the project.

Getting started

The project is live here.
Streamlit is a Python library that allows you to create interactive web applications with minimal code. 

Vanna is a Python package that uses AI to generate SQL queries from natural language questions. Together, they can help you build a chatbot for your SQL database in a few steps.

To build a chatbot for your SQL database with Streamlit and Vanna, you will need to:

- Install Streamlit and Vanna using `pip install streamlit vanna`
- Get a Vanna API key from [here](^1^) and store it in a file called `.streamlit/secrets.toml`
- Set the Vanna model and connect to your SQL database using `vn.set_model` and `vn.connect_to_sqlite` or `vn.connect_to_snowflake`
- Create a Streamlit app that takes a user question as input and displays the generated SQL, the query results, and a chart using `st.text_input`, `vn.generate_sql`, `vn.run_sql`, and `vn.get_plotly_figure`
- Deploy your app to Streamlit Cloud or your preferred platform
