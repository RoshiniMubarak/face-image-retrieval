# Face Image Retrieval with CelebA + CLIP + FAISS

## Overview
This project implements a **prompt-based face image retrieval pipeline** using the **CelebA dataset**, **OpenAI CLIP** model, and **FAISS** similarity search.  
You can query the dataset with text prompts (e.g., "person with sunglasses") and retrieve matching face images efficiently.

---

## Features
- Use CLIP to encode both images and text prompts into embeddings.
- Index image embeddings using FAISS for fast nearest neighbor search.
- Support for attribute-based filtering using CelebA annotations.
- Evaluate retrieval quality with False Match Rate (FMR).

---

## Dataset
We use the [CelebFaces Attributes Dataset (CelebA)](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html), which contains:
- 202,599 face images of 10,177 identities.
- 40 binary facial attribute annotations per image (e.g., Eyeglasses, Smiling).
- Images with pose variation and background clutter.

### Dataset Download
Due to the dataset size (~1.7GB), **the image folder is NOT included in this repo**.  
Please download and prepare the dataset manually:

1. Download the aligned and cropped images (`img_align_celeba.zip`) from the official source:  
   [CelebA Dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)
2. Extract the images to a folder, e.g., `./celeba/img_align_celeba`
3. Download the attribute annotation file (`list_attr_celeba.txt`) and place it under `./celeba/`

---

## Setup Instructions

### Prerequisites

- Python 3.7+
- GPU recommended for faster encoding (CLIP model)

### Install dependencies

```bash
pip install -r requirements.txt
