import os
from dotenv import load_dotenv
load_dotenv()

from api import get_rounds

if __name__ == "__main__":
    print(f"Token is {os.getenv('TOKEN')}")
    
    print(get_rounds()['now'])