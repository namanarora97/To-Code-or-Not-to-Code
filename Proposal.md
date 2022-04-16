# Final Project Proposal

[GitHub Repo URL](https://github.com/CMU-IDS-2022/final-project-zebra)

# Team Zebra Final Project Proposal

## Team Members
Naman Arora, Somya Agarwal, Ruhi Patel, Nate Fairbank  
## Dataset
We selected the results from the 2018 Stack Overflow Developer Survey. This questionnaire had over 100,000 respondents who reported information ranging from their exercise habits to compensation levels. The strengths of this data are that it broad and fairly standardized, and that some rudimentary cleaning of the data was done for the public release. The downsides are that results of a mass-solicited, self-reported survey may not be reliable, and may suffer from massive selection bias in terms of who saw and was willing to fill out the survey. Additionally, 100,000 entries may not be large enough to permit any complicated machine learning, and the data may become unreliably sparse once filtered for specific feature values.  
## Data URL
[Kaggle](https://www.kaggle.com/stackoverflow/stack-overflow-2018-developer-survey?select=survey_results_public.csv)

## The question
 “What makes a programmer successful?" This question is intentionally broad, to allow the user to project their own perception and line of inquiry onto it, prompting them to explore the data. For example, the pragmatic (and financially motived) reader might be interested in the answer to the sub-question “what computer language should I learn to make the most money?" Another, more socially-oriented user might wonder “do white men stay in the field of computer science longer than minorities or women?" A third viewer might be curious about what undergraduate majors generate the highest career satisfaction. All three users have, in a way, asked “what makes a programmer successful”, with different means of generating success, and different definitions of success itself. 

## Further comments 
It seems that a user-driver “Interactive Visualization/ Application Track” is best-suited to addressing this question. Our application would briefly explain the data and ask the question, perhaps with some initial suggestions for exploration, drawing the user in and allowing them to explore the data along their own path. However, if we find a series of compelling relationships a narrative track might allow us to better direct the user towards these key insights.

## Next steps:
### Sketching: 
each of us will make 3x initial sketches of questions we would like to try to answer. We should have the data schema in front of us while sketching, but not the actual data. We can then compare the 12 resulting sketches as a group, pick the best ones, refine them.
### Data exploration: 
we will then use Tableau to do initial exploration of the features we are interested in, checking for interesting relationships between features, feature values and summary statistics, and compelling visualizations. 
### Sketching round 2: 
This round of sketching will focus on tying together the areas of exploration that we feel are most promising based on the data exploration. How will the user navigate through the data? What interactivity will occur between graphs?  

This takes us through the initial design phase of the project. Once we have sketched individual visualizations, explored the data, and sketched a way to link together the individual visualizations we will be better able to plan the actual development of the product. 


# Data Analysis
We are using DeepNote (Pandas), Tableau and Trifacta for collaboratively working on data analysis.  

The dataset is quite rich and in good shape. Since the data is collected using surveys, there are certainly some nulls which we would consider dropping. 


![SfinA4GDVH](https://user-images.githubusercontent.com/85018020/163656786-22657ceb-b654-4e95-aaaf-5c84b82a71b5.png)
![aBhZPFzFw5](https://user-images.githubusercontent.com/85018020/163656950-6ce2c0b7-2164-47ed-943e-e48337b15894.png)

We have a large amount of data with 129 features available. We can drill down into each and choose what make the msot sense going forward. We have explored a subset of these in our sketches and initial EDA process.  

![msedge_s8G6E8LMMB](https://user-images.githubusercontent.com/85018020/163657100-7e21a139-9349-4e9c-bd88-0a0bbfafa3da.gif)


# Sketches

![bFOtfENE32](https://user-images.githubusercontent.com/85018020/163656549-f5b7f769-4704-4cf7-b608-05004a6810cb.png)

So the user gets asked "do you want to be a rich coder or a happy coder". Let's pretend they say "rich"- if they say "happy" then career satisfaction and "money" in the below description will be reversed.  
 Income is on the y-axis, and the x-axis is a category that the user selects from a list. It starts out as a histogram but could be any of the list I have there (or something else). So they can, for instance, say "what programming language makes the most money". But the cool thing is then they can click a bar on the chart, and on a separate 1-D chart it shows the career satisfaction of people in that category. So for instance you might see that Java programmers make more money than python programmers, but when you click their bars you see that Python programmers are happier.
 
 ![LBS3XpzT2l](https://user-images.githubusercontent.com/85018020/163656579-5dc2e0fd-43ab-43c8-8357-1651ae3e0b7d.png)

This chart shows how participation in a coding community affects success. I had envisioned career satisfaction and length being encoded on the vertical and horizontal axis, but I suppose other metrics of success such as salary could also be displayed (perhaps as a toggle).  
Each person would be plotted as a point on the graph, with a color encoding indicating the count of community-oriented activities (the size encoding shown above would not be effective). Tooltips would allow the user to show the specific activities that someone participated in. A cool interactivity would be to allow the user to select by area some subset of the population (or by activity count) and then display some extra information, such as the average salary of the selected population.  

## Programming languages used by those developers:-
![kD2H6yBKmm](https://user-images.githubusercontent.com/85018020/163656612-43c162f1-c8dd-4f6d-9795-13e2a6ccec3a.png)


## Education level of these developers:-

![W3JRtxGV4x](https://user-images.githubusercontent.com/85018020/163656639-2b6aae15-26c4-4c8e-ad4c-2ab90a24222c.png)

## The country these developers belong to:-
(Most satisfied developers reported are from the United States)

![UoHFDTaXZh](https://user-images.githubusercontent.com/85018020/163656659-da0df26a-00a3-49b2-8b99-60571024e18d.png)


## Demographics: 

We plan to show the distribution on age,race,gender,location on x axis and y axis will be income distribution. We also plan to have a bar to demonstrate career satisfaction or job satisfaction . So it can be interpreted as who makes the more money and how satisfied they are with their jobs. The demographics info can go in the dropdown  
![Ul5i4pAuW7](https://user-images.githubusercontent.com/85018020/163656676-79f5225f-b82f-425d-9973-68e4b80d19b7.png)


## Personal Habits:
Exploring columns like exercise,skipMeal, wakeTime, Computer hours. The idea is to show that necessarily not skipping meals, or not doing exercise would make you earn more/ or make you more satisfied or something.  

![uTlgQOshPK](https://user-images.githubusercontent.com/85018020/163656700-7ced37db-144a-4cbc-9feb-e15c2902ddaf.png)

## What can you expect to earn? How do you rank?
The expected earnings of an individual can be derived from a regression model. We can also add explanability elements to visualization that shows just how much factor provided by the user has influenced the salary number that we have predicted. 

![f1LoBV1d07](https://user-images.githubusercontent.com/85018020/163656714-096a6ef9-3d60-4713-96a2-7a32da2f2969.png)




