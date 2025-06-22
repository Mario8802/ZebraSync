# FolderSync – Minimal One-Way Folder Synchronization Tool

A Python-based CLI utility for one-way synchronization between a source and a replica folder.  
Designed for backup automation, job scheduling, and system-level mirroring.  
Built with reliability and zero external dependencies.

---

## Description

FolderSync maintains an identical replica of a source directory.  
All changes in the source (file creation, updates, deletions) are reflected in the replica after each cycle.  
Synchronization is one-way and non-destructive for the source.

Logging is performed both to a specified file and to stdout for monitoring and CI/CD integration.

---

## Key Features

- One-way mirror sync: source → replica
- Full directory recursion
- MD5 hash comparison (no timestamp reliance)
- Auto-create and clean replica
- Logging (console + file)
- No third-party dependencies
- Suitable for cron jobs, systemd timers or CI pipelines

---

## Usage

python sync.py <SOURCE_DIR> <REPLICA_DIR> <INTERVAL_SECONDS> <NUMBER_OF_RUNS> <LOG_FILE_PATH>

### Example:

python sync.py \
  /mnt/data/source \
  /mnt/backup/mirror \
  30 \
  5 \
  ./logs/sync.log

This will:
- Run 5 synchronization cycles
- Wait 30 seconds between each
- Keep the replica fully in sync with the source
- Log each operation to ./logs/sync.log and also to stdout

---

## Practical Examples

Dry run (1 sync, verbose log):
python sync.py ./test/source ./test/replica 1 1 ./test/sync.log

System-level use (cron-style interval):
python sync.py /srv/data /backup/data 300 12 /var/log/foldersync.log

In CI/CD pipeline step:
python sync.py ./deploy_build ./production 10 1 ./build.log

---

## Log Output Example

2025-06-22 23:12:08 - INFO - Copied/Updated: configs/settings.json  
2025-06-22 23:12:08 - INFO - Deleted file: old/file.txt  
2025-06-22 23:12:08 - INFO - Copied/Updated: images/logo.png  

---

## Technical Details

- Source and replica must be different directories
- Script blocks syncing into a subdirectory of source
- MD5 comparison is chunked (4KB) for large file efficiency
- Symlinks are skipped by design
- Handles permission errors and logs them (does not crash)
- Fails early on bad arguments or missing folders

---

## Integration Ready

Can be used in:
- Cron jobs
- Jenkins / GitHub Actions
- Kubernetes Jobs
- Bash automation scripts
- Recovery or forensic tools

---

## Design Principles

- Fail-safe: never modifies source
- Predictable: exact replica output
- Transparent: human-readable logs
- Minimalistic: no frameworks, no magic
- Testable: deterministic behavior by design
