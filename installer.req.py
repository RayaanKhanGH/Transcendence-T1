import os

def verify_requirements():
    if not os.path.exists('requirements.txt'):
        return False
    else:
        return True
    

def install():
    os.system("pip install -r requirements.txt")

if __name__ == "__main__":
    if verify_requirements():
        install()
    else:
        print("requirements.txt not found.")
        exit(1)