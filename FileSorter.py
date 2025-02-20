import os
import subprocess
import re
import shutil
import tempfile
from tika import parser
import ollama
import time

modelToUse = "gemma:2b" # How the model is called in ollama

enableManualPath = False
folderPath = "./Nueva carpeta" # Path to the folder to order

def get_pdf_context(pdf_file, model=modelToUse):
    """
    Extracts text from a PDF using Tika and asks the LLM to extract the context in one or two words.
    The model is instructed to enclose the answer in ** markers.
    """
    parsed = parser.from_file(pdf_file)
    content = parsed.get("content", "")
    if not content:
        return "NoContent"
    
    # Use only a snippet for summarization.
    snippet = content[:1000].strip()
    
    # Prompt the LLM to extract context.
    prompt = (
        "Extract the core context of the following text in exactly one or two words. "
        "Return only the one or two words with no extra commentary:\n\n" + snippet
    )
    
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}], stream=False)
    context = response["message"]["content"].strip()
    return context if context else "NoContent"

def extract_context_from_response(response_text):
    """
    Extracts the text between ** markers from the response.
    If markers are not found, returns the full response.
    """
    match = re.search(r"\*\*(.*?)\*\*", response_text)
    if match:
        return match.group(1).strip()
    else:
        return response_text.strip()

def unify_context_groups(context_groups):
    """
    Unify groups with similar context names. For example, if one key is "X" and another "Red X",
    they will be merged into a single group under the shorter name ("X").
    """
    unified = {}
    # Sort keys by length (shortest first)
    keys_sorted = sorted(context_groups.keys(), key=lambda k: len(k))
    for key in keys_sorted:
        assigned = False
        for ukey in unified.keys():
            # If the key is contained in the unified key or vice versa, merge them.
            if key.lower() in ukey.lower() or ukey.lower() in key.lower():
                unified[ukey].extend(context_groups[key])
                assigned = True
                break
        if not assigned:
            unified[key] = context_groups[key]
    return unified

def process_pdf_folder(folder_path, model=modelToUse, output_zip="organized_pdfs.zip"):
    """
    Scans the folder for PDF files, obtains a context summary for each,
    groups files with identical contexts (extracted from between ** markers) into subfolders,
    unifies similar group names (e.g. "X" and "Red X" become "X"),
    and creates a zip archive of the organized structure.
    """
    # List PDF files in the folder.
    pdf_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf")
    ]
    
    # Build a dictionary mapping the extracted context to a list of PDF paths.
    context_groups = {}
    for pdf in pdf_files:
        full_context = get_pdf_context(pdf, model=model)
        extracted_context = extract_context_from_response(full_context)
        print(f"File: {os.path.basename(pdf)} -> Full Context: '{full_context}' | Extracted: '{extracted_context}'")
        context_groups.setdefault(extracted_context, []).append(pdf)
    
    # Unify similar context group names.
    unified_groups = unify_context_groups(context_groups)
    print("\nUnified Context Groups:")
    for context, files in unified_groups.items():
        print(f"Group '{context}' with {len(files)} files.")
    
    # Create a temporary directory for the organized structure.
    with tempfile.TemporaryDirectory() as temp_dir:
        # For each unified group, create a subfolder and copy the PDFs if there are more than one file.
        for context, files in unified_groups.items():
            if len(files) > 1:  # Only create a folder if more than one file falls into the group.
                # Sanitize the folder name.
                safe_context = "".join(c for c in context if c.isalnum() or c in (" ", "_", "-")).strip() or "Unknown"
                subfolder = os.path.join(temp_dir, safe_context)
                os.makedirs(subfolder, exist_ok=True)
                for file in files:
                    try:
                        shutil.copy2(file, os.path.join(subfolder, os.path.basename(file)))
                    except Exception as e:
                        print(f"Error copying file {file} to folder {subfolder}: {e}")
            else:
                # If there is only one file, copy it directly to the main temp directory.
                for file in files:
                    try:
                        shutil.copy2(file, os.path.join(temp_dir, os.path.basename(file)))
                    except Exception as e:
                        print(f"Error copying file {file} to main folder: {e}")
        
        # Create the zip archive from the temporary directory.
        archive_name = os.path.splitext(output_zip)[0]
        shutil.make_archive(archive_name, 'zip', temp_dir)
        zip_path = f"{archive_name}.zip"
        print(f"\nZip file '{zip_path}' created with the organized structure.")
        return zip_path

if __name__ == "__main__":
    # Start the subprocess (Ollama)
    process = subprocess.Popen(f"ollama run {modelToUse}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Allow Ollama to start (ensure process is running before proceeding)
    time.sleep(2)
    print("Ollama is running in the background.")
    
    # Enable to get the folder path from the user
    # 

    # Enable to automate the folder to order with the hardcoded value at the top
    if enableManualPath:
        folder = input("Enter the path to the folder containing PDFs: ").strip()
    else:
        folder = folderPath
    
    # Process the PDFs and organize them
    process_pdf_folder(folder, model=modelToUse)
    
    # Kill the Ollama subprocess when done
    process.kill()
    print("Ollama process has been killed.")
