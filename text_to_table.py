import re
import pandas as pd
import pyperclip

# Content provided
content = """
content
"""

# Split the content into tasks
tasks = re.split(r'\n(?=\d{2}:\d{2}〜)', content)

# Filter out tasks that don't contain a time range
tasks = [task for task in tasks if '〜' in task]

# Define a function to extract the details from each task
def extract_details(task):
    # Split the task into lines
    lines = task.strip().split('\n')
    
    # Get the start and end times
    start_time, end_time = lines[0].split('〜')
    
    # Get the status
    status = lines[1].strip()
    
    # Get the Ver and task name
    ver_line = lines[2]
    ver_match = re.search(r'V[\d\.-]+', ver_line)
    ver = ver_match.group().replace('V', '') if ver_match else 'N/A'
    task_name = ver_line.replace('V' + ver, '').strip()

    # Get the detail
    detail_line = lines[3] if len(lines) > 3 else ""
    detail = detail_line.split('→', 1)[-1].strip() if '→' in detail_line else ''

    return start_time, end_time, status, ver, task_name, detail

# Apply the function to each task
task_details = [extract_details(task) for task in tasks]

# Create a DataFrame
df = pd.DataFrame(task_details, columns=['開始時間', '終了時間', 'ステータス', 'Ver', 'タスク名', '詳細'])

# Copy the DataFrame to clipboard as TSV
pyperclip.copy(df.to_csv(index=False, sep='\t'))
