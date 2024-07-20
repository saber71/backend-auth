import cryptocode
import storage
from fastapi import APIRouter, HTTPException

from constants import STORAGE_NAME, SECRET_KEY
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
    # 向远程服务请求用户密码。如果用户不存在，抛出未认证异常
    res = storage.get(
        {"id": data.id, "name": STORAGE_NAME}, status_code_mapper={404: 401}
    )
    # 解析响应，获取明文密码
    password = res.json()["password"]
    # 对密码进行解密
    password = cryptocode.decrypt(password, SECRET_KEY)
    # 如果解密后的密码与用户提供的密码不匹配，抛出未认证异常
    if password != data.password:
        raise HTTPException(status_code=401, detail="密码不正确")
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
    storage.save(
        {
            "name": STORAGE_NAME,
            "value": [
                {
                    "_id": data.id,
                    "password": cryptocode.encrypt(data.password, SECRET_KEY),
                }
            ],
        }
    )
    return "ok"


@router.get("/has")
def has(id: str):
    """
    检查用户是否存在函数，用于判断用户是否已注册。

    接收用户的ID作为输入，
    通过向远程服务请求来检查用户是否存在。
    """
    # 向远程服务请求用户信息
    res = storage.get({"id": id, "name": STORAGE_NAME}, check=False)
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
    storage.delete({"name": STORAGE_NAME, "id": id})
    return "ok"
