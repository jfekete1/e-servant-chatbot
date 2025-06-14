from pymongo import MongoClient

# Connect to MongoDB (default local Docker port)
client = MongoClient("mongodb://localhost:27017/")
db = client["weather_db"]
collection = db["weather_data"]

# Use the 'collstats' command to get storage stats
stats = db.command("collstats", collection.name)

# Extract key values
count = stats.get("count")
size_bytes = stats.get("size")
storage_size_bytes = stats.get("storageSize")
index_size_bytes = stats.get("totalIndexSize")

# Convert bytes to more readable units
def to_mb(bytes_val):
    return round(bytes_val / (1024 * 1024), 2)

print(f"📊 Collection: {collection.name}")
print(f"📁 Documents: {count}")
print(f"📦 Data Size (raw): {to_mb(size_bytes)} MB")
print(f"🧱 Storage Size (allocated): {to_mb(storage_size_bytes)} MB")
print(f"🔍 Index Size: {to_mb(index_size_bytes)} MB")
