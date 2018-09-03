import time

timeout = time.time() + 5  # round minutes from now
while True:
    if time.time() > timeout:
        break
    print ("dsfsdfsdfs")
