# Import required Azure Cosmos DB SDK components
# CosmosClient: Main class for database operations
# PartitionKey: Class for defining how data is distributed across partitions
from azure.cosmos import CosmosClient, PartitionKey

# Initialize connection to Cosmos DB (using local emulator)
# The emulator runs on port 8081 by default and uses a well-known key
client = CosmosClient(
    url="https://localhost:8081",  # Local emulator endpoint
    credential=(  # Default emulator master key
        "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGG"
        "yPMbIZnqyMsEcaGQy67XIw/Jw=="
    )
)

# Define database and container names
# These must match the names in app.py if you want to query the same data
database_name = "cosmicworks"  # Our database name
container_name = "products"    # Our container (collection) name

# Get references to database and container
# These clients are lightweight and don't make network calls until used
database = client.get_database_client(database_name)  # Get database client
container = database.get_container_client(container_name)  # Get container client

def insert_sample_items(count=25):
    """Insert sample items to demonstrate pagination
    
    Args:
        count (int): Number of sample items to create (default: 25)
        
    This function creates {count} items with sequential IDs and prices
    Each item has:
    - id: Unique identifier (item_0, item_1, etc.)
    - name: Product name (Product 0, Product 1, etc.)
    - category: Fixed value "Sample"
    - price: Sequential price (0.99, 1.99, etc.)
    """
    print(f"\nInserting {count} sample items...")
    
    # Create and insert items one by one
    for i in range(count):
        # Create an item with unique id and sequential values
        item = {
            "id": f"item_{i}",        # Unique ID (used as partition key)
            "name": f"Product {i}",    # Product name
            "category": "Sample",      # Fixed category
            "price": float(i) + 0.99   # Sequential price
        }
        # Upsert: Creates if not exists, updates if exists
        container.upsert_item(item)
    print("Sample items inserted.")

def demonstrate_pagination(page_size=10):
    """Demonstrate different pagination approaches
    
    Args:
        page_size (int): Number of items per page (default: 10)
        
    Shows two pagination approaches:
    1. Basic: Get just the first page
    2. Complete: Iterate through all pages using continuation tokens
    
    Cosmos DB pagination uses continuation tokens to efficiently
    resume reading results from where the previous page ended.
    """
    
    print("\n1. Basic pagination with continuation tokens:")
    print("-" * 50)
    
    # Define the query - select all items, ordered by name
    # ORDER BY is important for consistent pagination results
    query = "SELECT * FROM c ORDER BY c.name"
    
    # Get just the first page of results
    # enable_cross_partition_query=True allows querying across partition key values
    # max_item_count controls the page size
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True,  # Required for queries across partitions
        max_item_count=page_size           # Maximum items per page
    ))
    
    # Display the first page
    print(f"First page ({len(items)} items):")
    for item in items:
        print(f"- {item['name']}")
    
    print("\n2. Manual pagination through all items:")
    print("-" * 50)
    
    # Initialize tracking variables
    continuation_token = None  # Tracks where to resume reading
    page_number = 1          # Tracks current page number
    total_items = 0         # Tracks total items seen
    
    # Loop until we've read all pages
    while True:
        # Get the next page of results
        # continuation_token tells Cosmos DB where to resume reading
        page_query = container.query_items(
            query=query,
            enable_cross_partition_query=True,
            max_item_count=page_size,
            continuation_token=continuation_token  # None on first page, then populated
        )
        
        # Convert query results to a list and update counts
        items = list(page_query)
        total_items += len(items)
        
        # Display the current page
        print(f"\nPage {page_number} ({len(items)} items):")
        for item in items:
            print(f"- {item['name']}")
        
        # Get token for next page
        # If None, we've reached the end
        continuation_token = page_query.continuation_token
        if not continuation_token:
            break  # No more pages
            
        page_number += 1  # Move to next page
    
    # Show final statistics
    print(f"\nRetrieved {total_items} total items in {page_number} pages")

def main():
    """Main function that runs the complete pagination demonstration
    
    1. Creates sample data (25 items by default)
    2. Shows pagination with 10 items per page
    """
    # First, insert some sample items to work with
    insert_sample_items(25)
    
    # Then show how pagination works with these items
    demonstrate_pagination(page_size=10)

# Standard Python idiom: only run if this is the main script
if __name__ == "__main__":
    main()