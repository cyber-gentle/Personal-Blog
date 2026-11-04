import json, os, random

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "data")

def load_articles() -> tuple[dict[int, dict], list]:
    
    articles = {}
    errors = []
    
    for article_num, article_file in enumerate(os.listdir(DATA_DIR_PATH), start=1):
        full_path = os.path.join(DATA_DIR_PATH, article_file)
        if os.path.isfile(full_path):
            try:
                with open(file=full_path, mode="r", encoding="utf-8") as file:
                    content = json.loads(file.read())
                    
                    if not content:
                        errors.append(f"{full_path} is empty")
                    
                    articles[article_num] = content
                        
            except json.JSONDecodeError:
                errors.append(f"{full_path} is undecodeable")
            except FileNotFoundError:
                errors.append(f"{full_path} is not found")
            except Exception as err:
                errors.append(f"{full_path}: unexpected error: {err}")
            
    return (articles, errors)
    
    
def save_article(article_id: int, article: dict) -> str:
    full_path = os.path.join(DATA_DIR_PATH, f"article_{article_id:03d}.json")
    if not full_path or not isinstance(full_path, str):
        return "File name must be a string"

    if not isinstance(article, dict):
        return "Blog article must be a dictionary"

    try:
        with open(file=full_path, mode="w") as file:
            json.dump(article, file, indent=4)
            return "file saved successfully"
    except FileNotFoundError:
        return "Failed to save article"
    except Exception as err:
        return f"Unexpected error: {err}"


def save_articles(articles: dict[int, dict]) -> str:
    for article_id, article in articles.items():
        result = save_article(article_id, article)
        if "error" in result.lower() or "failed" in result.lower():
            return result
    return "all articles saved successfully"
    
    
    