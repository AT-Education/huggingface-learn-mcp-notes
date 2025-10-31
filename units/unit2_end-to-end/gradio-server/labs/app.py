import gradio as gr

def sentiment(text: str) -> str:
    """Very small, dependency-free sentiment heuristic used for labs.

    This is intentionally tiny so you can run the lab without heavy NLP dependencies.
    Replace with a proper model or TextBlob/transformers pipeline in real labs.
    """
    if not text:
        return "neutral (score=0)"
    t = text.lower()
    score = 0
    for w in ["good", "great", "love", "excellent", "happy", "awesome", "like"]:
        if w in t:
            score += 1
    for w in ["bad", "terrible", "hate", "awful", "sad", "worst", "dislike"]:
        if w in t:
            score -= 1
    label = "positive" if score > 0 else ("negative" if score < 0 else "neutral")
    return f"{label} (score={score})"


demo = gr.Interface(
    fn=sentiment,
    inputs=gr.components.Textbox(lines=3, placeholder="Enter text to analyze"),
    outputs="text",
    title="Minimal Sentiment Tool",
    description="A minimal, dependency-light sentiment tool used as a Gradio lab scaffold.",
)


if __name__ == "__main__":
    demo.launch()
