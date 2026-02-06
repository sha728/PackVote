try:
    print("Importing google.generativeai...")
    import google.generativeai as genai
    print("google.generativeai imported successfully.")
except ImportError as e:
    print(f"FAILED to import google.generativeai: {e}")
except Exception as e:
    print(f"CRASH during import: {e}")

try:
    print("Importing app.main...")
    from app.main import app
    print("app.main imported successfully.")
except Exception as e:
    print(f"FAILED to import app.main: {e}")
