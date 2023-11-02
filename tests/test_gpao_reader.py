import requests
import json
import pytest
import requests_mock
from gpao.reader import Reader

# Test data
mock_url_api = "http://gpao-mock.fr:8080"

mock_projects = [
    {
        'project_id': 1,
        'project_name': 'project_1', 
        'project_priority': 'normal', 
        'project_status': 'running', 
        'ready': '3', 
        'done': '0', 
        'waiting': '0', 
        'running': '0', 
        'failed': '0', 
        'total': '6'
    }
]

mock_jobs = [
  {
    "job_id": 1,
    "job_name": "job 0",
    "job_start_date": None,
    "job_end_date": None,
    "job_status": "ready",
    "job_return_code": None,
    "job_id_project": 1,
    "job_session": None,
    "project_name": "project_1",
    "date": None,
    "hms": None,
    "duree": None
  },
  {
    "job_id": 2,
    "job_name": "job 1",
    "job_start_date": None,
    "job_end_date": None,
    "job_status": "ready",
    "job_return_code": None,
    "job_id_project": 1,
    "job_session": None,
    "project_name": "project_1",
    "date": None,
    "hms": None,
    "duree": None
  },
  {
    "job_id": 3,
    "job_name": "job 2",
    "job_start_date": None,
    "job_end_date": None,
    "job_status": "ready",
    "job_return_code": None,
    "job_id_project": 1,
    "job_session": None,
    "project_name": "project_1",
    "date": None,
    "hms": None,
    "duree": None
  },
]

mock_sessions = [
    {
        "sessions_id": 906,
        "sessions_host": "mock_host.fr",
        "sessions_start_date": "2023-10-26T08:37:28.604Z",
        "sessions_end_date": "2023-10-26T08:38:30.443Z",
        "sessions_status": "closed",
        "sessions_tags": [],
        "date_debut": "26-10-2023",
        "hms_debut": "08:37:28",
        "duree": 61.84,
        "date_fin": "26-10-2023",
        "hms_fin": "08:38:30",
        "hms_last_activity": "08:37:28"
    },
]

mock_nodes = [
  {
    "host": "mock_host.fr",
    "closed": "224",
    "active": 0,
    "idle": 0,
    "idle_requested": 0,
    "running": 0,
    "hms_last_activity": "08:37:29"
  }
]

@pytest.fixture
def reader():
    return Reader()

@pytest.fixture
def mock_request():
    with requests_mock.Mocker() as m:
        yield m

def test_get_projects(reader, mock_request):
    mock_request.get(f"{mock_url_api}/api/projects", json=mock_projects)
    projects = reader.get_projects(mock_url_api)

    assert len(projects) == 1
    assert projects[0]['project_name'] == "project_1"
    assert projects[0]['ready'] == "3"

def test_get_jobs(reader, mock_request):
    mock_request.get(f"{mock_url_api}/api/jobs", json=mock_jobs)
    jobs = reader.get_jobs(mock_url_api)

    assert len(jobs) == 3
    assert jobs[0]['job_name'] == "job 0"
    assert jobs[1]['job_name'] == "job 1"
    assert jobs[2]['job_name'] == "job 2"

def test_get_sessions(reader, mock_request):
    mock_request.get(f"{mock_url_api}/api/sessions", json=mock_sessions)
    sessions = reader.get_sessions(mock_url_api)

    assert len(sessions) == 1
    assert sessions[0]['sessions_host'] == "mock_host.fr"

def test_get_nodes(reader, mock_request):
    mock_request.get(f"{mock_url_api}/api/nodes", json=mock_nodes)
    nodes = reader.get_nodes(mock_url_api)

    assert len(nodes) == 1
    assert nodes[0]['host'] == "mock_host.fr"
