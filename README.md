# AI_term_project_Recommender

This project is for NTU course - Introduction to AI

As for food delivery app is becoming popular

We want ot develop a recommendation system

This system recommends meals that match user’s preference, reduce the time that might be used to browsing and making decision, enhance adherence rate and also bring additional value by helping user fit his/her diet plan. 

## Catogory

<a href='#Reminder'>Reminder</a>

<a href='#meeting_minutes'>MeetingMinutes</a>

<a href='#model'>Model</a>

<a href='#algorithm'>Algorithm</a>

<a href='#recommender'>Recommender</a>

---
## <p id=reminder>Reminder</p>

1. Json format data in '/data' directory will be auto load to db when run this project

2. Database migration have not introduced

---
## <p id=meeting_minutes>MeetingMinutes</p>

### 5/6

1. Add UserReview, FoodCategory

2. Do we need to Model "User Preference" ? -> Temporary Not

3. Make provide 'id' in json file can be auto loaded, if no id is provided, auto generate id

4. Please start to aad loading data to '/data' and write your algorithm

### 5/9

1. Write runable algorithm

2. Give some diet schedule

3. Write evaluation proxy

4. Make poster

5. reference

> Nutrition ratio of Simple Diet Schedule reference from America Council fo Health
> https://www.acefitness.org/education-and-resources/professional/expert-articles/5904/how-to-determine-macronutrient-needs-based-on-goals

---
## <p id=model>Model</p>

define data model which will be operated by app in run time

data source can be data collections in different format or data base, but all will be loaded to app in runtime

1. data loader : support different format data source, include food data and user related data

2. app context (not necessary) : we can load all data into app, but we can adopt lazy method, which search and load data when it's need

3. consider further possibility to integrate with ORM

---
## <p id=algorithm>Algorithm</p>

recommendation algorithms

1. Markov Process

2. CF (Collaborative Filtering)

3. CB (Content-Based Filtering)

4. CSP (Constraint Satisfaction Problem)

5. others

---
## <p id=recommender>Recommender</p>

1. A running server

2. manage all resource and run algorithm

3. provide interface to interact with user
