###### tạo thư mục .streamlit nếu chưa có
New-Item -ItemType Directory -Path $env:USERPROFILE\.streamlit -Force

###### tạo config.toml với fileWatcherType = "poll"
@'
[server]
fileWatcherType = "poll"
'@ | Set-Content -Path $env:USERPROFILE\.streamlit\config.toml -Encoding UTF8

streamlit run streamlit_portfolio.py
# BuildPortfolio
