@echo off
cd /d "E:\DA Project Youtube\PROJECT\Project Real-Time Weather"
python pipeline_run.py >> logs\pipeline_log.txt 2>&1
