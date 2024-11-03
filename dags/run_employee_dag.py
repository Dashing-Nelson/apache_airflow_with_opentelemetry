from airflow import DAG
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from tracing import tracer
from airflow.hooks.base_hook import BaseHook
from sqlalchemy import create_engine
import pandas as pd

def transform_data(**kwargs):
    with tracer.start_as_current_span("transform_data"):
        # Database connection
        conn = BaseHook.get_connection('my_mysql_conn')
        engine = create_engine(f'mysql+pymysql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')

        # Extract data
        with tracer.start_as_current_span("extract_data"):
            with tracer.start_as_current_span("getting_employees"):
                employees_df = pd.read_sql("SELECT emp_no, first_name, last_name FROM employees", engine)
            with tracer.start_as_current_span("getting_salaries"):    
                salaries_df = pd.read_sql("SELECT emp_no, salary, from_date, to_date FROM salaries", engine)
            with tracer.start_as_current_span("getting_departments"):
                departments_df = pd.read_sql("""
                    SELECT de.emp_no, d.dept_name
                    FROM dept_emp de
                    JOIN departments d ON de.dept_no = d.dept_no
                """, engine)

        # Transform data
        with tracer.start_as_current_span("merge_data"):
            # Merge DataFrames
            with tracer.start_as_current_span("employees_df.merge"):
                merged_df = employees_df.merge(salaries_df, on='emp_no')
            with tracer.start_as_current_span("merged_df.merge"):
                merged_df = merged_df.merge(departments_df, on='emp_no')

        with tracer.start_as_current_span("calculate_salary_growth"):
            # Sort by emp_no and from_date
            with tracer.start_as_current_span("merged_df.sort_values"):
                merged_df.sort_values(by=['emp_no', 'from_date'], inplace=True)
            # Calculate salary growth
            with tracer.start_as_current_span("calculate-salary-growth"):
                merged_df['salary_growth'] = merged_df.groupby('emp_no')['salary'].pct_change()
            # Handle NaN values resulting from pct_change
            with tracer.start_as_current_span("handle_NaN_values_resulting_from_pct_change"):
                merged_df['salary_growth'].fillna(0, inplace=True)

        with tracer.start_as_current_span("aggregate_data"):
            # Calculate average salary growth per department
            with tracer.start_as_current_span("merged_df.groupby"):
                avg_growth_df = merged_df.groupby('dept_name')['salary_growth'].mean().reset_index()
            with tracer.start_as_current_span("avg_growth_df.rename"):
                avg_growth_df.rename(columns={'salary_growth': 'avg_salary_growth'}, inplace=True)

        # Load data
        with tracer.start_as_current_span("load_data"):
            with tracer.start_as_current_span("load_data_sql"):
            # Option 1: Save to a new MySQL table
               avg_growth_df.to_sql('avg_salary_growth_per_dept', con=engine, if_exists='replace', index=False)
            with tracer.start_as_current_span("load_data_csv"):
            # Option 2: Export to CSV
                avg_growth_df.to_csv('avg_salary_growth_per_dept.csv', index=False)

default_args = {
    'owner': 'airflow',
}

with DAG('etl_pipeline', default_args=default_args, catchup=False, schedule_interval=None) as dag:

    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        dag=dag
    )

    transform