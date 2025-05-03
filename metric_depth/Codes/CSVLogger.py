import os
import csv
import time

class CSVLogger:
    def __init__(self,
                 save_dir: str,
                 plot: bool = False,
                 metrics_filename: str = 'metrics.csv',
                 step_filename: str = 'train_steps.csv'):
        """
        A logger that writes per-epoch and per-step metrics to CSV.

        Args:
            save_dir: Directory to save CSVs.
            plot: Ignored (plotting functionality removed).
            metrics_filename: Filename for epoch metrics CSV.
            step_filename: Filename for step metrics CSV.
        """
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        # --- CSV setup ---
        # Epoch metrics
        self.metrics_path = os.path.join(save_dir, metrics_filename)
        self.metrics_file = open(self.metrics_path, 'w', newline='')
        self.metrics_writer = csv.writer(self.metrics_file)
        self.metrics_writer.writerow([
            'epoch', 'time_s', 'avg_train_loss', 'lr',
            'd1', 'd2', 'd3',
            'abs_rel', 'sq_rel', 'rmse', 'rmse_log', 'log10', 'silog'
        ])
        # Step metrics (lazy init)
        self.step_path = os.path.join(save_dir, step_filename)
        self.step_file = None
        self.step_writer = None

    def on_epoch_start(self):
        """Call at the top of each epoch to start timing."""
        self._epoch_start = time.time()

    def log_epoch(self,
                  epoch: int,
                  avg_train_loss: float,
                  lr: float,
                  metrics: dict):
        """
        Call at the end of each epoch.
        Writes to CSV.
        """
        elapsed = time.time() - self._epoch_start
        row = [
            epoch,
            round(elapsed, 2),
            round(avg_train_loss, 6),
            round(lr, 8),
        ] + [round(metrics[k], 6) for k in (
            'd1', 'd2', 'd3',
            'abs_rel', 'sq_rel', 'rmse', 'rmse_log', 'log10', 'silog'
        )]
        self.metrics_writer.writerow(row)
        self.metrics_file.flush()

    def log_step(self, global_step: int, loss: float, lr: float):
        """
        Call each training iteration to record loss and lr.
        Lazily initializes the step CSV on first use.
        """
        if self.step_writer is None:
            self.step_file = open(self.step_path, 'w', newline='')
            self.step_writer = csv.writer(self.step_file)
            self.step_writer.writerow(['global_step', 'loss', 'lr'])
        self.step_writer.writerow([global_step, round(loss, 6), round(lr, 8)])
        self.step_file.flush()

    def close(self):
        """Close files."""
        self.metrics_file.close()
        if self.step_file:
            self.step_file.close()
