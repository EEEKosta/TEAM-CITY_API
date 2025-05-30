import pytest
import requests
from api.api_manager import ApiManager
from data.project_data import ProjectData
from data.user_data import UserData
from entities.user import User, Role
from enums.roles import Roles
from resources.user_creds import SuperAdminCreds


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

# создаем объект юзера (SuperAdmin) с использование учетных данных из SuperAdminCreds
@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, new_session, ['SUPER_ADMIN', 'g'])
    super_admin.api_manager.auth_api.auth_and_get_csfr(super_admin.creds)
    return super_admin


@pytest.fixture
def super_admin_creds():
    return SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD


@pytest.fixture
def user_create(user_session, super_admin):
    created_user_pool = [] # сохраняем юзеров, потом можем удалить


    def  _user_create(role):
        user_data = UserData.create_user_data(role, scope='g')
        super_admin.api_manager.user_api.create_user(user_data)
        new_session = user_session()
        created_user_pool.append(user_data['username'])
        return User(user_data['username'], user_data['password'], new_session, [Role(role)])

    yield _user_create

    for username in created_user_pool:
        super_admin.api_manager.user_api.delete_user(username)


@pytest.fixture
def project_data(super_admin):
    project_id_pool = []

    def _create_data():
        project = ProjectData.create_project_data()
        project_id_pool.append(project.id)
        return project

    yield _create_data

    for project_id in project_id_pool:
        super_admin.api_manager.project_api.clean_up_project(project_id)