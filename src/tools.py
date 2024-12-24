def log(path:str, content:str) -> None:
    if path != None and path != "":
        f = open(path, "a")
        f.write(content + "\n")
        f.close()