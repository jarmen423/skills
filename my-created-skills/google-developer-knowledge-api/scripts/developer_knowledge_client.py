#!/usr/bin/env python3
"""
Google Developer Knowledge API Client

A Python client for accessing Google's developer documentation
via the Developer Knowledge REST API.

IMPORTANT: Despite documentation suggesting API keys work, 
the API actually requires OAuth2/ADC authentication.

Usage:
    from developer_knowledge_client import DeveloperKnowledgeClient
    
    # Using Application Default Credentials (ADC)
    client = DeveloperKnowledgeClient()
    results = client.search("Cloud Storage buckets")
    
    # Using explicit access token
    client = DeveloperKnowledgeClient(access_token="ya29.xxx")
    
    # Using service account JSON file
    client = DeveloperKnowledgeClient(service_account_file="path/to/sa.json")
"""

import os
import json
import urllib.request
import urllib.parse
import subprocess
from typing import Optional


class DeveloperKnowledgeClient:
    """Client for the Google Developer Knowledge API."""
    
    BASE_URL = "https://developerknowledge.googleapis.com/v1alpha"
    SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
    
    def __init__(
        self, 
        access_token: Optional[str] = None,
        service_account_file: Optional[str] = None
    ):
        """
        Initialize the client.
        
        Args:
            access_token: Explicit OAuth2 access token.
            service_account_file: Path to service account JSON file.
            
        If neither is provided, attempts to use Application Default Credentials.
        """
        self._access_token = access_token
        self._service_account_file = service_account_file
        self._cached_token = None
    
    def _get_access_token(self) -> str:
        """Get an OAuth2 access token."""
        if self._access_token:
            return self._access_token
        
        if self._cached_token:
            return self._cached_token
        
        # Try using google-auth library first
        try:
            import google.auth
            import google.auth.transport.requests
            
            if self._service_account_file:
                from google.oauth2 import service_account
                credentials = service_account.Credentials.from_service_account_file(
                    self._service_account_file,
                    scopes=self.SCOPES
                )
            else:
                credentials, _ = google.auth.default(scopes=self.SCOPES)
            
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
            self._cached_token = credentials.token
            return self._cached_token
        except ImportError:
            pass
        
        # Fallback: try gcloud CLI
        try:
            result = subprocess.run(
                ["gcloud", "auth", "application-default", "print-access-token"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                self._cached_token = result.stdout.strip()
                return self._cached_token
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        raise RuntimeError(
            "Could not obtain access token. Options:\n"
            "1. Install google-auth: pip install google-auth\n"
            "2. Run: gcloud auth application-default login\n"
            "3. Pass access_token or service_account_file to constructor"
        )
    
    def _make_request(
        self, 
        endpoint: str, 
        method: str = "GET", 
        data: Optional[dict] = None
    ) -> dict:
        """Make an authenticated HTTP request to the API."""
        url = f"{self.BASE_URL}/{endpoint}"
        
        token = self._get_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        if data:
            request_data = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url, data=request_data, headers=headers, method=method
            )
        else:
            req = urllib.request.Request(url, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            
            # Clear cached token on auth errors
            if e.code in (401, 403):
                self._cached_token = None
            
            raise Exception(f"API Error {e.code}: {error_body}") from e
    
    def search(
        self, 
        query: str, 
        page_size: Optional[int] = None, 
        page_token: Optional[str] = None
    ) -> dict:
        """
        Search for document chunks matching a query.
        
        Args:
            query: The search query string
            page_size: Optional max number of results per page
            page_token: Optional token for pagination
            
        Returns:
            dict with 'documentChunks' array containing:
                - parent: Document identifier for GetDocument
                - content: Snippet of matching content
                - uri: Original documentation URL
        """
        params = {"query": query}
        if page_size:
            params["pageSize"] = str(page_size)
        if page_token:
            params["pageToken"] = page_token
        
        query_string = urllib.parse.urlencode(params)
        endpoint = f"documents:searchDocumentChunks?{query_string}"
        
        return self._make_request(endpoint)
    
    def get_document(self, document_name: str) -> dict:
        """
        Retrieve the full content of a document.
        
        Args:
            document_name: The 'parent' value from search results
                          (e.g., 'documents/developers.google.com/...')
        
        Returns:
            dict with:
                - name: Document identifier
                - uri: Original URL
                - content: Full Markdown content
        """
        # Remove leading slash if present
        if document_name.startswith("/"):
            document_name = document_name[1:]
        
        return self._make_request(document_name)
    
    def batch_get_documents(self, document_names: list[str]) -> dict:
        """
        Retrieve multiple documents at once.
        
        Args:
            document_names: List of 'parent' values from search results
                           (max 100 documents)
        
        Returns:
            dict with 'documents' array containing full document objects
        """
        if len(document_names) > 100:
            raise ValueError("Maximum 100 documents per batch request")
        
        return self._make_request(
            "documents:batchGet",
            method="POST",
            data={"names": document_names}
        )
    
    def search_and_get(self, query: str, max_results: int = 5) -> list[dict]:
        """
        Convenience method: search and fetch full documents.
        
        Args:
            query: Search query
            max_results: Maximum documents to retrieve
            
        Returns:
            List of full document objects
        """
        search_results = self.search(query, page_size=max_results)
        chunks = search_results.get("documentChunks", [])
        
        if not chunks:
            return []
        
        # Get unique parent documents
        parents = list({chunk["parent"] for chunk in chunks})[:max_results]
        
        if len(parents) == 1:
            return [self.get_document(parents[0])]
        else:
            result = self.batch_get_documents(parents)
            return result.get("documents", [])


def main():
    """Demo usage of the client."""
    import sys
    
    print("Initializing Developer Knowledge API client...")
    
    try:
        client = DeveloperKnowledgeClient()
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Example search
    query = sys.argv[1] if len(sys.argv) > 1 else "Cloud Storage buckets"
    print(f"Searching for: {query}\n")
    
    try:
        results = client.search(query, page_size=3)
    except Exception as e:
        print(f"Search failed: {e}")
        sys.exit(1)
    
    chunks = results.get("documentChunks", [])
    if not chunks:
        print("No results found")
        return
    
    print(f"Found {len(chunks)} results:\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"--- Result {i} ---")
        print(f"URL: {chunk.get('uri')}")
        print(f"Parent: {chunk.get('parent')}")
        content = chunk.get("content", "")[:300]
        print(f"Preview: {content}...")
        print()
    
    # Fetch full document for first result
    print("\n--- Fetching full document for first result ---")
    doc = client.get_document(chunks[0]["parent"])
    content = doc.get("content", "")
    print(f"Document length: {len(content)} characters")
    print(f"First 500 chars:\n{content[:500]}...")


if __name__ == "__main__":
    main()
