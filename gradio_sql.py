import gradio as gr
import sqlite3
import pandas as pd

# Create a sample database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary REAL
    )
''')
cursor.executemany('INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)',
                   [('John Doe', 'IT', 75000),
                    ('Jane Smith', 'HR', 65000),
                    ('Mike Johnson', 'Sales', 80000),
                    ('Emily Brown', 'Marketing', 70000)])
conn.commit()

def execute_sql(query):
    try:
        with sqlite3.connect(':memory:') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    department TEXT,
                    salary REAL
                )
            ''')
            cursor.executemany('INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)',
                               [('John Doe', 'IT', 75000),
                                ('Jane Smith', 'HR', 65000),
                                ('Mike Johnson', 'Sales', 80000),
                                ('Emily Brown', 'Marketing', 70000)])
            conn.commit()
            df = pd.read_sql_query(query, conn)
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
    inputs=gr.Textbox(lines=5, label="SQL Query", placeholder="Enter your SQL query here..."),
    outputs=gr.Dataframe(label="Query Result"),
    title="SQL Query Interface",
    description="Enter a SQL query to retrieve data from the sample database.",
    theme="soft",
    examples=[
        ["SELECT * FROM employees"],
        ["SELECT name, salary FROM employees WHERE department = 'IT'"],
        ["SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department"]
    ]
)

if __name__ == "__main__":
    iface.launch()