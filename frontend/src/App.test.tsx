import { MockWebServer, mockWebServer } from "./TestSupport/MockWebServer.ts"
import { render } from "@testing-library/react"
import { App } from "./App.tsx"

describe("App", () => {
    let server: MockWebServer

    beforeEach(() => {
        server = mockWebServer.create()
    })

    afterEach(async () => {
        await server.stopAsync()
    })

    test("loading the message", async () => {
        server.stub(200, { message: "Oh hai" })

        const page = render(<App apiUrl={server.baseUrl()} />)

        await page.findByText("Oh hai")

        const recordedRequest = server.lastRequest()
        expect(recordedRequest?.method).toEqual("GET")
        expect(recordedRequest?.path).toEqual("/api/hello")
    })

    test("loading the message, on error", async () => {
        const page = render(<App apiUrl={server.baseUrl()} />)

        await page.findByText("Connection error or invalid json")
    })

    test("loading the message, on unexpected json", async () => {
        server.stub(200, { not: "expected" })

        const page = render(<App apiUrl={server.baseUrl()} />)

        await page.findByText("Error decoding the response")
    })
})
