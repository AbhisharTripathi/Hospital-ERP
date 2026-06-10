from app import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port= 8000, host="0.0.0.0", reload= True)