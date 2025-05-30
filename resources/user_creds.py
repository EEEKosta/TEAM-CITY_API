import os
from dotenv import load_dotenv

load_dotenv()


class SuperAdminCreds:
    USERNAME = 'admin'
    #PASSWORD = os.getenv('SUPER_ADMIN_TOKEN')
    PASSWORD = 'admin'