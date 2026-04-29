import gzip
import json
import os
from datetime import datetime, timedelta
from pymongo import MongoClient

# Mongo connection
client = MongoClient("mongodb://localhost:27017")
db = client["weather_db"]        # adjust if needed
collection = db["weather_data"]  # adjust if needed

# Calculate the "older than 1 month" cutoff
cutoff = datetime.utcnow() - timedelta(days=30)

# Query old documents
old_docs = list(collection.find({"timestamp": {"$lt": cutoff}}))

if not old_docs:
    print("No documents older than 1 month.")
    exit()

# Ensure archive directory exists
archive_dir = "/home/speakbot/e-servant-chatbot/weather-archives"
os.makedirs(archive_dir, exist_ok=True)

# JSON filename
json_path = os.path.join(
    archive_dir,
    f"weather_archive_{datetime.utcnow().strftime('%Y-%m-%d')}.json"
)

# Write raw JSON file
with open(json_path, "w") as f:
    json.dump(old_docs, f, default=str, indent=2)

# Compress using gzip
gz_path = json_path + ".gz"
with open(json_path, "rb") as f_in:
    with gzip.open(gz_path, "wb") as f_out:
        f_out.writelines(f_in)

print(f"Compressed archive created: {gz_path}")

# Delete the raw JSON file (keep only compressed)
os.remove(json_path)

# Delete old documents from MongoDB
#result = collection.deleteMany({"timestamp": {"$lt": cutoff}})
#print(f"Deleted {result.deleted_count} documents older than 1 month.")

result = collection.delete_many({"timestamp": {"$lt": cutoff}})
print(f"Deleted {result.deleted_count} documents older than 1 month.")


