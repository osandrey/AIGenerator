import uvicorn
from fastapi import FastAPI
from src.routes import text_generator, auth

app = FastAPI(title="AIGenerator", swagger_ui_parameters={"operationsSorter": "method"})


app.include_router(text_generator.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

@app.get("/")
def root():
    return {"message": "Welcome to AIGenerator!"}



if __name__ == '__main__':
    uvicorn.run("main:app",host="localhost", port=8000, reload=True)