import httpx


def search(url: str) -> str:
    """Demo web retrieval tool.

    For production, use an allowlisted search provider rather than accepting
    arbitrary URLs from an untrusted model.
    """
    if not (url.startswith("https://") or url.startswith("http://")):
        raise ValueError("Only http/https URLs are allowed")

    response = httpx.get(url, timeout=5.0, follow_redirects=True)
    response.raise_for_status()

    # Teaching simplification: return a bounded slice.
    return response.text[:5000]


def schema() -> dict:
    return {
        "name": "search",
        "description": "Fetch text from a public HTTP/HTTPS URL for demonstration.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string"}
            },
            "required": ["url"],
        },
    }
