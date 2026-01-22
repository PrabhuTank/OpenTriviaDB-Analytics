# Seamless API interactions
import requests
# Interacting with MongoDB databases
import mysql.connector as myCon
# Data manipulation and transformation
import pandas as pd
# Shuffling the order of items randomly
import random

def extract_data():
    # Extracting data from the API  
    results = requests.get("https://opentdb.com/api.php?amount=50")
    # Extracting the data for movies in JSON format
    results = results.json()
    raw_data = results.get("results", [])
    
    return raw_data

def transform_data(raw_data):
    # Defining the dataframe to store the relevant data
    df_questions = pd.DataFrame()
    
    # Fetching the items
    for item in raw_data:
        ## Gathering all answers to string list
        list_answers = [str(x) for x in item.get("incorrect_answers", [])]
        list_answers.append(item.get("correct_answer", ""))
        ## Shuffling the order of answers
        random.shuffle(list_answers)
        ## Getting the rows number
        nb_rows = len(list_answers)
        
        ## Storing all relevant data into stagia dataframe
        df_stagia = pd.DataFrame({
            'type': [item.get("type", "")] * nb_rows,
            'difficulty': [str(item.get("difficulty")).capitalize()] * nb_rows,
            'category': [item.get("category", "")] * nb_rows,
            'question': [item.get("question", "")] * nb_rows,
            'answer': list_answers,
            'correct': ["No"] * nb_rows
        })
       
        ## Defining the correct answer 
        df_stagia["correct"] = df_stagia.apply(
            lambda x: "Yes" if x["answer"] == item.get("correct_answer", "") else x["correct"], axis=1
            )
        
        ## Merging new records with the existing ones
        df_questions = pd.concat([df_questions, df_stagia], axis=0, ignore_index=True)
    
    # Dropping the duplicates
    df_questions = df_questions.drop_duplicates()
    
    return df_questions

def load_data(df_questions):
    # Setting up a connection to the database
    conn = myCon.Connect(
        host="localhost",
        user="root",
        password="admin",
        database="triviadb"
        )
    
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    
    # Extracting the table named "categories"  
    cursor.execute("select * from Categories")
    df_categories = pd.DataFrame(cursor.fetchall(), columns=["ID_category","Category_name"])
    
    # Extracting the table named "types"  
    cursor.execute("select * from Types")
    df_types = pd.DataFrame(cursor.fetchall(), columns=["ID_type","Type_name","Type_slug"])
    
    # Extracting the table named "levels"  
    cursor.execute("select * from Levels")
    df_levels = pd.DataFrame(cursor.fetchall(), columns=["ID_level","Level_name"])
    
    # Normalizing the data
    ## Merging with others tables
    df_questions = pd.merge(df_questions, df_categories, left_on = "category", right_on="Category_name")
    df_questions = pd.merge(df_questions, df_types, left_on = "type", right_on="Type_slug")
    df_questions = pd.merge(df_questions, df_levels, left_on = "difficulty", right_on="Level_name")
    ## Keeping only the main columns
    df_questions = df_questions[['question', 'answer', 'correct','ID_type','ID_level','ID_category']]
    
    # Preparing the list of questions
    questions = df_questions["question"].drop_duplicates().reset_index()
    questions = questions["question"]
    
    # Fetching the questions
    for question in questions:
        ## Converting the question into string type
        question_text = str(question)
        
        ## Checking if the question exists(Updating)
        cursor.execute("select * from Questions where Question_text = %s", (question,))
        res = cursor.fetchone()
        ### if exists
        if res is not None: 
            ### Removing the question along with all associated data
            ### for objective to insert the question and the news answers.
            cursor.execute("delete from Questions where Question_text = %s", (question,))
            conn.commit()
        
        ## Filtering the data for the current question
        question_stagia = df_questions[df_questions['question'] == question]
        question_stagia = question_stagia.reset_index()
        
        ## Preparing the columns as foreign keys
        ID_type = int(question_stagia["ID_type"].iloc[0])
        ID_level = int(question_stagia["ID_level"].iloc[0])
        ID_category = int(question_stagia["ID_category"].iloc[0])
        
        ## Inserting the question data
        cursor.execute("insert into Questions(Question_text, ID_type, ID_level, ID_category)values(%s,%s,%s,%s)", 
                      (question_text, ID_type, ID_level, ID_category,))
        
        ## Getting the ID for the last inserted question
        ID_question = cursor.lastrowid
        
        ## Fetching answers
        for i in range(0, len(question_stagia)):
            ### Getting the answer text
            answer_sentence = question_stagia["answer"].iloc[i]
            ### Getting the answer status
            correct = question_stagia["correct"].iloc[i]
            
            ### Inserting the answer
            cursor.execute("insert into Answers(Answer_sentence, Correct, ID_question)values(%s,%s,%s)", 
                          (answer_sentence, correct, ID_question,))
    
    # Save changes to the database           
    conn.commit()
    # Close the cursor
    cursor.close()
    # Close the connection
    conn.close()