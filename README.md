![UFC Streaks](https://github.com/austinlackey/ufc/blob/main/Medium/UFC%208.png)
# Visualizing UFC Streaks
This project visualizes the streaks of the UFC fighters with the most wins in the history of the organization. This project utilized a full-stack approach from data scraping/collection to manipulation and visualization. The data was collected from two different sources, then merged and cleaned using Python. The data was then visualized using Tableau and Adobe Illustrator/Photoshop for eye-catching elements.

### Technologies
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Adobe Photoshop](https://img.shields.io/badge/adobe%20photoshop-%2331A8FF.svg?style=for-the-badge&logo=adobe%20photoshop&logoColor=white)
![Adobe Illustrator](https://img.shields.io/badge/adobe%20illustrator-%23FF9A00.svg?style=for-the-badge&logo=adobe%20illustrator&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)


# Motivation
One of the most interesting aspects of the UFC is the streaks that fighters go on. Whether it be a winning streak or a losing streak, these streaks can define a fighter's career. To visualize these streaks, we need data. However, data that is easily accessible is never up-to-date, accurate, or complete. API endpoints aren't always available, and often requires a subscription. My goal was to intelligently scrape data from multiple online sources, merge them, and visualize the data in a way that is both informative and visually appealing.

# :sparkles: Innovative Emphasis
**I designed this project to be a full-stack project that provides an efficient workflow while underscoring value. Data for this project is easily updated and maintained, with the run of a single Python script. We can intelligently compare local data with online additions, and only collect new data. Data can then be automatically cleaned and merged, and connected to Tableau for visualization. There is no need for manual updates.**

# Methodology
My methodology for this project is explained in detail in the following
[Medium article](https://medium.com/@austin-lackey/unveiling-dominance-a-data-science-journey-into-ufc-fighter-streaks-scraping-manipulating-and-78dd5402e9ae)

# Data Collected

## Fighter Information
- **URL**
- **Division**
- **Nickname**
- **Name**
- **Wins**
- **Losses**
- **Draws**
- **Status**
- **Place of Birth**
- **Age**
- **Height**
- **Weight**
- **Octagon Debut**
- **Significant Strikes Landed**
- **Significant Strikes Attempted**
- **Significant Strikes Landed Per Minute**
- **Significant Strikes Absorbed Per Minute**
- **Takedown Average Per 15 Minutes**
- **Submission Average Per 15 Minutes**
- **Significant Strike Defense**
- **Takedown Defense**
- **Knockdown Average Per 15 Minutes**
- **Average Fight Time**
- **Standing**
- **Clinch**
- **Ground**
- **Head**
- **Body**
- **Leg**
- **Knockout/Technical Knockout**
- **Decision**
- **Submission**
- **Has Image**
- **Dana White's Contender Series**
- **Takedowns Landed**
- **Takedowns Attempted**
- **Fighting Style**
- **Reach**
- **Trains at**

## Event Information
- **Event**
- **Date**
- **Location**
- **Fight**
- **Fighter A**
- **Fighter B**
- **Bout**
- **Method**
- **Round**
- **Time**
- **Format**
- **Referee**
- **Details**
- **Winner**
- **Winner Name**
- **Event Link**

## Fight Statistics
- **Event**
- **Fight**
- **Round**
- **Fighter**
- **Knockdowns**
- **Significant Strikes**
- **Significant Strikes Percentage**
- **Total Strikes**
- **Takedowns**
- **Takedown Percentage**
- **Submission Attempts**
- **Reversals**
- **Control**
- **Head**
- **Body**
- **Leg**
- **Distance**
- **Clinch**
- **Ground**

> [!NOTE]
> Fighter images are also collected, but are not included in this repository due to size constraints.

# Files

* `main_v2.py` - The main Python script that scrapes online data. Functions allow for fine-tuning of data collection, what data to collect, and how to collect it.
* `clean.py` - The Python script that merges and cleans the data. Reads data from the `Raw Data` folder, and outputs in the `Clean Data` folder.
* `test_deletion.py` - A Python script that deletes certain fights/events from the data. This is useful for testing the update functionality.
* `colors.py` - Python class for color-coding text in command line.
* `All other files` - These are the files that are used for ad-hoc analysis, and are not necessary for the main project.