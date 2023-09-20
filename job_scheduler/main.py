from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from route import bacalau_script

app = FastAPI(debug=True)

# TODO: restriction to only specific origin of requests (for our case its only docker call).
app.add_middleware(
    CORSMiddleware
)

app.include_router(bacalau_script.router)

@app.get("/")
def entrypoint():
    return {"message": "LidarHD API server is working"}



if __name__ ==  "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)