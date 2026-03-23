import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.vector_store import VectorStoreService


try:
    print("Initializing VectorStoreService...")
    service = VectorStoreService()
    print("Loading documents...")
    service.load_document()
    print("Test completed successfully!")
except Exception:
    print("Error occurred:")
    traceback.print_exc()
