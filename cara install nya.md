1.  # Pastikan Python sudah terinstall
    python --version
    # Harus Python 3.8 ke atas
    Kalau belum, download di: https://python.org/downloads

2.  # Masuk ke folder project
    cd "run bibir AI"

3.  # Buat Virtual Environment (disarankan/opsional)
    # Buat venv
    python -m venv venv

    # Aktifkan venv — Windows:
    venv\Scripts\activate

    # Aktifkan venv — Mac/Linux:
    source venv/bin/activate

4.  # Install Dependencies dari requirements.txt
    pip install -r requirements.txt
    # Karena ada file best.pt (model YOLO/PyTorch), Harus perlu di install ini juga:
    pip install streamlit torch torchvision ultralytics opencv-python pillow

5.  # Jalankan Aplikasi
    python app.py
    # Setelah itu browser akan otomatis terbuka di http://localhost:8501
    
-------------------------------------------------------------------------------------
# Troubleshooting umum >>>

# Kalau error "streamlit not found"
pip install streamlit

# Kalau error terkait torch/CUDA (GPU)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Kalau pakai CPU saja (tidak ada GPU)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu