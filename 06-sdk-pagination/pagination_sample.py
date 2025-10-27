from azure.cosmos import CosmosClient, PartitionKey

# Initialize the Cosmos Client
client = CosmosClient(
    url="https://localhost:8081",
    credential=(
        "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGG"
        "yPMbIZnqyMsEcaGQy67XIw/Jw=="
    )
)

# Database and container names
database_name = "cosmicworks"
container_name = "products"

# Get database and container
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def insert_sample_items(count=25):
    """Insert sample items to demonstrate pagination"""
    print(f"\nInserting {count} sample items...")
    
    for i in range(count):
        item = {
            "id": f"item_{i}",
            "name": f"Product {i}",
            "category": "Sample",
            "price": float(i) + 0.99
        }
        container.upsert_item(item)
    print("Sample items inserted.")

def demonstrate_pagination(page_size=10):
    """Demonstrate different pagination approaches"""
    
    print("\n1. Basic pagination with continuation tokens:")
    print("-" * 50)
    
    # Query with a small page size
    query = "SELECT * FROM c ORDER BY c.name"
    
    # Get the first page
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True,
        max_item_count=page_size
    ))
    
    print(f"First page ({len(items)} items):")
    for item in items:
        print(f"- {item['name']}")
    
    print("\n2. Manual pagination through all items:")
    print("-" * 50)
    
    # Initialize parameters for paging
    continuation_token = None
    page_number = 1
    total_items = 0
    
    while True:
        # Get the next page of results
        page_query = container.query_items(
            query=query,
            enable_cross_partition_query=True,
            max_item_count=page_size,
            continuation_token=continuation_token
        )
        
        # Get the results and continuation token
        items = list(page_query)
        total_items += len(items)
        
        # Print the current page
        print(f"\nPage {page_number} ({len(items)} items):")
        for item in items:
            print(f"- {item['name']}")
        
        # Get continuation token and break if we're done
        continuation_token = page_query.continuation_token
        if not continuation_token:
            break
            
        page_number += 1
    
    print(f"\nRetrieved {total_items} total items in {page_number} pages")

def main():
    # First, insert some sample items
    insert_sample_items(25)
    
    # Then demonstrate pagination
    demonstrate_pagination(page_size=10)

if __name__ == "__main__":
    main()