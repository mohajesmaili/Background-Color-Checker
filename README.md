# Background Color Checker API

This project is a simple **FastAPI**-based service that checks whether the background of an **Image or PDF** is colored or not.

---

##  Features:

- Detect background color for **Images (JPG / PNG)**
- Detect background color for **PDFs (Single Page / Multi-Page)**
- Supports both **Colored** and **Grayscale** detection
- Adjustable **Brightness** and **Difference Thresholds**

---

## Requirements:

- Python 3.8 or higher
- Install dependencies:

```bash
pip install fastapi uvicorn pillow pymupdf
```

---

##  How to Use:

Run the server:

```bash
uvicorn Main:app --reload
```

Open your browser and visit:

```
http://127.0.0.1:8000/docs
```

---

##  API Endpoints:

| Endpoint                              | Description                                       | Input                        | Output                |
|---------------------------------------|---------------------------------------------------|------------------------------|------------------------|
| `/Check_Colored (Image)`              | Check if an uploaded image background is colored  | `UploadFile`                 | `True / False`         |
| `/Check_GrayScale`                    | Check if an uploaded image is grayscale           | `UploadFile`                 | `True / False`         |
| `/Check_Colored (PDF - Single Page)`  | Check if a single page of a PDF is colored        | `UploadFile` + `Page Number` | `True / False`         |
| `/Check_Colored (PDF - Full Page)`    | Check all pages of a PDF for colored backgrounds  | `UploadFile`                 | `List of Colored Pages`|
| `/Check_GrayScale (PDF)`              | Check if a single page of a PDF is grayscale      | `UploadFile` + `Page Number` | `True / False`         |

---

##  Threshold Settings:

You can adjust detection sensitivity in `Main.py`:

```python
Brightness_Threshold = 250
Diff_Threshold = 10
```
