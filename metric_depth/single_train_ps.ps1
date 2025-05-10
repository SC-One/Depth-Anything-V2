<#
    Main training launcher with dot-sourced configs.
    Usage:
    # Default (vkitti)
    PS> .\dist_train.ps1

    # Hypersim
    PS> .\dist_train.ps1 -ConfigName hypersim
#>

param(
    [ValidateSet('vkitti','hypersim')]
    [string]$ConfigName = 'vkitti'
)

# Load environment variable
$Env:USE_LIBUV = '0'

# Dot-source the chosen config file
$cfgFile = Join-Path $PSScriptRoot "train_configs\$ConfigName.ps1"
if (-not (Test-Path $cfgFile)) {
    Throw "Config file not found: $cfgFile"
}
############# default from original codes:
$epoch           = 120
$bs              = 4
$gpus            = 8
$lr              = 5e-6
$encoder         = 'vitl'
$dataset         = 'hypersim'
$img_size        = 518
$min_depth       = 0.001
$max_depth       = 20
$pretrained_from = "../checkpoints/depth_anything_v2_${encoder}.pth"
$folder_dataset  = "exp/hypersim"
#############
. $cfgFile

# Generate timestamp and save path
try {
    $now = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
} catch {
    Throw "Failed to format date: $_"
}
$save_path = "Z:/MDE/DA_v2/Depth-Anything-V2/metric_depth/output_path/${now}_${dataset}_${encoder}"
if (-not (Test-Path -Path $save_path)) {
    New-Item -ItemType Directory -Path $save_path | Out-Null
}

# Build the training arguments array
echo "Building argument list for training..."
$arguments = @(
    'train.py',
    '--epoch',           $epoch,
    '--encoder',         $encoder,
    '--bs',              $bs,
    '--lr',              $lr,
    '--save-path',       $save_path,
    '--dataset',         $dataset,
    '--img-size',        $img_size,
    '--min-depth',       $min_depth,
    '--max-depth',       $max_depth,
    '--pretrained-from', $pretrained_from,
    '--model-name',      "TrainedModel_$now",
    '--folder-dataset',  $folder_dataset,
    '--random-seed',     42,
    '--port',            20596
)

# Start training with live output & logging
$logFile = Join-Path $save_path "$now.log"
Write-Host "Starting training with config '$ConfigName'..."
Write-Host "------------------------------------------------------------"

python @arguments *>&1 | Tee-Object -FilePath $logFile

Write-Host "------------------------------------------------------------"
Write-Host 'Training completed! Press any key to exit.'
[Console]::ReadKey() | Out-Null
