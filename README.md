# Super AI Master API 🚀

Super advanced Flask API bina API keys ke! Mixes Claude Sonnet 3.5/Opus, GPT-4o/5.2, Gemini Ultra powers. Chat, vision, file analysis, study, notebook/slide gen, image gen. Fastest free providers via g4f.[cite:4]

## Quick Deploy on Render
1. Fork/Connect this repo to Render.
2. Build: Python
3. Start: Procfile (gunicorn app:app)
4. Env: PORT=10000

Live: [your-render-url]/health

## Endpoints

| Endpoint | Usage | Example |
|----------|--------|---------|
|/v1/chat POST | JSON {'messages':[...], 'model':'gpt-4o'} | Unlimited chat |
|/v1/vision POST | {'messages':..., 'image_b64':...} | Image analyze |
|/v1/analyze_file POST | Multipart file + prompt | PDF/Image study |
|/v1/study POST | {'content':..., 'mode':'quiz'} | Tutor mode |
|/v1/notebook POST | {'prompt':...} | Download .ipynb |
|/v1/slide POST | {'prompt':...} | MD slides |
|/v1/image_gen POST | {'prompt':...} | Image b64 |
|/v1/desk POST | {'prompt':...} | Dashboard code |

OpenAI compatible - sell sub-APIs!

Test: curl -X POST [url]/v1/chat -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"Hi"}] }'

No limits, flexible, future-proof.