# To Code or Not to Code

* **Online URL**: https://share.streamlit.io/cmu-ids-2022/final-project-zebra/main/StackOverFlow.py
* **Team members**:
  * [Nate](mailto:ndf@andrew.cmu.edu)
  * [Naman](mailto:namana@andrew.cmu.edu)
  * [Ruhi](mailto:ruhihemp@andrew.cmu.edu)
  * [Somya](mailto:somyaa@andrew.cmu.edu)


## Summary  

The project is centered around exploring the insights collected from the [Stack Overflow 2020 Developer Survey](https://insights.stackoverflow.com/survey/2020). We performed heavy data cleaning to bring the data into a workable format. Our vision throughout was to give the user maximum flexibility to freely understand and explore the data. Since a lot of users in the survey also shared Salary information, we attempted to build a regression model to predict the salary that a candidate can expect to earn given a certain set of parameters.  

The target audience for the application is anybody who is interesting in a career that involves writing code, or somebody who is already in the field but looking to explore how the industry has evolved, and where it is headed. The insights can be used to influence decisions about which skill to learn next, and which area is best suited for investing one's time in, so that output can be maximized. 

## Homepage 
Below is a screenshot of the homepage of the application:  

![homepage](assets/zebra-homepage.png)

## Setup
The app can be directly accessed from the hyperlink available above. If needed to run locally, you can do so by cloning the repository on your system and then within the directory use the following command: 
```
streamlit run StackOverFlow.py
```

## Work distribution

All of our work was fairly equally distributed. We worked on the cleaning process in collaboration, and used DeepNote to work together and collaborate on a live shared Python notebook. Each team member had roughly the same contribution to the cleaning process, which was a huge task in itself because the data was extremly dirty.  

After cleaning, we decided to realise the ideas we had conceptualized during the sketching phase. Nate worked on the "Measure Success" and the "Demographics Explorer" dashboards. Naman worked towards further cleaning of the data and later used it to train the Random Forest regressor for salary prediction. Ruhi came with the novel idea of explorng how habits affect other quanitifiable parameters and worked on it in entirety. Somya handled the Job Satisfaction prediciton and Today to Tomorrow dashboards. 



