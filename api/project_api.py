from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class ProjectAPI(CustomRequester):

    def create_project(self, project_data, expected_status=HTTPStatus.OK):
        return self.send_request('POST', '/app/rest/projects', data=project_data, expected_status=expected_status)

    def get_project(self):
        return self.send_request('GET', '/app/rest/projects')

    def get_project_by_locator(self, locator):
        return self.send_request('GET', f'/app/rest/projects/{locator}')

    def delete_project(self, project_id, expected_status=HTTPStatus.NO_CONTENT):
        return self.send_request('DELETE', f'/app/rest/projects/{project_id}', expected_status=expected_status)

    def clean_up_project(self, created_project_id):
        self.delete_project(created_project_id)
        get_projects_response = self.get_project().json()
        project_ids = [project.get('id', {}) for project in get_projects_response.get('project', [])]
        assert created_project_id not in project_ids, f'Project {created_project_id} already exists'
