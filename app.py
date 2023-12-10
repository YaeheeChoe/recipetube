import gradio

def greet(name):
    return "Hello " + name + "!"

demo = gradio.Interface(fn=greet, inputs="text", outputs="text")
    
if __name__ == "__main__":
    demo.launch(share=True)