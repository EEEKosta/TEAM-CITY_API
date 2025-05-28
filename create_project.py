import requests
import pytest

from custom_requester.custom_requester import CustomRequester
from data.project_data import ProjectData


class TestProjectCreate:
    project_data = None

    @classmethod
    def setup_class(cls):
        cls.project_data= ProjectData.create_project_data()
        cls.create_project_id = cls.project_data["id"]

    def test_project_create(self):
        requester=CustomRequester(requests.Session())
        requester.session.auth = ("admin","admin")
        # Получение токена
        csrf_token = requester.send_request("GET", "/authenticationTest.html?csrf").text
        requester._update_session_headers(**{"X-TC-CSRF-Token": csrf_token})

        # Создание проекта
        create_responce = requester.send_request("POST", "/app/rest/projects", data=self.project_data)
        assert create_responce.status_code == 200, "Не удалось создать проект"

        check_project = requester.send_request("GET", f"/app/rest/projects/id:{self.create_project_id}")
        assert check_project.status_code == 200

        # Удаление проекта
        delete_project = requester.send_request("DELETE", f"/app/rest/projects/id:{self.create_project_id}", expected_status=204)
        assert delete_project.status_code == 204, "Не удалось удалить проект"