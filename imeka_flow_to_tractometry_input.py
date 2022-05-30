#!/usr/bin/env python3
"""
Create symlinks to tractometry input files.
"""
import argparse
from glob import glob
import os
import shutil


def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('root_dir')
    p.add_argument('--output_hc', default='./input_hc')
    p.add_argument('--output_ms', default='./input_ms')

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

    if os.path.exists(args.output_hc):
        if not args.force:
            parser.error('Output directory already exists. Use -f to force.')
        else:
            clear_outdir(args.output_hc)
    if os.path.exists(args.output_ms):
        if not args.force:
            parser.error('Output directory already exists. Use -f to force.')
        else:
            clear_outdir(args.output_ms)

    # create output directories
    os.mkdir(args.output_hc)
    os.mkdir(args.output_ms)

    abs_root_dir = os.path.abspath(args.root_dir)

    sub_dirs = [dir for dir in os.listdir(abs_root_dir) 
                if os.path.isdir(os.path.join(abs_root_dir, dir))]

    for sub_id in sub_dirs:
        #  FODF file
        fodf_file = os.path.join(abs_root_dir, sub_id, 'FODF',
                                 os.listdir(os.path.join(abs_root_dir, sub_id,
                                                         'FODF'))[0])
        # Mask file
        mask_file = os.path.join(abs_root_dir, sub_id, 'Add_Additional_Mask_To_WM',
                                 os.listdir(os.path.join(abs_root_dir, sub_id,
                                                         'Add_Additional_Mask_To_WM'))[0])

        # all bundle files
        bundles = glob(os.path.join(abs_root_dir, sub_id, 'Tracking_and_Bundling', '**/*.trk'))

        if '-ms_' in sub_id:
            output_dir = args.output_ms
        elif '-hc_' in sub_id:
            output_dir = args.output_hc
        else:
            print('Unknown sub_id: {}'.format(sub_id))
            continue

        # symlink to subject
        output_dir = os.path.join(output_dir, sub_id)

        os.mkdir(output_dir)
        os.symlink(fodf_file, os.path.join(output_dir, os.path.basename(fodf_file)))
        os.symlink(mask_file, os.path.join(output_dir, sub_id+'_wm_mask.nii.gz'))
        out_bundles_dir = os.path.join(output_dir, 'bundles')
        os.mkdir(out_bundles_dir)
        for bundle_f in bundles:
            os.symlink(bundle_f, os.path.join(out_bundles_dir, os.path.basename(bundle_f)))


if __name__ == '__main__':
    main()