# TEST_DIR=/opt/nvme2n1/fiotest
TEST_DIR=/opt/nvme1n1/fiotest

sudo mkdir -p $TEST_DIR

sudo fio --name=write_throughput --directory=$TEST_DIR --numjobs=16 \
--size=10G --time_based --runtime=60s --ramp_time=2s --ioengine=libaio \
--direct=1 --verify=0 --bs=1M --iodepth=64 --rw=write \
--group_reporting=1 --iodepth_batch_submit=64 \
--iodepth_batch_complete_max=64

 sudo fio --name=write_iops --directory=$TEST_DIR --size=10G \
--time_based --runtime=60s --ramp_time=2s --ioengine=libaio --direct=1 \
--verify=0 --bs=4K --iodepth=256 --rw=randwrite --group_reporting=1  \
--iodepth_batch_submit=256  --iodepth_batch_complete_max=256

sudo fio --name=read_throughput --directory=$TEST_DIR --numjobs=16 \
--size=10G --time_based --runtime=60s --ramp_time=2s --ioengine=libaio \
--direct=1 --verify=0 --bs=1M --iodepth=64 --rw=read \
--group_reporting=1 \
--iodepth_batch_submit=64 --iodepth_batch_complete_max=64

sudo fio --name=read_iops --directory=$TEST_DIR --size=10G \
--time_based --runtime=60s --ramp_time=2s --ioengine=libaio --direct=1 \
--verify=0 --bs=4K --iodepth=256 --rw=randread --group_reporting=1 \
--iodepth_batch_submit=256  --iodepth_batch_complete_max=256
