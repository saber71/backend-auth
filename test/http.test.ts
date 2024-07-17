import { httpTest, setDefaultAxiosConfig } from "@heraclius/http-test"
import { describe, test } from "vitest"

setDefaultAxiosConfig({ baseURL: "http://localhost:10001" })

//@ts-ignore
await fetch("http://localhost:10001/storage/collection/default?type=memory", { method: "post" })

describe.sequential("backend-auth", () => {
  test("should auth failed before save", async () => {
    await httpTest({ url: "/auth/verify", data: { id: "123", password: "123" }, method: "post" })
      .expectStatus(401)
      .done()
  })
  test("should save success", async () => {
    await httpTest({ url: "/auth/save", data: { id: "123", password: "123" }, method: "post" })
      .expectStatus(200)
      .expectBody("ok")
      .done()
  })
  test("should auth success after save", async () => {
    await httpTest({ url: "/auth/verify", data: { id: "123", password: "123" }, method: "post" })
      .expectStatus(200)
      .expectBody("ok")
      .done()
  })
  test("should exist id", async () => {
    await httpTest({ url: "/auth/has", params: { id: "123" }, method: "get" })
      .expectStatus(200)
      .expectBody(true)
      .done()
  })
  test("should delete success", async () => {
    await httpTest({ url: "/auth/delete", params: { id: "123" }, method: "post" })
      .expectStatus(200)
      .expectBody("ok")
      .done()
  })
  test("should auth failed after delete", async () => {
    await httpTest({ url: "/auth/verify", data: { id: "123", password: "123" }, method: "post" })
      .expectStatus(401)
      .done()
  })
  test("should verify jwt token", async () => {
    const token = await (
      await fetch("http://localhost:10001/auth/jwt/encode", {
        method: "post",
        headers: {
          "Content-Type": "application/json" // 根据实际情况设置请求头
        },
        body: JSON.stringify({ id: "123", password: "123" })
      })
    ).text()
    await httpTest({ url: "/auth/jwt/verify", params: { token }, method: "get" })
      .expectBody(200)
      .expectBody({ id: "123", password: "123" })
      .done()
  })
})
