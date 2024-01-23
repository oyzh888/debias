import json
import os
import time
from multiprocessing import Pool

import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from debias.consts import (DATA_PATH, EXPORT_METRIC_CSV_PATH, OPENAI_WORKSPACE,
                           TEST_CSV_PATH)

sys_prompt = '''As a professional music expert, you are tasked with employing the A-vs-B approach for GPT to conduct a multi-dimensional comparative analysis. 

# The evaluation should encompass the following aspects:
- Accuracy: This measures the overall alignment of the response with the expected answer, expressed as a percentage.
- Keywords Matching: This evaluates the degree to which the response aligns with the key terms or phrases specified.
- Reason: Provide a concise justification, in no more than 10 words, for the assessment of the response as good or bad. These reasons, collected from 6000 results, will be used to generate a comprehensive summary of the model's performance.
- Human Likability
    Creativity
    Relevance
    Coherence
    Emotional Resonance
    Cultural Appropriateness

# Your response should be formatted in JSON as follows:
{{
  "Accuracy": 0.7,
  "Keywords Matching": 0.8,
  "Music Metrics": {{
    "Human Likability": 0.8,
    "Creativity": 0.6,
    "Relevance": 0.7,
    "Coherence": 0.8,
    "Emotional Resonance": 0.9,
    "Cultural Appropriateness": 0.7
  }}
  "Reason": "This is a good reason"
}}

# Context:
Groudtruth: {groud_truth}
Prediction: {prediction}

'''


def section_law_classify(groud_truth, prediction):
    llm = ChatOpenAI(
        # model_name="gpt-3.5-turbo-1106",
        model_name="gpt-4-1106-preview",
        temperature=0.0,
        request_timeout=300.0,
    ).bind(response_format={"type": "json_object"})

    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_prompt),
        # ("user", "{input}")
    ])

    chain = prompt | llm

    s_t = time.time()
    res = chain.invoke({"groud_truth": groud_truth, "prediction":prediction}).content
    print(res)
    print(time.time() - s_t)
    return res

def classify_and_cache(groud_truth, prediction, index):
    cache_folder = OPENAI_WORKSPACE
    os.makedirs(cache_folder, exist_ok=True)
    cache_file = os.path.join(cache_folder, f'{index}.json')

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    try:
        result = section_law_classify(groud_truth, prediction)
        with open(cache_file, 'w') as f:
            json.dump(result, f)
        return result
    except Exception as e:
        print(f"Failed to process section at index {index}: {e}")

def process_csv_row(index_row):
    index, row = index_row  # Unpacking the tuple
    return classify_and_cache(row['GroudTruth'], row['Prediction'], index)

def process_all_rows(df):
    with Pool(4) as pool:
        results = pool.map(process_csv_row, df.iterrows())  # Use map instead of starmap

    # iter rows
    # results = []
    # for index, row in df.iterrows():
    #     res = classify_and_cache(row['GroudTruth'], row['Prediction'], index)
    #     results.append(str(res))
    
    return results

if __name__ == '__main__':
    df = pd.read_csv(TEST_CSV_PATH)
    results = process_all_rows(df)


    # Create a dictionary from results to add as a new column
    # results_dict = {index: result for index, result in results}
    df['result'] = results
    # Export the updated DataFrame to a new CSV file
    new_csv_path = EXPORT_METRIC_CSV_PATH
    df.to_csv(new_csv_path, index=False)
    print(f"Results exported to {new_csv_path}")