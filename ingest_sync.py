import os
import re
import pdfplumber


class SynchronousIngestionPipeline:

  def __init__(self, file_path: str):
    self.file_path = file_path

  def extract_text_from_pdf(self) -> str:
    """Extracts raw text page by page from a PDF document synchronously."""
    raw_text = ""
    try:
      print(f"[INFO] Opening file synchronously: {self.file_path}")
      with pdfplumber.open(self.file_path) as pdf:
        for i, page in enumerate(pdf.pages):
          text = page.extract_text()
          if text:
            raw_text += f"\n--- Page {i+1} ---\n" + text
      print(f"[SUCCESS] Successfully extracted text from {self.file_path}")
    except Exception as e:
      print(f"[ERROR] Failed to extract PDF synchronously: {e}")
    return raw_text

  def clean_text(self, raw_text: str) -> str:
    """Applies basic ETL cleaning rules: removes excess whitespace and artifacts."""
    cleaned = re.sub(r"[ \t]+", " ", raw_text)
    cleaned = re.sub(r"\n\s*\n", "\n\n", cleaned)
    return cleaned.strip()

  def run(self):
    print("[INFO] Starting Synchronous ETL Ingestion Pipeline...")
    raw_data = self.extract_text_from_pdf()
    if raw_data:
      clean_data = self.clean_text(raw_data)
      output_filename = "cleaned_output.txt"
      with open(output_filename, "w", encoding="utf-8") as f:
        f.write(clean_data)
      print(f"[SUCCESS] Cleaned data saved locally to {output_filename}")
    else:
      print("[WARNING] No text found or extraction failed.")


if __name__ == "__main__":
  sample_file = "sample.pdf"
  if os.path.exists(sample_file):
    pipeline = SynchronousIngestionPipeline(sample_file)
    pipeline.run()
  else:
    print(
        f"[NOTICE] Please place a file named '{sample_file}' in your workspace"
        " directory to run the test."
    )