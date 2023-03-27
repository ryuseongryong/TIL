DEVICE=/dev/nvme2n1
# DEVICE=/dev/nvme1n1

sudo fio --name=fill_disk \
  --filename=$DEVICE --filesize=1000G \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=128K --iodepth=64 --rw=randwrite \
  --iodepth_batch_submit=64  --iodepth_batch_complete_max=64

sudo fio --name=write_bandwidth_test \
  --filename=$DEVICE --filesize=1000G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=1M --iodepth=64  --iodepth_batch_submit=64  --iodepth_batch_complete_max=64 \
  --rw=write --numjobs=16 --offset_increment=100G

sudo fio --name=write_iops_test \
  --filename=$DEVICE --filesize=1000G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=4K --iodepth=256 --rw=randwrite \
  --iodepth_batch_submit=256  --iodepth_batch_complete_max=256

sudo fio --name=write_latency_test \
  --filename=$DEVICE --filesize=1000G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=4K --iodepth=4 --rw=randwrite --iodepth_batch_submit=4  \
  --iodepth_batch_complete_max=4

sudo fio --name=read_bandwidth_test \
  --filename=$DEVICE --filesize=1000G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=1M --iodepth=64 --rw=read --numjobs=16 --offset_increment=100G \
  --iodepth_batch_submit=64  --iodepth_batch_complete_max=64

sudo fio --name=read_iops_test \
  --filename=$DEVICE --filesize=1000G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=4K --iodepth=256 --rw=randread \
  --iodepth_batch_submit=256  --iodepth_batch_complete_max=256

sudo fio --name=read_latency_test \
  --filename=$DEVICE --filesize=1000G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=4K --iodepth=4 --rw=randread \
  --iodepth_batch_submit=4  --iodepth_batch_complete_max=4

sudo fio --name=read_bandwidth_test \
  --filename=$DEVICE --filesize=1000G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --numjobs=4 --thread --offset_increment=500G \
  --bs=1M --iodepth=64 --rw=read \
  --iodepth_batch_submit=64  --iodepth_batch_complete_max=64

sudo fio --name=write_bandwidth_test \
  --filename=$DEVICE --filesize=1000G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --numjobs=4 --thread --offset_increment=500G \
  --bs=1M --iodepth=64 --rw=write \
  --iodepth_batch_submit=64  --iodepth_batch_complete_max=64
