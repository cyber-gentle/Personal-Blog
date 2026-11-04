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
    
    
def save_article(articles: dict[int, dict], total_article: int) -> str:
    full_path = os.path.join(DATA_DIR_PATH, f"article_{total_article+1}")
    if not filepath or not isinstance(filepath, str):
        return "File name must be a string"
    
    if not isinstance(blog_articles, dict[int, dict]):
        return "Blog articles must be a nested dictionary"
     
    try:
        with open(file=fullpath, mode="w") as file:
            json.dump(articles, file, indent=4)
    except FileNotFoundError:
        return "Failed to save article"
    except Exception as err:
        return f"Unexpected error: {err}"
    
    
    