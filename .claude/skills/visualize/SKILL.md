---
name: visualize
description: Visualizes data stored in the ".claude/skills/migrate/data/" directory and generates visualizations based on that data. Use this skill when you want to create visual representations of your data for better insights and analysis.
--- 

## Usage

### Step-1: Pick the python environment
Before you start, make sure to pick the python environment in which you want to run the code. You can run/install dependencies using my '.venv' environment which is located at "C:\Users\roger\Desktop\Claude Code\Claude_Code_Demo\.venv".

### Step-2: Use Pandas to build KPIs
You need to use the Pandas library to build KPIs based on the data stored in the ".claude/skills/migrate/data/" directory. This involves loading the data into a Pandas DataFrame, performing necessary data manipulation and calculations to derive key performance indicators (KPIs defined below) that are relevant to your analysis.
After reading the data, you need to build the following KPIs:
    1. total sales
    2. total returns
    3. net sales
    4. average sales per store
    5. average sales per product

### Step-3: Generate Visualizations
Once you have calculated the KPIs, you can use libraries like Matplotlib or Seaborn to create visualizations that represent these KPIs effectively. You can create bar charts, line graphs, or any other type of visualization that best suits the data and the insights you want to convey. Make sure to create a "visualization" folder under ".claude/skills/visualize/" and save these visualizations using plt.savefig() function in that directory for easy access and reference.


<!-- ### Step-2: Run the Python Script To Visualize Data & Generate Visualizations
You need to run the Python Script stored at ".claude/skills/visualize/scripts/visualize.py". This script will generate visualizations based on the data you have and save them in the appropriate directory. -->
