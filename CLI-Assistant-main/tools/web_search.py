from duckduckgo_search import DDGS

def search_web(query):
    """
    Searches the web using DuckDuckGo and returns formatted results.
    """
    try:
        # Using the context manager for DDGS as recommended in the latest documentation
        with DDGS() as ddgs:
            # We use the .text method to get search results
            results = list(ddgs.text(query, max_results=10))
            
            if not results:
                return "לא נמצאו תוצאות לחיפוש המבוקש."
            
            formatted_output = "--- Web Search Results ---\n\n"
            for i, r in enumerate(results, 1):
                title = r.get('title', 'No Title')
                link = r.get('href', 'No Link')
                snippet = r.get('body', 'No Description available.')
                
                formatted_output += f"{i}. {title}\n"
                formatted_output += f"    Source: {link}\n"
                formatted_output += f"    Snippet: {snippet}\n\n"
            
            return formatted_output
            
    except Exception as e:
        return f"Error occurred while searching web: {str(e)}"