import requests

couchdb1_url = "http://admin:password@localhost:5984"
couchdb2_url = "http://admin:password@localhost:5985"
couchdb3_url = "http://admin:password@localhost:5986"
replicator_db = "_replicator"

def check_replication_status(couchdb_url):
    try:
        url = f"{couchdb_url}/{replicator_db}/_all_docs?include_docs=true"
        response = requests.get(url)
        response.raise_for_status()
        
        replication_docs = response.json().get("rows", [])
        db_name = couchdb_url.split('@')[1]
        
        active_replications = any(
            doc.get("doc", {}).get("continuous") is True and
            "error" not in doc.get("doc", {})
            for doc in replication_docs
        )
        
        print(f"Database {db_name} is {'replicating' if active_replications else 'not replicating'}")

    except requests.exceptions.RequestException:
        print(f"Database {db_name} is not accessible")

if __name__ == "__main__":
    for url in [couchdb1_url, couchdb2_url, couchdb3_url]:
        check_replication_status(url)