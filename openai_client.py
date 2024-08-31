from openai import OpenAI

class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def summarize_paper(self, title, link):
        # Update the prompt to ask for a structured summary
        prompt = (
            f"Summarize the following paper in the format below:\n"
            f"Paper Title: {title}\n"
            f"Paper Link: {link}\n"
            f"\n"
            f"1. Key Idea:\n"
            f"2. Motivation:\n"
            f"3. Experiments / Datasets / Evals:\n"
            f"4. Results:\n"
            f"5. Strengths and Weakness:\n"
            f"6. Conclusion:"
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Convert the response to a dictionary
        response_dict = response.to_dict()
        return response_dict['choices'][0]['message']['content']
