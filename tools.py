from ddgs import DDGS
from langchain_core.tools import tool

@tool
def calculator(expression: str):
    """
    A simple calculator tool that evaluates mathematical expressions.

    Args:
        expression (str): The mathematical expression to evaluate.

    Returns:
        str: The result of the evaluated expression.
    """
    try:
        # Evaluate the expression and return the result
        print("calculator tool called")
        result = eval(expression)
        print(f"result======{result}")
        return result
    except Exception as e:
        return f"Error evaluating expression: {e}"

@tool
def search_tool(query: str):
    """
    A search tool that uses DuckDuckGo to perform web searches.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    try:
        results = []
        last_error = None

        for _ in range(3):
            try:
                results = DDGS().text(query, max_results = 4, backend="HTML")
                break
            except Exception as e:
                last_error = e
        if not results and last_error:
            return f"Search Failed: {last_error}"

        if not results:
            return "No Live Search Results Found for this question"

        lines = []

        for item in results:
            title = item.get("title", "")

            snippet = item.get("body", "")

            lines.append(f"{title}: {snippet}")

        return "\n".join(lines)
    except Exception as e:
        return f"Error performing search: {e}"