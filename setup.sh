 
mkdir -p ~/.streamlit/
echo "[general]
email = \"metalarmy101@gmail.com\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
