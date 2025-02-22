if __name__ == '__main__':
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()
    uvicorn.run("thumbnail.main:app", host="0.0.0.0", port=8086, reload=True)
