import gradio
from gpt3_recipe_assistant import get_recipe_summarys_from_data

def generate(recipe_name):
    summarys = get_recipe_summarys_from_data(recipe_name)
    numbered_summarys = '\n'.join([f"\n**********\n레시피{i+1}. {summary}\n**********" for i, summary in enumerate(list(filter(None,summarys)))])
    return numbered_summarys

# 인터페이스 생성
demo = gradio.Interface(fn=generate, inputs="text", outputs="text")
    
if __name__ == "__main__":
    demo.launch(share=True)