from http import HTTPStatus


def test_get_role_list(client, roles_list):
    response = client.get('/role')
    assert response.status_code == HTTPStatus.OK
    assert response.json.roles == roles_list

def test_create_role(client, admin_token):
    response = client.post('/role', json={
        'code': 'test_role', 'description': 'for test'
        }, headers=admin_token)
    assert response.status_code == HTTPStatus.CREATED

def test_create_role_without_admin_permission(client, user_token):
    response = client.post('/role', json={
        'code': 'test_role', 'description': 'for test'
        }, headers=user_token)
    assert response.status_code == HTTPStatus.FORBIDDEN

def test_get_role_by_id(client, role_by_id_expected):
    response = client.get('/role/a9c6e8da-f2bf-458a-978b-d2f50a031451')
    assert response.status_code == HTTPStatus.OK
    assert response.json.role == role_by_id_expected

def test_get_non_existing_role_by_id(client):
    response = client.get('/role/444433332222')
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_chage_role_details(client, role_by_id_expected):
    response = client.patch('/role/a9c6e8da-f2bf-458a-978b-d2f50a031451', json={
        'code': 'admin', 'description': 'unlimited access to all actions'})
    assert response.status_code == HTTPStatus.OK
    assert response.json.role == role_by_id_expected

def test_delete_role(client, admin_token):
    response = client.delete('/role/7cf56926-054c-4522-ac6f-d9f5d0e9d18e', headers=admin_token)
    assert response.status_code == HTTPStatus.NO_CONTENT

def test_delete_role_without_admin_permissions(client, user_token):
    response = client.delete('/role/7cf56926-054c-4522-ac6f-d9f5d0e9d18e', headers=user_token)
    assert response.status_code == HTTPStatus.FORBIDDEN

def test_assign_roles(client, assigned_roles_to_user, admin_token):
    response = client.post('/assign_roles', json={
        'user_id': '7cd483e9-5888-40fd-813a-a382154bcfd2', 
        'role_ids': ['a9c6e8da-f2bf-458a-978b-d2f50a031451', '7cf56926-054c-4522-ac6f-d9f5d0e9d18e'],
        }, headers=admin_token)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json.user_role == assigned_roles_to_user

def test_assign_roles_without_admin_permissions(client, user_token):
    response = client.post('/assign_roles', json={
        'user_id': '7cd483e9-5888-40fd-813a-a382154bcfd2', 
        'role_ids': ['a9c6e8da-f2bf-458a-978b-d2f50a031451', '7cf56926-054c-4522-ac6f-d9f5d0e9d18e'],
        }, headers=user_token)
    assert response.status_code == HTTPStatus.FORBIDDEN

def test_check_permissions(client, admin_token):
    response = client.post('/check_permissions', json={
        "user_id": "cd483e9-5888-40fd-813a-a382154bcfd2", 
        "role_ids": ["a9c6e8da-f2bf-458a-978b-d2f50a031451", "7cf56926-054c-4522-ac6f-d9f5d0e9d18e"]}, headers=admin_token)
    assert response.status_code == HTTPStatus.OK
    assert response.json.has_permissions == True

def test_check_permissions_without_admin_permission(client, user_token):
    response = client.post('/check_permissions', json={
        "user_id": "cd483e9-5888-40fd-813a-a382154bcfd2", 
        "role_ids": ["a9c6e8da-f2bf-458a-978b-d2f50a031451", "7cf56926-054c-4522-ac6f-d9f5d0e9d18e"]}, headers=user_token)
    assert response.status_code == HTTPStatus.FORBIDDEN
