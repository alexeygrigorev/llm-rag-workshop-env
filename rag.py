from elasticsearch import Elasticsearch
from openai import OpenAI

es_client = Elasticsearch(hosts=['http://localhost:9200'])
openai_client = OpenAI()


index_name = "course-questions"



def retrieve(query):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "data-engineering-zoomcamp"
                    }
                }
            }
        }
    }
    response = es_client.search(index=index_name, body=search_query)

    relevant_docs = []
    for hit in response['hits']['hits']:
        doc = hit['_source']
        relevant_docs.append(doc)

    return relevant_docs

prompt_template = """
You're a course teaching assistant. You need to answer a QUESTION from students based on
the provided CONTEXT. If the provided CONTEXT doesn't contain the answer, say "I don't know"

QUESTION: {query}

CONTEXT:

{context}
""".strip()

context_template = """
section: {section}
question: {question}
answer: {text}
""".strip()

def build_prompt(query, context_documents):
    context = ""

    for doc in context_documents:
        context_piece = context_template.format(**doc)
        context = context + '\n\n' + context_piece
    
    context = context.strip()

    prompt = prompt_template.format(query=query, context=context)

    return prompt

def llm(prompt):
    oai_response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    
    return oai_response.choices[0].message.content

def rag(query):
    context_documents = retrieve(query)
    prompt = build_prompt(query, context_documents)
    response = llm(prompt)
    return response