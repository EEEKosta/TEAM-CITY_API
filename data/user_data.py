from utils.data_generator import DataGenerator
from enums.roles import Roles


class UserData:
    @classmethod
    def create_user_data(cls, role=Roles.SYSTEM_ADMIN.value, scope='g'):
        return {
            'username': DataGenerator.fake_name(),
            'password': DataGenerator.fake_project_id(),
            'email': 'example@mail.com', # добавить в фейкер генерацию почты
            'roles':{
                'role':[
                    {
                        'roleId': role,
                        'scope': scope,
                    }
                ]
            }
        }
