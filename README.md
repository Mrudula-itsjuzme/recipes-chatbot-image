# Recipe Chatbot with Image Recognition

An AI recipe-assistant concept that combines chatbot interaction with image-based ingredient recognition.

The project explores a practical kitchen workflow: upload an ingredient image, identify possible ingredients, and suggest recipes through a conversational interface.

---

## Project links and evidence

| Item | Link / Note |
|---|---|
| Repository | https://github.com/Mrudula-itsjuzme/recipes-chatbot-image |
| Paper / reference | Applied AI prototype; no paper attached |
| Demo video | Not uploaded yet |
| Deployment | No hosted deployment yet |
| Dataset note | Intended for ingredient images and recipe metadata; dataset sources should be documented before serious reuse |
| Result screenshots | Add sample input image, detected ingredients, and generated recipe response screenshots under `docs/` or `screenshots/` |

---

## Problem statement

People often have ingredients but do not know what to cook with them. A visual recipe assistant can make cooking suggestions faster by recognizing ingredients from images and turning them into recipe ideas.

---

## Features

- ingredient recognition from uploaded images
- chatbot-based recipe discovery
- recipe suggestions based on detected ingredients
- image-processing module structure
- experiment area for ingredient-classification models
- dataset and notebook organization for future training

---

## System flow

```text
Ingredient Image
       ↓
Image Processing / Recognition
       ↓
Ingredient List
       ↓
Recipe Matching
       ↓
Chatbot Response
```

---

## Repository structure

```text
recipes-chatbot-image/
├── src/          # chatbot and image-processing modules
├── experiments/  # model experiments for ingredient classification
├── notebooks/    # exploratory analysis and prototypes
├── datasets/     # image data and recipe metadata
├── docs/         # architecture and methodology notes
└── README.md
```

---

## How to use

```bash
git clone https://github.com/Mrudula-itsjuzme/recipes-chatbot-image.git
cd recipes-chatbot-image

pip install -r requirements.txt
```

Configure any required API keys or model paths, then run the primary app script from the `src/` folder.

---

## Tech focus

- Computer Vision
- Image classification
- Conversational AI
- Recipe recommendation
- Python-based AI prototyping

---

## Future improvements

- add a runnable demo entry point
- include sample input/output images
- improve multi-ingredient recognition
- add personalized recipe preferences
- add voice support for hands-free cooking
- document dataset sources and model accuracy

---

## Author

Built by [Pedamallu Sai Mrudula](https://github.com/Mrudula-itsjuzme) as part of an applied AI, computer-vision, and chatbot portfolio.
