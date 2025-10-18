#!/usr/bin/env python3
# test_system.py
"""
系统功能测试脚本
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000/api"

def test_api_endpoint(endpoint, method='GET', data=None, auth_token=None):
    """测试API端点"""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
    }
    
    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            return False, f"不支持的HTTP方法: {method}"
        
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

def test_user_registration():
    """测试用户注册"""
    print("测试用户注册...")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "password2": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }
    
    success, result = test_api_endpoint("/users/register/", "POST", data)
    if success:
        print("✓ 用户注册成功")
        return True
    else:
        print(f"✗ 用户注册失败: {result}")
        return False

def test_user_login():
    """测试用户登录"""
    print("测试用户登录...")
    data = {
        "username": "testuser",
        "password": "TestPassword123!"
    }
    
    success, result = test_api_endpoint("/token/", "POST", data)
    if success and "access" in result:
        print("✓ 用户登录成功")
        return result["access"], result["refresh"]
    else:
        print(f"✗ 用户登录失败: {result}")
        return None, None

def test_plant_list():
    """测试植物列表获取"""
    print("测试植物列表获取...")
    success, result = test_api_endpoint("/plants/")
    if success and "results" in result:
        print(f"✓ 成功获取植物列表，共{len(result['results'])}种植物")
        return True
    else:
        print(f"✗ 获取植物列表失败: {result}")
        return False

def test_my_plants(auth_token):
    """测试我的植物功能"""
    print("测试我的植物功能...")
    
    # 获取我的植物列表
    success, result = test_api_endpoint("/care/my-plants/", "GET", auth_token=auth_token)
    if not success:
        print(f"✗ 获取我的植物列表失败: {result}")
        return False
    
    print("✓ 获取我的植物列表成功")
    
    # 添加新植物
    new_plant = {
        "nickname": "测试植物",
        "plant": 1,  # 假设第一个植物存在
        "location": "客厅窗台",
        "purchase_date": "2024-01-01",
        "status": "healthy",
        "notes": "这是一个测试植物"
    }
    
    success, result = test_api_endpoint("/care/my-plants/", "POST", new_plant, auth_token=auth_token)
    if success and "id" in result:
        print("✓ 添加新植物成功")
        plant_id = result["id"]
        
        # 更新植物信息
        update_data = {
            "notes": "更新后的测试植物信息"
        }
        success, result = test_api_endpoint(f"/care/my-plants/{plant_id}/", "PATCH", update_data, auth_token=auth_token)
        if success:
            print("✓ 更新植物信息成功")
        else:
            print(f"✗ 更新植物信息失败: {result}")
        
        # 删除植物
        success, result = test_api_endpoint(f"/care/my-plants/{plant_id}/", "DELETE", auth_token=auth_token)
        if success:
            print("✓ 删除植物成功")
        else:
            print(f"✗ 删除植物失败: {result}")
        
        return True
    else:
        print(f"✗ 添加新植物失败: {result}")
        return False

def test_care_plan(auth_token):
    """测试养护计划功能"""
    print("测试养护计划功能...")
    
    # 先添加一个植物用于测试
    new_plant = {
        "nickname": "测试植物2",
        "plant": 1,
        "location": "阳台",
        "purchase_date": "2024-01-01",
        "status": "healthy"
    }
    
    success, plant_result = test_api_endpoint("/care/my-plants/", "POST", new_plant, auth_token=auth_token)
    if not success:
        print(f"✗ 添加测试植物失败: {plant_result}")
        return False
    
    plant_id = plant_result["id"]
    
    # 生成养护计划
    success, plan_result = test_api_endpoint(f"/care/my-plants/{plant_id}/generate_care_plan/", "POST", auth_token=auth_token)
    if success:
        print("✓ 生成养护计划成功")
        
        # 获取养护计划列表
        success, plans_result = test_api_endpoint("/care/care-plans/", "GET", auth_token=auth_token)
        if success and len(plans_result["results"]) > 0:
            print("✓ 获取养护计划列表成功")
    else:
        print(f"✗ 生成养护计划失败: {plan_result}")
    
    # 清理测试数据
    test_api_endpoint(f"/care/my-plants/{plant_id}/", "DELETE", auth_token=auth_token)
    
    return success

def main():
    """主测试函数"""
    print("=" * 50)
    print("植物养护管理系统功能测试")
    print("=" * 50)
    
    # 测试顺序
    tests = [
        ("植物列表获取", test_plant_list),
        ("用户注册", test_user_registration),
        ("用户登录", test_user_login),
        ("我的植物功能", lambda: test_my_plants(auth_token) if 'auth_token' in locals() else False),
        ("养护计划功能", lambda: test_care_plan(auth_token) if 'auth_token' in locals() else False),
    ]
    
    # 执行测试
    auth_token = None
    refresh_token = None
    
    for test_name, test_func in tests:
        if test_name == "用户登录":
            success, result = test_func()
            if success:
                auth_token, refresh_token = result
            print()
        else:
            success = test_func()
            print()
    
    print("=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    main()