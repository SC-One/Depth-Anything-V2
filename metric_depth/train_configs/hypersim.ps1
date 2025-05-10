# HYPERSIM configuration parameters
$epoch           = 40
$bs              = 3
$gpus            = 1
$lr              = 5e-6
$encoder         = 'vitb'
$dataset         = 'hypersim'
$img_size        = 518
$min_depth       = 0.001
$max_depth       = 20
$pretrained_from = "../checkpoints/depth_anything_v2_${encoder}.pth"
$folder_dataset  = "F:/Dataset/Partial_hypersim_extracted"