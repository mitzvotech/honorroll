import os
import dotenv
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(PROJECT_PATH, ".env"))

from utils import update_organizations
update_organizations('District of Columbia Government')
