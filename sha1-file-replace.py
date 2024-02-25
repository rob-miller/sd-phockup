#!/usr/bin/python3

import argparse
import os
import shutil
import hashlib
from pathlib import Path

# Constants for directories
srcDir = "live"
destDir = "photos"
discardDir = "discard"
clobberDir = "clobbered"

# Set up command-line argument parsing for dry-run option
parser = argparse.ArgumentParser(description='Process files with optional dry-run mode.')
parser.add_argument('--dry-run', action='store_true', help='Enable dry-run mode: log actions without performing them.')
args = parser.parse_args()

# Set global dry_run variable and dry_run_prefix for logging
dry_run = args.dry_run
dry_run_prefix = "Dry-run: " if dry_run else ""

def compute_sha1(file_path):
    """Compute and return the SHA1 hash of the file at file_path."""
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()

def log_action(action, src=None, dest=None, reason=""):
    """Log action with details, incorporating dry_run_prefix."""
    print(f"{dry_run_prefix}{action}, src: {src}, dest: {dest} [{reason}]")

def ensure_dir_exists(directory):
    """Ensure the specified directory exists; create it if it does not."""
    if not os.path.exists(directory):
        if not dry_run:
            os.makedirs(directory)
        log_action("Create directory", src=directory)

def move_file(src, dest, reason):
    """Move a file from src to dest, logging the action."""
    if not dry_run:
        try:
            shutil.move(src, dest)
        except FileNotFoundError:
            pass
    log_action("Move file", src=src, dest=dest, reason=reason)

def copy_file(src, dest):
    """Copy a file from src to dest, logging the action.  Do not overwrite."""
    if os.path.exists(dest):
        raise FileExistsError(f"copy error from {src} to {dest}: file exists.")
    if not dry_run:
        shutil.copy2(src, dest)
    log_action("Copy file", src=src, dest=dest)

def process_files(src_dir, dest_dir, discard_dir, clobber_dir):
    """Process files in the given directory according to the specified logic."""
    # Ensure the corresponding directories in dest and discard exist
    ensure_dir_exists(dest_dir)
    ensure_dir_exists(discard_dir)

    # Cache SHA1 hashes for all files in dest_dir
    dest_files_sha1 = {f: compute_sha1(os.path.join(dest_dir, f)) for f in os.listdir(dest_dir) if os.path.isfile(os.path.join(dest_dir, f))}
    
    # for k in dest_files_sha1.keys():
    #    print(k, dest_files_sha1[k])

    # Process each file in the src_dir
    for src_file in os.listdir(src_dir):
        src_file_path = os.path.join(src_dir, src_file)
        if not os.path.isfile(src_file_path):
            continue  # Skip if not a file

        src_file_sha1 = compute_sha1(src_file_path)
        
        # Identify and move files with matching SHA1 hash from dest to discard
        for dest_file, dest_hash in dest_files_sha1.items():
            if src_file_sha1 == dest_hash:
                # Move matching file from dest to discard
                move_file(os.path.join(dest_dir, dest_file), os.path.join(discard_dir, dest_file), f"sha1 {src_file}")

                # Additionally, identify and move files with the same base name but .jpeg or .JPG extension
                base_name, _ = os.path.splitext(dest_file)
                base_name_l = base_name.lower()
                for ext in ['.jpeg']:  # , '.JPG']:
                    for dest_file in dest_files_sha1.keys():
                        if (base_name in dest_file or base_name_l in dest_file) and dest_file.endswith(ext):
                            move_file(os.path.join(dest_dir, dest_file), os.path.join(discard_dir, dest_file), f"{ext} on {base_name}")
        
        # ready to copy, check for clobber
        dest_file_path = os.path.join(dest_dir, src_file)
        if os.path.exists(dest_file_path):
            # Ensure the directory structure in clobberDir matches
            clobber_file_path = os.path.join(clobber_dir, src_file)
            os.makedirs(os.path.dirname(clobber_file_path), exist_ok=True)
            move_file(dest_file_path, clobber_file_path, "CLOBBER!")
        # Copy the src file to dest using the original filename, not the SHA1 hash
        try:
            copy_file(src_file_path, dest_file_path)
        except FileExistsError as e:
            if dry_run:
                print(e)
            else:
                raise


def process_directory_structure():
    if not os.path.exists(srcDir) or not os.path.exists(destDir):
        raise FileNotFoundError("srcDir or destDir does not exist, cannot proceed.")
    ensure_dir_exists(discardDir)
    ensure_dir_exists(clobberDir)

    for root, dirs, files in os.walk(srcDir):
        for dir_name in dirs:
            current_src_dir = os.path.join(root, dir_name)
            relative_path = os.path.relpath(current_src_dir, srcDir)
            current_dest_dir = os.path.join(destDir, relative_path)
            current_discard_dir = os.path.join(discardDir, relative_path)
            current_clobber_dir = os.path.join(clobberDir, relative_path)
            process_files(current_src_dir, current_dest_dir, current_discard_dir, current_clobber_dir)

# Uncomment to execute with actual command-line arguments
process_directory_structure()
