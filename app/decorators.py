def fence(func): 
    def wrapper(): 
        print("+" * 20) 
        func() 
        print("+" * 20) 
    return wrapper

@fence
def log():
    print("Logging from the log function.")

log()