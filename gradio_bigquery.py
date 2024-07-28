import gradio as gr
from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
client = bigquery.Client()

def execute_sql(query):
    try:
        query_job = client.query(query)
        results = query_job.result()
        df = results.to_dataframe()
        return df
    except Exception as e:
        return str(e)

def sql_interface(query):
    result = execute_sql(query)
    if isinstance(result, pd.DataFrame):
        return result
    else:
        return f"Error: {result}"

iface = gr.Interface(
    fn=sql_interface,
    inputs=gr.Textbox(lines=5, label="SQL Query", placeholder="Enter your BigQuery SQL query here..."),
    outputs=gr.Dataframe(label="Query Result"),
    title="BigQuery SQL Interface",
    description="Enter a SQL query to retrieve data from your BigQuery dataset.",
    theme="soft",
    examples=[
        ["SELECT * FROM `your_project.your_dataset.your_table` LIMIT 10"],
        ["SELECT column1, column2 FROM `your_project.your_dataset.your_table` WHERE condition = 'value'"],
        ["SELECT column, COUNT(*) as count FROM `your_project.your_dataset.your_table` GROUP BY column"]
    ]
)

if __name__ == "__main__":
    iface.launch()