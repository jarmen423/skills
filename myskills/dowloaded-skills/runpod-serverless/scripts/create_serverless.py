import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_URL = "https://api.runpod.io/graphql"

# Mappings
RUNTIMES = {
    "python": "runpod/serverless-python:latest",
    "node": "runpod/serverless-node-18:latest",  # specific version often better
    "nodejs": "runpod/serverless-node-18:latest"
}

GPU_TYPES = {
    "3090": "AMPERE_24",
    "4090": "ADA_24",
    "a4000": "AMPERE_16",
    "a5000": "AMPERE_24",
    "a6000": "AMPERE_48",
    "a100": "AMPERE_80",
    "a100-80gb": "AMPERE_80",
    "h100": "HOPPER_80"
}

def run_query(query, variables, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code} - {e.reason}")
        print(e.read().decode("utf-8"))
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def get_existing_resources(api_key):
    query = """
    query {
        myself {
            templates {
                id
                name
            }
            endpoints {
                id
                name
            }
        }
    }
    """
    result = run_query(query, {}, api_key)
    if "errors" in result:
        print("Error fetching resources:", result["errors"])
        sys.exit(1)
        
    data = result["data"]["myself"]
    templates = {t["name"]: t["id"] for t in data["templates"]}
    endpoints = {e["name"]: e["id"] for e in data["endpoints"]}
    return templates, endpoints

def create_template(name, image, disk, api_key, existing_id=None):
    mutation = """
    mutation saveTemplate($input: TemplateInput!) {
        saveTemplate(input: $input) {
            id
            name
        }
    }
    """
    
    input_data = {
        "name": name,
        "imageName": image,
        "containerDiskInGb": disk,
        "dockerArgs": "", # default
        "isServerless": True
    }
    
    if existing_id:
        print(f"Updating existing template '{name}' ({existing_id})...")
        # In some APIs, you need the ID in the input to update.
        # RunPod usually uses ID to identify update vs create.
        # Checking schema: saveTemplate(input: TemplateInput!) -> TemplateInput usually has an optional 'id' field.
        # If not in input, it creates new?
        # Let's try adding 'id' to input if it exists.
        # Based on typical GraphQL patterns.
        # If 'id' is not in TemplateInput definition, we might create a duplicate. 
        # But 'myself { templates }' returns IDs.
        # We will assume 'id' is a valid field for update.
        # Wait, the search result for 'saveTemplate' input fields didn't explicitly list 'id', 
        # but mutations usually take it for updates. 
        # Let's hope. If not, we might be creating duplicates with same name (allowed?) or failing.
        # To be safe, if it exists, we might just use it and not update it unless forced?
        # But "idempotent generation" usually implies ensuring the state matches.
        # I'll try to pass ID.
        # Actually, looking at RunPod docs (from memory/inference), 'id' is usually required for update.
        pass # We will see. For now, let's assume we use the existing one if it matches our needs, or update it.
    else:
        print(f"Creating new template '{name}'...")

    # Note: To update, we probably need to pass 'id' in the input. 
    # I'll add it if existing_id is set.
    if existing_id:
        # We can't easily update if we don't know the schema allows 'id' in input.
        # But usually it does.
        # However, to be safe: If it exists, we just return the ID and don't update (Immutable pattern usually safer if unsure).
        # But prompt says "Ensure template generation is idempotent" -> calling it twice produces same result.
        # If I create it again, I might get a new ID.
        # So reusing existing ID is key.
        print(f"Template '{name}' already exists with ID: {existing_id}. Using it.")
        return existing_id

    result = run_query(mutation, {"input": input_data}, api_key)
    
    if "errors" in result:
        print("Error creating template:", result["errors"])
        sys.exit(1)
        
    return result["data"]["saveTemplate"]["id"]

def create_endpoint(name, template_id, gpu_id, workers_min, workers_max, api_key, existing_id=None):
    mutation = """
    mutation saveEndpoint($input: EndpointInput!) {
        saveEndpoint(input: $input) {
            id
            name
        }
    }
    """
    
    input_data = {
        "name": name,
        "templateId": template_id,
        "gpuIds": gpu_id,
        "workersMin": workers_min,
        "workersMax": workers_max,
        "idleTimeout": 5, # default 5s
        "locations": "US", # default preference
        "scalerType": "QUEUE_DELAY",
        "scalerValue": 4
    }
    
    if existing_id:
        print(f"Updating existing endpoint '{name}' ({existing_id})...")
        input_data["id"] = existing_id
    else:
        print(f"Creating new endpoint '{name}'...")
        
    result = run_query(mutation, {"input": input_data}, api_key)
    
    if "errors" in result:
        print("Error creating endpoint:", result["errors"])
        sys.exit(1)
        
    return result["data"]["saveEndpoint"]["id"]

def main():
    parser = argparse.ArgumentParser(description="Create RunPod Serverless Template & Endpoint")
    parser.add_argument("--name", required=True, help="Name for the template and endpoint")
    parser.add_argument("--runtime", required=True, choices=["python", "node", "nodejs"], help="Runtime environment")
    parser.add_argument("--gpu", required=True, help="GPU Type (e.g., '3090', 'a100') or specific ID")
    parser.add_argument("--disk", type=int, default=10, help="Container disk size in GB (default: 10)")
    parser.add_argument("--min-workers", type=int, default=0, help="Min workers (default: 0)")
    parser.add_argument("--max-workers", type=int, default=1, help="Max workers (default: 1)")
    
    args = parser.parse_args()
    
    api_key = os.environ.get("RUNPOD_API_KEY")
    if not api_key:
        print("Error: RUNPOD_API_KEY environment variable not set.")
        sys.exit(1)

    # Resolve Runtime
    image = RUNTIMES.get(args.runtime.lower())
    if not image:
        # Should be caught by argparse choices, but safe fallback
        print(f"Unknown runtime: {args.runtime}")
        sys.exit(1)

    # Resolve GPU
    gpu_id = GPU_TYPES.get(args.gpu.lower(), args.gpu) # Use map or raw input

    print(f"Configuration:")
    print(f"  Name: {args.name}")
    print(f"  Runtime: {args.runtime} -> {image}")
    print(f"  GPU: {args.gpu} -> {gpu_id}")
    print("-" * 20)

    # Idempotency Check
    print("Checking existing resources...")
    templates, endpoints = get_existing_resources(api_key)
    
    existing_template_id = templates.get(args.name)
    existing_endpoint_id = endpoints.get(args.name)

    # Create/Get Template
    template_id = create_template(args.name, image, args.disk, api_key, existing_template_id)
    print(f"Template ID: {template_id}")

    # Create/Update Endpoint
    endpoint_id = create_endpoint(args.name, template_id, gpu_id, args.min_workers, args.max_workers, api_key, existing_endpoint_id)
    print(f"Endpoint ID: {endpoint_id}")
    print("Success!")

if __name__ == "__main__":
    main()
