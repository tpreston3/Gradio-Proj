# Available AI Models

## PaLM 2 Chat (Legacy)

- **Internal Name:** `models/chat-bison-001`
- **Version:** 001
- **Description:** A legacy text-only model optimized for chat conversations
- **Input Token Limit:** 4096
- **Output Token Limit:** 1024
- **Supported Actions:**
  - `generateMessage`
  - `countMessageTokens`

---
## PaLM 2 (Legacy)

- **Internal Name:** `models/text-bison-001`
- **Version:** 001
- **Description:** A legacy model that understands text and generates text as an output
- **Input Token Limit:** 8196
- **Output Token Limit:** 1024
- **Supported Actions:**
  - `generateText`
  - `countTextTokens`
  - `createTunedTextModel`

---
## Embedding
Gecko

- **Internal Name:** `models/embedding-gecko-001`
- **Version:** 001
- **Description:** Obtain a distributed representation of a text.
- **Input Token Limit:** 1024
- **Output Token Limit:** 1
- **Supported Actions:**
  - `embedText`
  - `countTextTokens`

---
## Gemini 1.0 Pro Vision

- **Internal Name:** `models/gemini-1.0-pro-vision-latest`
- **Version:** 001
- **Description:** The original Gemini 1.0 Pro Vision model version which was optimized for image understanding. Gemini 1.0 Pro Vision was deprecated on July 12, 2024. Move to a newer Gemini version.
- **Input Token Limit:** 12288
- **Output Token Limit:** 4096
- **Supported Actions:**
  - `generateContent`
  - `countTokens`

---
## Gemini 1.0 Pro Vision

- **Internal Name:** `models/gemini-pro-vision`
- **Version:** 001
- **Description:** The original Gemini 1.0 Pro Vision model version which was optimized for image understanding. Gemini 1.0 Pro Vision was deprecated on July 12, 2024. Move to a newer Gemini version.
- **Input Token Limit:** 12288
- **Output Token Limit:** 4096
- **Supported Actions:**
  - `generateContent`
  - `countTokens`

---
## Gemini 1.5 Pro Latest

- **Internal Name:** `models/gemini-1.5-pro-latest`
- **Version:** 001
- **Description:** Alias that points to the most recent production (non-experimental) release of Gemini 1.5 Pro, our mid-size multimodal model that supports up to 2 million tokens.
- **Input Token Limit:** 2000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`

---
## Gemini 1.5 Pro 001

- **Internal Name:** `models/gemini-1.5-pro-001`
- **Version:** 001
- **Description:** Stable version of Gemini 1.5 Pro, our mid-size multimodal model that supports up to 2 million tokens, released in May of 2024.
- **Input Token Limit:** 2000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`
  - `createCachedContent`

---
## Gemini 1.5 Pro 002

- **Internal Name:** `models/gemini-1.5-pro-002`
- **Version:** 002
- **Description:** Stable version of Gemini 1.5 Pro, our mid-size multimodal model that supports up to 2 million tokens, released in September of 2024.
- **Input Token Limit:** 2000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`
  - `createCachedContent`

---
## Gemini 1.5 Pro

- **Internal Name:** `models/gemini-1.5-pro`
- **Version:** 001
- **Description:** Stable version of Gemini 1.5 Pro, our mid-size multimodal model that supports up to 2 million tokens, released in May of 2024.
- **Input Token Limit:** 2000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`

---
## Gemini 1.5 Flash Latest

- **Internal Name:** `models/gemini-1.5-flash-latest`
- **Version:** 001
- **Description:** Alias that points to the most recent production (non-experimental) release of Gemini 1.5 Flash, our fast and versatile multimodal model for scaling across diverse tasks.
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`

---
## Gemini 1.5 Flash 001

- **Internal Name:** `models/gemini-1.5-flash-001`
- **Version:** 001
- **Description:** Stable version of Gemini 1.5 Flash, our fast and versatile multimodal model for scaling across diverse tasks, released in May of 2024.
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`
  - `createCachedContent`

---
## Gemini 1.5 Flash 001 Tuning

- **Internal Name:** `models/gemini-1.5-flash-001-tuning`
- **Version:** 001
- **Description:** Version of Gemini 1.5 Flash that supports tuning, our fast and versatile multimodal model for scaling across diverse tasks, released in May of 2024.
- **Input Token Limit:** 16384
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`
  - `createTunedModel`

---
## Gemini 1.5 Flash

- **Internal Name:** `models/gemini-1.5-flash`
- **Version:** 001
- **Description:** Alias that points to the most recent stable version of Gemini 1.5 Flash, our fast and versatile multimodal model for scaling across diverse tasks.
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`

---
## Gemini 1.5 Flash 002

- **Internal Name:** `models/gemini-1.5-flash-002`
- **Version:** 002
- **Description:** Stable version of Gemini 1.5 Flash, our fast and versatile multimodal model for scaling across diverse tasks, released in September of 2024.
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`
  - `createCachedContent`

---
## Gemini 1.5 Flash-8B

- **Internal Name:** `models/gemini-1.5-flash-8b`
- **Version:** 001
- **Description:** Stable version of Gemini 1.5 Flash-8B, our smallest and most cost effective Flash model, released in October of 2024.
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `createCachedContent`
  - `generateContent`
  - `countTokens`

---
## Gemini 1.5 Flash-8B 001

- **Internal Name:** `models/gemini-1.5-flash-8b-001`
- **Version:** 001
- **Description:** Stable version of Gemini 1.5 Flash-8B, our smallest and most cost effective Flash model, released in October of 2024.
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `createCachedContent`
  - `generateContent`
  - `countTokens`

---
## Gemini 1.5 Flash-8B Latest

- **Internal Name:** `models/gemini-1.5-flash-8b-latest`
- **Version:** 001
- **Description:** Alias that points to the most recent production (non-experimental) release of Gemini 1.5 Flash-8B, our smallest and most cost effective Flash model, released in October of 2024.
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `createCachedContent`
  - `generateContent`
  - `countTokens`

---
## Gemini 1.5 Flash 8B Experimental 0827

- **Internal Name:** `models/gemini-1.5-flash-8b-exp-0827`
- **Version:** 001
- **Description:** Experimental release (August 27th, 2024) of Gemini 1.5 Flash-8B, our smallest and most cost effective Flash model. Replaced by Gemini-1.5-flash-8b-001 (stable).
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`

---
## Gemini 1.5 Flash 8B Experimental 0924

- **Internal Name:** `models/gemini-1.5-flash-8b-exp-0924`
- **Version:** 001
- **Description:** Experimental release (September 24th, Flash-8B, our smallest and most cost effective Flash model. Replaced by Gemini-1.5-flash-8b-001 (stable).
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:**
  - `generateContent`
  - `countTokens`