git add -A
$gitMessage = Read-Host "git commit Message"
git commit -m $gitMessage
git push