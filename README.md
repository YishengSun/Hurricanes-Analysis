
### The Data
For this assignment, you’ll need to download data from two completely
different data sources and then properly load and join data frames
(similar to SQL joins), as discussed in class.

* Download the 2018 edition of Lahman’s Baseball Database, in the Zipped
CSV format. It is available at
http://www.seanlahman.com/baseball-archive/statistics
The link and file you want from that page is described as 
"2018 - comma-delimited version" and the filename itself is v2019.2.zip. The 
database is documented at http://www.seanlahman.com/files/database/readme2017.txt

* Download the “National data” file from the US Social Security names
database at https://www.ssa.gov/oact/babynames/limits.html  This is also
a Zipped collection of CSV files.  Tip:  There are many examples in the
McKinney book that load and analyze these baby name files using Pandas.


### The Programming

Your final product should be a Jupyter Notebook that clearly documents 
and shows results of your work to analyze some of the following queries. Work 
in your team by dividing the work, trying independently, then doing
code review for each other and finally present the best-quality completed
work you can as a single notebook. 

**You must write at least two custom functions in the notebook or in a separate 
Python module that you import into the notebook.  Those functions need to be 
complete with Docstrings and Doctests, and properly use DataFrames as parameters 
and/or return values.**

### Tips for collaborating through Git:
1. If multiple people are simultaneously using the same notebook and you try 
committing, you will find that trying to do a "git merge" on a Jupyter 
Notebook is very difficult.  So you might want to each work on 
distinct notebook files to avoid merge conflicts and then combine 
the parts into the final notebook at the end.  

2. Try to remember to use git Update each time before you start to edit things, 
it'll reduce the need for merges.  

3. You don't need git _branches_ or _pull requests_ for this assignment. Avoid 
that complexity. 

4. If you're using PyCharm as your git client, I recommend using these options when updating:
![](Pycharm_git_update_dialog.png)

## For Baseball-specific analysis (__*do any 3 of these*__):

NOTE: You can ignore the Post-season data files for these analyses 
(e.g. "BattingPost.csv", "PitchingPost.csv", etc.). Just use the main 
regular-season files. 

* A) Think like an analyst exploring the question "Do baseball players with 
high batting averages consistently get paid more than others?"  Calculate the 
correlation between batting average and salary.  However, don't include 
pitchers in this since they are not hired for hitting ability. 
You can determine pitchers either from the Appearances or Pitching tables. 
(Join People, Appearances, and Batting tables).  To remove the disparities 
caused by historical growth of salaries, limit this to seasons from 
2000-onward.

* B) List the top 30 players in career success for stealing the most bases.  
Use total of “Stolen Bases” + total of “Caught Stealing” and call that result 
"Stealing Attempts". Also compute and show their base stealing success rate as 
a percentage of attempts.  In the results, show their name & the calculated 
numbers. (Join People and Batting tables)

* C) Calculate and plot a chart showing the mean (average) height of all
active players per year.  (The player must be listed in a team roster 
for the year to be “active”, so join People & Appearances)

* D) List the 20 most dangerous pitchers derived from their career total 
statistics.  Specifically, those with the highest career rates of hitting 
batters.  (Join People & Pitching tables.  Use the formula 
total “Batters Hit By Pitch” / total “Outs Pitched”)

* E) List the top schools by number of alumni who were _actually_ inducted into the
Hall of Fame. (Join Schools, CollegePlaying, HallOfFame)

## For cross-database integration analysis (__*do either 1 of these*__):

Notice that the People table has fields called "nameFirst", "nameLast", and 
"nameGiven".  For many of the players, the nameFirst column actually contains 
their _nickname_.  See Babe Ruth as an example, whose real first name was "George". 
Another is Cornelius Ryan who went by 'Connie'. So many of these nicknames are 
typically female that you have to extract their real first names (the 
"nameGiven" column) to do a sensible analytical comparison with the SSN database.

* List all player given names that are statistically higher frequency among
baseball players than among males in the general population _for their
year of birth_. Sort results by the proportion of commonality.

* Alphabetically list the full names of all players having real given names 
that were higher frequency for female babies _in the same year the player was born_.

Tips for these queries: Use the Baseball People table to extract player's 
real first names and dates of birth. Then properly join them with the 
“Baby Names” data matching their year of birth.  That's a multi-column join.
