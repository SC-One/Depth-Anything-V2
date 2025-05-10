# PowerShell version of dist_train.sh
$Env:USE_LIBUV = "0"

# Get current date in YYYYMMDD_HHMMSS format
$now = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

# Training parameters
$epoch = 60
$bs = 4
$gpus = 1
$lr = 0.000005
$encoder = "vitb"
$dataset = "vkitti" # "vkitti", "hypersim"
$img_size = 518
$min_depth = 0.001
$max_depth = 80 # vkitti: 80 , hypersim: 20
$pretrained_from = "../checkpoints/depth_anything_v2_${encoder}.pth"
$save_path = "Z:/MDE/DA_v2/Depth-Anything-V2/metric_depth/output_path/${now}_${dataset}_${encoder}" # "exp/vkitti"
$folder_dataset = "G:/Dataset/vikitti/vkitti_2.0.3"
# "F:/Dataset/Partial_hypersim_extracted"
# "F:/Dataset/vikitti/vkitti_2.0.3"

# Create save directory if it doesn't exist
if (!(Test-Path -Path $save_path)) {
    New-Item -ItemType Directory -Path $save_path | Out-Null
}

# Build the command arguments
$arguments = @(
    # "-m", "torch.distributed.launch",
    # "--nproc_per_node=$gpus",
    # "--nnodes", "1",
    # "--node_rank=0",
    # "--master_addr=localhost",
    # "--master_port=20596",
    "train.py",
    "--epoch", $epoch,
    "--encoder", $encoder,
    "--bs", $bs,
    "--lr", $lr,
    "--save-path", $save_path,
    "--dataset", $dataset,
    "--img-size", $img_size,
    "--min-depth", $min_depth,
    "--max-depth", $max_depth,
    "--pretrained-from", $pretrained_from,
    "--model-name", "TrainedModel_${now}",
    "--folder-dataset", $folder_dataset,
    "--random-seed", 42,
    "--port", "20596"
)

# Execute with live output and logging
$logFile = "${save_path}/${now}.log"
Write-Host "Starting training - output will be shown below and saved to $logFile"
Write-Host "------------------------------------------------------------"

# Run command with live output and logging
python $arguments *>&1 | Tee-Object -FilePath $logFile

# Keep window open after completion
Write-Host "------------------------------------------------------------"
Write-Host "Training completed! Press any key to continue..."
[Console]::ReadKey() | Out-Null