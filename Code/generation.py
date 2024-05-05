import torch
import random
import numpy as np
from better_profanity import profanity
from transformers import GPT2Tokenizer, GPT2LMHeadModel


def load_generative_model(model_dir):
    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    model = GPT2LMHeadModel.from_pretrained(model_dir)
    return tokenizer, model


def generate_output(
    model, tokenizer, prompt, temperature=1.0, top_k=50, max_length=150
):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = torch.ones_like(input_ids)
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        top_k=top_k,
        temperature=temperature,
        do_sample=True,
    )
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
    stop_index = decoded_output.find("*")
    if stop_index != -1:
        decoded_output = decoded_output[:stop_index]
    return decoded_output.strip()


def generate_tweet_and_mbti():
    mbti = [
        "ISTJ",
        "ISFJ",
        "INFJ",
        "INTJ",
        "ISTP",
        "ISFP",
        "INFP",
        "INTP",
        "ESTP",
        "ESFP",
        "ENFP",
        "ENTP",
        "ESTJ",
        "ESFJ",
        "ENFJ",
        "ENTJ",
    ]
    random_mbti = random.choice(mbti)
    prompt = f"{random_mbti}: "

    tokenizer, model = load_generative_model("model-generation")
    while True:
        generated_tweet, generated_mbti = "", ""
        generation = generate_output(
            model, tokenizer, prompt, temperature=np.random.rand()
        )
        if not profanity.contains_profanity(generation):
            generated_tweet = generation.split(":", 1)[1].strip().capitalize()
            generated_mbti = generation.split(":", 1)[0]
            break

    return generated_tweet, generated_mbti


if __name__ == "__main__":
    generate_tweet_and_mbti()
