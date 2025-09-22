# Bootstrap '25 submission
This is a simple LLM-based personalized learning platform hosted on https://defang.io.

It uses crew.ai on the backend to invoke `gemini-2.5-flash-lite` as and when needed. The frontend is a simple a static webpage.

All user data is stored on the frontend due to skill issues on part of the developers.

The app features a General mode to clear doubts and explain questions, and a Question Generation mode to generate 10 questions on any given topic. Double clicking a question feeds it back to the LLM to provide a solution with answers.

