
import requests
import json

couchdb1_url = "http://admin:password@localhost:5984"
couchdb2_url = "http://admin:password@localhost:5985"
couchdb3_url = "http://admin:password@localhost:5986"
replicator_db = "_replicator"

replication_data_template = {
    "source": "",
    "target": "",
    "continuous": True,
    "create_target": True
}


def create_replication_document(couchdb_url, replication_data):
    try:
        url = f"{couchdb_url}/{replicator_db}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(replication_data))
        
        response.raise_for_status()
        replication_doc = response.json()
        print(json.dumps(replication_doc, indent=4))
        return replication_doc.get("id")  

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error creating replication document: {e}")


def ensure_replicator_db_exists(couchdb_url):
    """ตรวจสอบและสร้างฐานข้อมูล `_replicator` หากยังไม่มี"""
    try:
        url = f"{couchdb_url}/{replicator_db}"
        headers = {"Content-Type": "application/json"}
        
        response = requests.put(url, headers=headers)
        
        if response.status_code == 201:
            print(f"Successfully created '{replicator_db}' on {couchdb_url}")
        elif response.status_code == 412:
            print(f"'{replicator_db}' already exists on {couchdb_url}")
        else:
            print(f"Failed to create '{replicator_db}' on {couchdb_url}: {response.status_code} {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error ensuring replicator database exists: {e}")


if __name__ == "__main__":
    print("Ensuring replicator databases exist...")
    ensure_replicator_db_exists(couchdb1_url)
    ensure_replicator_db_exists(couchdb2_url)
    ensure_replicator_db_exists(couchdb3_url)

    print("\nCreating replication from CouchDB1 to CouchDB2...")
    replication_data_template["source"] = "http://admin:password@couchdb1:5984/usernames"
    replication_data_template["target"] = "http://admin:password@couchdb2:5984/usernames"
    replication_id = create_replication_document(couchdb1_url, replication_data_template)

    if replication_id:
        print("Creating replication from CouchDB2 to CouchDB3...")
        replication_data_template["source"] = "http://admin:password@couchdb2:5984/usernames"
        replication_data_template["target"] = "http://admin:password@couchdb3:5984/usernames"
        replication_data_template["_id"] = replication_id  
        create_replication_document(couchdb2_url, replication_data_template)

        print("Creating replication from CouchDB3 to CouchDB1...")
        replication_data_template["source"] = "http://admin:password@couchdb3:5984/usernames"
        replication_data_template["target"] = "http://admin:password@couchdb1:5984/usernames"
        create_replication_document(couchdb3_url, replication_data_template)
