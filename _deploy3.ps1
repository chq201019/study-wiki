$ErrorActionPreference = 'Stop'
$env:SSH_PASS = 'C-hao-qian-1019'
$env:SSH_TIMEOUT = '1800'
$tar = "$env:TEMP\opencode\content.tar.gz"
if (Test-Path $tar) { Remove-Item $tar -Force }
tar -czf $tar -C . docs src static docusaurus.config.ts sidebars.ts scripts package.json package-lock.json
if ($LASTEXITCODE -ne 0) { throw 'pack failed' }
python "$env:TEMP\opencode\put.py" $tar '/tmp/content.tar.gz'
if ($LASTEXITCODE -ne 0) { throw 'upload failed' }
Write-Host 'uploaded'
$cmd = @'
set -e
cd /opt/study-wiki/app
tar -xzf /tmp/content.tar.gz
rm -rf build
timeout 1200 npm run build > /tmp/build_out.log 2>&1 || { echo BUILD_FAILED; tail -20 /tmp/build_out.log; exit 1; }
tail -3 /tmp/build_out.log
sh /opt/study-wiki/publish.sh /opt/study-wiki/app/build > /tmp/publish_out.log 2>&1 || { echo PUBLISH_FAILED; tail -20 /tmp/publish_out.log; exit 1; }
tail -6 /tmp/publish_out.log
echo DEPLOY_OK
'@
$cmd | python "$env:TEMP\opencode\sshx.py" -
Write-Host "ssh_rc=$LASTEXITCODE"