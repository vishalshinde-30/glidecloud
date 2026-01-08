import PyPDF2
import os
from typing import List, Dict, Any

class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
        """Extract text from PDF with page numbers and metadata"""
        text_chunks = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    if text.strip():
                        text_chunks.append({
                            "text": text,
                            "page_number": page_num + 1,
                            "total_pages": total_pages,
                            "pdf_name": os.path.basename(pdf_path)
                        })
                
            return text_chunks
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
    
    @staticmethod
    def split_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
            
            if i + chunk_size >= len(words):
                break
        
        return chunks