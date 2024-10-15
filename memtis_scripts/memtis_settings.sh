#!/bin/bash

function func_memtis_setting() {
    echo 199 | sudo tee /sys/kernel/mm/htmm/htmm_sample_period
    echo 100007 | sudo tee /sys/kernel/mm/htmm/htmm_inst_sample_period
    echo 1 | sudo tee /sys/kernel/mm/htmm/htmm_thres_hot
    echo 2 | sudo tee /sys/kernel/mm/htmm/htmm_split_period
    echo 100000 | sudo tee /sys/kernel/mm/htmm/htmm_adaptation_period
    echo 2000000 | sudo tee /sys/kernel/mm/htmm/htmm_cooling_period
    echo 2 | sudo tee /sys/kernel/mm/htmm/htmm_mode
    echo 500 | sudo tee /sys/kernel/mm/htmm/htmm_demotion_period_in_ms
    echo 500 | sudo tee /sys/kernel/mm/htmm/htmm_promotion_period_in_ms
    echo 4 | sudo tee /sys/kernel/mm/htmm/htmm_gamma
    echo 30 | sudo tee /sys/kernel/mm/htmm/ksampled_soft_cpu_quota

    echo 1 | sudo tee /sys/kernel/mm/htmm/htmm_thres_split

    echo 0 | sudo tee /sys/kernel/mm/htmm/htmm_nowarm

    echo "enabled" | sudo tee /sys/kernel/mm/htmm/htmm_cxl_mode

    echo "always" | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
    echo "always" | sudo tee /sys/kernel/mm/transparent_hugepage/defrag
}

func_memtis_setting
