from data.project_data import ProjectData, ProjectResponseModel
from enums.roles import Roles


class TestProjectCreate:

    def test_project_create_with_role_model(self, super_admin, user_create, project_data):
        project_data1 = project_data()
        create_project_response = super_admin.api_manager.project_api.create_project(project_data1.model_dump()).text
        project_response = ProjectResponseModel.model_validate_json(create_project_response)
        assert project_response.id == project_data1.id

        get_projects_response = super_admin.api_manager.project_api.get_project_by_locator(project_data1.id).text
        created_project = ProjectResponseModel.model_validate_json(get_projects_response)
        assert created_project.id == project_data1.id
