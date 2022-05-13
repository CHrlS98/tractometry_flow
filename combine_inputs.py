#!/usr/bin/env python3
"""
Combine rbx and tractoflow outputs into the format required by the flow.
"""
import argparse
from glob import glob
import os
import shutil


def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('tractoflow_root')
    p.add_argument('rbx_root')
    p.add_argument('sub_ids', nargs='+')
    p.add_argument('--output_directory', default='./input')

    p.add_argument('-f', action='store_true', dest='force')
    return p


def clear_outdir(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    os.rmdir(path)


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    if os.path.exists(args.output_directory):
        if not args.force:
            parser.error('Output directory already exists. Use -f to force.')
        else:
            clear_outdir(args.output_directory)
    os.mkdir(args.output_directory)

    for sub_id in args.sub_ids:
        tractoflow_dir = os.path.join(args.tractoflow_root, sub_id)
        rbx_dir = os.path.join(args.rbx_root, sub_id)

        # FODF file
        fodf_file = glob(os.path.join(tractoflow_dir, '**/*fodf.nii.gz'), recursive=True)

        # Mask file
        mask_file = glob(os.path.join(tractoflow_dir, '**/*local_tracking_mask.nii.gz'), recursive=True)
        
        # all bundle files
        rbx_files = glob(os.path.join(rbx_dir, '**/*.trk'), recursive=True)
        
        if len(rbx_files) > 0 and len(fodf_file) > 0 and len(mask_file) > 0:
            output_dir = os.path.join(args.output_directory, sub_id)
            os.mkdir(output_dir)
            os.symlink(fodf_file[0], os.path.join(output_dir, os.path.basename(fodf_file[0])))
            os.symlink(mask_file[0], os.path.join(output_dir, os.path.basename(mask_file[0])))
            out_bundles_dir = os.path.join(output_dir, 'bundles')
            os.mkdir(out_bundles_dir)
            for rbx_file in rbx_files:
                os.symlink(rbx_file, os.path.join(out_bundles_dir, os.path.basename(rbx_file)))


if __name__ == '__main__':
    main()