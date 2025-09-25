import os, time, json
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
import assemblyai as aai   # ✅ AssemblyAI SDK

# Load environment variables
load_dotenv()
app = Flask(__name__)

UPLOAD_DIR = "uploads"
TRANS_DIR = "transcripts"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANS_DIR, exist_ok=True)

# Get AssemblyAI API key
ASSEMBLY_KEY = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = ASSEMBLY_KEY   # ✅ configure SDK

# ---- Pages ----
@app.route("/")
def home():
    return render_template("recorder.html")

@app.route("/viewer")
def viewer():
    return render_template("viewer.html")

# ---- API: Upload audio ----
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    file.save(filepath)

    if not ASSEMBLY_KEY:
        return jsonify({"error": "No AssemblyAI key set"}), 500

    # --- Transcribe using AssemblyAI SDK ---
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.universal)
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(filepath)

    if transcript.status == "error":
        return jsonify({"error": transcript.error}), 500

    transcript_text = transcript.text

    # --- Save transcript (TXT + PDF + JSON) ---
    tid = str(int(time.time()))
    txt_path = os.path.join(TRANS_DIR, f"{tid}.txt")
    pdf_path = os.path.join(TRANS_DIR, f"{tid}.pdf")
    meta_path = os.path.join(TRANS_DIR, f"{tid}.json")

    # Save TXT
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    # Save PDF
    c = canvas.Canvas(pdf_path)
    c.setFont("Helvetica", 12)
    c.drawString(100, 800, "Transcript:")
    y = 780
    for line in transcript_text.split(". "):
        c.drawString(50, y, line.strip())
        y -= 20
        if y < 50:  # new page
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 780
    c.save()

    # Save JSON metadata
    meta = {
        "id": tid,
        "created_at": time.ctime(),
        "txt": f"/download/{tid}/txt",
        "pdf": f"/download/{tid}/pdf",
        "text": transcript_text
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    return jsonify(meta)

# ---- API: List transcripts ----
@app.route("/transcripts")
def list_transcripts():
    files = [f for f in os.listdir(TRANS_DIR) if f.endswith(".json")]
    result = []
    for f in files:
        with open(os.path.join(TRANS_DIR, f)) as jf:
            result.append(json.load(jf))
    return jsonify(result)

# ---- API: Download transcript ----
@app.route("/download/<tid>/<ftype>")
def download_transcript(tid, ftype):
    # Decide file extension
    ext = "txt" if ftype.lower() == "txt" else "pdf"

    # Use your absolute transcripts folder path
    local_trans_folder = r" folder_url"

    return send_from_directory(local_trans_folder, f"{tid}.{ext}", as_attachment=True)

# ---- Run App ----
if __name__ == "__main__":
    app.run(port=8000, debug=True)

