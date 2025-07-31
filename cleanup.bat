@echo off
echo Cleaning up uploaded and converted files...

if exist "uploads" (
    echo Removing uploads directory...
    rmdir /s /q "uploads"
    mkdir "uploads"
    echo Uploads directory cleaned.
)

if exist "outputs" (
    echo Removing outputs directory...
    rmdir /s /q "outputs"
    mkdir "outputs"
    echo Outputs directory cleaned.
)

echo.
echo Cleanup complete! All temporary files have been removed.
echo.
pause
