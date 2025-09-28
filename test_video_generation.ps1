# Test video generation endpoint
$uri = "http://localhost:8000/api/generate-video"

# Simple test with English text
$boundary = [System.Guid]::NewGuid().ToString()
$LF = "`r`n"

$bodyLines = (
    "--$boundary",
    "Content-Disposition: form-data; name=`"image`"; filename=`"test_image.svg`"",
    "Content-Type: image/svg+xml$LF",
    [System.IO.File]::ReadAllText("test_image.svg"),
    "--$boundary",
    "Content-Disposition: form-data; name=`"text`"$LF",
    "Welcome to VEO7 video generation platform",
    "--$boundary",
    "Content-Disposition: form-data; name=`"language`"$LF",
    "en",
    "--$boundary",
    "Content-Disposition: form-data; name=`"voice_speed`"$LF",
    "1.0",
    "--$boundary",
    "Content-Disposition: form-data; name=`"user_id`"$LF",
    "demo-user-9232",
    "--$boundary--$LF"
) -join $LF

try {
    Write-Host "Sending request to generate video..."
    $response = Invoke-RestMethod -Uri $uri -Method POST -Body $bodyLines -ContentType "multipart/form-data; boundary=$boundary"
    Write-Host "Success: Video generation completed"
    Write-Host "Response: $($response | ConvertTo-Json -Depth 3)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}