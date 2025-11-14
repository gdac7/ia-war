from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from typing import List, Dict, Optional

class LocalModelTransformers():
    def __init__(self, model_name, bnb_config=True, device: str = "auto"):
        if bnb_config:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
        else:
            bnb_config = None
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.bfloat16
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            padding_side="left"
        )
        
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            self.model.config.pad_token_id = self.model.config.eos_token_id
        
    def generate(
            self,
            user_prompt: str,
            system_prompt: str = None,
            max_tokens: int = 4096,
            temperature: float = 0.7,
            condition: str = ""
    ):
        output_ids = None
        inputs = None
        generation_params = {
            "max_new_tokens": max_tokens,
            "pad_token_id": self.tokenizer.eos_token_id
        }
        if temperature > 0:
            generation_params["do_sample"] = True
            generation_params["temperature"] = temperature
        with torch.inference_mode():
            if getattr(self.tokenizer, "chat_template", None):
                try:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ] if system_prompt else [{"role": "user", "content": user_prompt}]
                    plain_text = self.tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=True
                    )
                    plain_text += condition
                    inputs = self.tokenizer(plain_text, return_tensors="pt").to(self.model.device)
                except:
                    plain_text = f"{system_prompt}\n\n{user_prompt}" if system_prompt else user_prompt
                    plain_text += condition
                    messages = [{"role": "user", "content": plain_text}]
                    inputs = self.tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=True
                    )
                    inputs = self.tokenizer(plain_text, return_tensors="pt").to(self.model.device)
            else:
                plain_text = f"{system_prompt}\n\n{user_prompt}" if system_prompt else user_prompt
                plain_text += condition
                inputs = self.tokenizer(plain_text, return_tensors="pt").to(self.model.device)
            
            
            output_ids = self.model.generate(**inputs, **generation_params)
            input_length = inputs['input_ids'].shape[1]
            generated_tokens = output_ids[0][input_length:]
            final_response = self.wrapper(
                self.tokenizer.decode(
                    generated_tokens,
                    skip_special_tokens=True
                ).strip()
            )
            del inputs
            del output_ids
            torch.cuda.empty_cache()
            return final_response
        
    def wrapper(self, response: str):
        tag = "[END OF MOVE]"
        if tag in response:
            return response.split(tag)[0]
        return response
        
