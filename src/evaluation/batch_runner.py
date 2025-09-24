# src/evaluation/batch_runner.py

import argparse
import json
import os
import sys
import yaml

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.rag.rag_pipeline import create_rag_chain

def run_rag_pipeline(rag_chain, query):
    """
    Runs the RAG pipeline for a given query.
    """
    print(f"Running RAG pipeline for query: {query['text']}")
    response = rag_chain.invoke(query['text'])
    
    # The 'response' from the RAG chain is a dictionary containing the answer and context
    retrieved_docs = [doc.page_content for doc in response.get('context', [])]
    generated_answer = response.get('answer', "No answer generated.")
    
    return {
        "query_id": query["id"],
        "retrieved_docs": retrieved_docs,
        "generated_answer": generated_answer
    }

def main():
    """
    Main function to run the RAG pipeline over a batch of queries.
    """
    parser = argparse.ArgumentParser(description="Run the RAG pipeline over a batch of queries.")
    parser.add_argument("--config", type=str, default="configs/evaluation/default.yml", help="Path to the configuration file.")
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    queries_path = os.path.join(config['evaluation_data_dir'], config['queries_file'])
    output_path = os.path.join(config['results_dir'], config['batch_run_results_file'])

    # Create the RAG pipeline
    rag_chain = create_rag_chain(
        llm_provider_name=config['rag_pipeline']['llm_provider'],
        vector_store_type=config['rag_pipeline']['vector_store']
    )

    results = []
    with open(queries_path, "r") as f:
        for line in f:
            query = json.loads(line)
            result = run_rag_pipeline(rag_chain, query)
            results.append(result)

    os.makedirs(config['results_dir'], exist_ok=True)
    with open(output_path, "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")

    print(f"Successfully processed {len(results)} queries. Results saved to {output_path}")

if __name__ == "__main__":
    main()