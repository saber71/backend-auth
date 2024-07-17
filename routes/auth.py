# 导入加密模块和请求库，用于数据加密和外部API通信
import cryptocode
import requests
# 导入FastAPI的相关组件，用于构建API路由和处理HTTP请求
from fastapi import APIRouter, HTTPException

# 从常量模块导入基础URL、存储名称和密钥，用于API调用和数据加密
from constants import BASE_URL, STORAGE_NAME, SECRET_KEY
# 从模型模块导入认证信息类，用于解析请求中的认证数据
from models.auth import Auth

# 初始化API路由器，用于定义和管理API端点
router = APIRouter()


@router.post("/verify")
def auth(data: Auth):
    """
    认证函数，用于验证用户身份。

    接收一个包含用户ID和密码的Auth对象作为输入，
    通过向远程服务发送请求来验证密码的正确性。

    如果用户不存在或密码不匹配，将抛出HTTPException异常，
    否则返回"ok"表示认证成功。
    """
    # 向远程服务请求用户密码
    res = requests.get(
        BASE_URL + "/storage/get", params={"id": data.id, "name": STORAGE_NAME}
    )
    # 如果用户不存在，抛出未认证异常
    if res.status_code == 404:
        raise HTTPException(status_code=401)
    # 解析响应，获取明文密码
    password = res.json()["password"]
    # 对密码进行解密
    password = cryptocode.decrypt(password, SECRET_KEY)
    # 如果解密后的密码与用户提供的密码不匹配，抛出未认证异常
    if password != data.password:
        raise HTTPException(status_code=401)
    # 认证成功，返回"ok"
    return "ok"


@router.post("/save")
def save(data: Auth):
    """
    保存用户密码函数，用于将用户密码存储到远程服务。

    接收一个包含用户ID和密码的Auth对象作为输入，
    将加密后的密码存储到远程服务。
    """
    # 构建要存储的数据，包括加密后的密码
    res = requests.post(
        BASE_URL + "/storage/save",
        json={
            "name": STORAGE_NAME,
            "value": [
                {
                    "_id": data.id,
                    "password": cryptocode.encrypt(data.password, SECRET_KEY),
                }
            ],
        },
    )
    # 如果存储成功，返回"ok"，否则抛出异常
    if res.status_code == 200:
        return "ok"
    raise HTTPException(status_code=res.status_code, detail=res.text)


@router.get("/has")
def has(id: str):
    """
    检查用户是否存在函数，用于判断用户是否已注册。

    接收用户的ID作为输入，
    通过向远程服务请求来检查用户是否存在。
    """
    # 向远程服务请求用户信息
    res = requests.get(
        BASE_URL + "/storage/get", params={"id": id, "name": STORAGE_NAME}
    )
    # 返回用户是否存在，通过响应状态码判断
    return res.status_code != 404


@router.post("/delete")
def delete(id: str):
    """
    删除用户函数，用于从远程服务中删除用户密码。

    接收用户的ID作为输入，
    向远程服务发送请求以删除指定用户的密码。
    """
    # 向远程服务发送删除请求
    res = requests.post(
        BASE_URL + "/storage/delete", json={"name": STORAGE_NAME, "id": id}
    )
    # 如果删除成功，返回"ok"，否则抛出异常
    if res.status_code == 200:
        return "ok"
    raise HTTPException(status_code=res.status_code, detail=res.text)
