Create virtual environment 
# python3 -m venv myenv
Activate virtual environment 
# source myenv/bin/activate

# pip install fastapi uvicorn pyd

Uvicorn is a lightning-fast ASGI (Asynchronous Server Gateway Interface) server for Python. It's what actually runs your FastAPI application and handles incoming HTTP requests.

# uvicorn main:app --reload
