const openRouterUrl = "https://openrouter.ai/api/v1/chat/completions"
const model = "deepseek/deepseek-chat"

export const generateResponse = async (prompt) => {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 120000) // 2 min timeout

    try {
        const res = await fetch(openRouterUrl, {
            method: 'POST',
            signal: controller.signal,
            headers: {
                Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: model,
                max_tokens: 8000,
                messages: [
                    { role: "system", content: "You must return ONLY valid raw JSON. No markdown, no backticks." },
                    { role: "user", content: prompt },
                ],
                temperature: 0.2
            }),
        })
        clearTimeout(timeout)

        if (!res.ok) {
            const err = await res.text()
            throw new Error("openRouter err" + err)
        }

        const data = await res.json()
        return data.choices[0].message.content

    } catch (error) {
        clearTimeout(timeout)
        throw error
    }
}
