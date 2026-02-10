# def main():
#     print("Hello from learn-fastapi!")


# if __name__ == "__main__":
#     main()

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", host = "0.0.0.0", port = 8000, reload = True)
    # inside the folder app - there is a file named app - inside this file I am running the app variable as the server
    # 0.0.0.0 means run it on any available domain
    # /hello-world is available in the port 8000
    # Reload = True will make sure when ever there is a change in the file it will stop and restart the server