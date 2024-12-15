@echo off
rem npm run devを別ウィンドウで起動し、サーバーを立ち上げ続ける
start cmd /k "npm run dev"

rem サーバー起動完了待機（5秒）
timeout /t 5 /nobreak >nul

rem ブラウザで http://localhost:3000 を開く
start "" "http://localhost:3000/"

