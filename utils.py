import os
import torch
import clip
import pickle
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load image embeddings
image_embeddings = torch.load("image_embeddings.pt", map_location=torch.device('cpu'))

# Load valid image names
with open("valid_images.pkl", "rb") as f:
    valid_images = pickle.load(f)

# Update all paths to match your actual local dataset path
actual_img_dir = r"C:\\Users\\91763\\Downloads\\img_align_celeba\\img_align_celeba"
valid_images = [os.path.join(actual_img_dir, os.path.basename(path)) for path in valid_images]

# Convert to tensor if needed
if isinstance(image_embeddings, list):
    image_embeddings = torch.stack(image_embeddings)

def text_to_embedding(prompt):
    text = clip.tokenize([prompt]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)
    text_features = text_features.to(dtype=image_embeddings.dtype)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    return text_features

def search_images(prompt, top_k=5):
    text_embedding = text_to_embedding(prompt)
    similarities = (image_embeddings @ text_embedding.T).squeeze(1)
    top_indices = similarities.topk(top_k).indices.cpu().numpy()

    results = []
    for i, idx in enumerate(top_indices):
        results.append({
            "path": valid_images[idx],
            "score": float(similarities[idx])
        })
    return results
