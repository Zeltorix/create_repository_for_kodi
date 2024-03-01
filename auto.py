import os

os.system('git checkout --orphan latest_branch')
os.system('git add -A')
os.system('git commit -am "Фиксация"')
os.system('git branch -D main')
os.system('git branch -m main')
os.system('git push -f origin main')
print("Автоматический сброс комитов")