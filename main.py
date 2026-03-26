from fastapi import FastAPI

app = FastAPI()

# Define a simple route
@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is the about page!"}