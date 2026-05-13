import fitz # PyMuPDF
import cv2
import numpy as np
import easyocr
import os

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    # grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # denoising
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    
    # Save temp preprocessed
    temp_path = image_path + "_preprocessed.png"
    cv2.imwrite(temp_path, denoised)
    return temp_path

def extract_text_from_image(image_path):
    results = reader.readtext(image_path)
    text_blocks = []
    confidence_sum = 0
    
    for (bbox, text, prob) in results:
        text_blocks.append(text)
        confidence_sum += prob
        
    full_text = "\n".join(text_blocks)
    avg_confidence = confidence_sum / len(results) if results else 0
    return full_text, avg_confidence

def process_document(filepath: str):
    if filepath.lower().endswith(".pdf"):
        doc = fitz.open(filepath)
        all_text = ""
        total_conf = 0
        pages_processed = 0
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            temp_img = f"{filepath}_page_{page_num}.png"
            pix.save(temp_img)
            
            prep_img = preprocess_image(temp_img)
            if prep_img:
                text, conf = extract_text_from_image(prep_img)
                all_text += f"\n--- Page {page_num+1} ---\n" + text
                total_conf += conf
                pages_processed += 1
                os.remove(prep_img)
            os.remove(temp_img)
            
        return all_text, (total_conf / pages_processed if pages_processed else 0)
    else:
        # Assuming image
        prep_img = preprocess_image(filepath)
        if prep_img:
            text, conf = extract_text_from_image(prep_img)
            os.remove(prep_img)
            return text, conf
        return "", 0
