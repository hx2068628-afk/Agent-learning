from rag.vector_store import VectorStoreService
import traceback

try:
    print("Initializing VectorStoreService...")
    service = VectorStoreService()
    print("Loading documents...")
    service.load_document()
    print("Test completed successfully!")
except Exception as e:
    print("Error occurred:")
    traceback.print_exc()
