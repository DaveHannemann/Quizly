@echo off

git add .
set /p msg=Commit message:

git commit -m "%msg%"
git push
ssh davidhannemanndev@34.105.215.66 "cd /home/davidhannemanndev/projects/Quizly && git pull --rebase && sudo supervisorctl restart quizly_gunicorn"
