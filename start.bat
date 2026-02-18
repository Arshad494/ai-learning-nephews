@echo off
echo ========================================
echo    AI Learning Hub - Starting Up...
echo ========================================
echo.

echo [1/4] Installing backend dependencies...
cd backend
pip install -r requirements.txt
echo.

echo [2/4] Seeding database...
python seed_data.py
echo.

echo [3/4] Starting backend server...
start "Backend" cmd /c "uvicorn main:app --reload --port 8000"
cd ..

echo [4/4] Installing frontend and starting...
cd frontend
call npm install
start "Frontend" cmd /c "npm run dev"
cd ..

echo.
echo ========================================
echo    AI Learning Hub is running!
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo ========================================
echo.
pause
