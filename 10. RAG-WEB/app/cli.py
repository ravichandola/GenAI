from ingestion import ingest_url_to_qdrant
from retrieval import get_answer
import logging
from urllib.parse import urlparse
import sys
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def validate_environment():
    """Validate that all required environment variables are set."""
    required_vars = ['OPENAI_API_KEY', 'QDRANT_HOST', 'COLLECTION_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("\nError: Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        print("\nPlease create a .env file with the required variables.")
        sys.exit(1)

def print_header():
    """Print the CLI header."""
    print("\n=== Web Content RAG CLI ===")
    print("This tool allows you to ingest web content and ask questions about it.")
    print("Type 'exit' at any prompt to quit.\n")

def get_menu_choice():
    """Display menu and get user choice."""
    while True:
        print("\nOptions:")
        print("1. Ingest a webpage")
        print("2. Ask a question")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice in ['1', '2', '3', 'exit']:
            return choice
        else:
            print("\nInvalid choice. Please try again.")

def handle_ingest():
    """Handle webpage ingestion."""
    while True:
        url = input("\nEnter the URL to ingest (or 'back' to return to menu): ").strip()
        
        if url.lower() == 'back':
            return
            
        try:
            result = ingest_url_to_qdrant(url)
            print("\nSuccess!")
            print(f"- Message: {result['message']}")
            print(f"- URL: {result['url']}")
            print(f"- Number of chunks: {result['num_chunks']}")
            print(f"- Collection: {result['collection_name']}")
            return
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again with a different URL.")

def handle_query():
    """Handle question answering."""
    while True:
        query = input("\nEnter your question (or 'back' to return to menu): ").strip()
        
        if query.lower() == 'back':
            return
            
        if not query:
            print("\nError: Question cannot be empty. Please try again.")
            continue
            
        try:
            result = get_answer(query)
            
            print("\nAnswer:")
            print(f"{result['answer']}\n")
            
            if result['sources']:
                print("Sources:")
                for source in result['sources']:
                    print(f"- {source}")
                    
            print(f"\nNumber of relevant documents: {result['num_docs_retrieved']}")
            return
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again with a different question.")

def main():
    """Main CLI function."""
    try:
        # Validate environment
        validate_environment()
        
        # Print header
        print_header()
        
        while True:
            choice = get_menu_choice()
            
            if choice in ['3', 'exit']:
                print("\nGoodbye!")
                break
                
            elif choice == '1':
                handle_ingest()
                
            elif choice == '2':
                handle_query()
                
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print("\nAn unexpected error occurred. Please check the logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 