# Azure Cosmos DB Python SDK Pagination Example

This example demonstrates how to use pagination features with the Azure Cosmos DB Python SDK.

## Features Demonstrated
- Basic pagination with continuation tokens
- Manual pagination through all results
- Control of page sizes
- Handling large result sets efficiently

## Prerequisites
- Python 3.6+
- Azure Cosmos DB Emulator running locally
- azure-cosmos package installed

## Running the Sample
1. Ensure the Cosmos DB Emulator is running
2. Run the script:
```powershell
python pagination_sample.py
```

## Expected Output
The sample will:
1. Insert 25 sample items into the container
2. Demonstrate basic pagination (first page)
3. Show manual pagination through all items with continuation tokens

## Key Concepts
- `max_item_count`: Controls the maximum number of items per page
- `continuation_token`: Used to get the next page of results
- `enable_cross_partition_query`: Required for queries that span multiple partitions