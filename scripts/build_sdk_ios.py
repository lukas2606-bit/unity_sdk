import os, subprocess
from scripting_utils import *

def build(root_dir, ios_submodule_dir, with_test_lib):
    # ------------------------------------------------------------------
    # paths
    srcdir                = '{0}/sdk'.format(ios_submodule_dir)
    lib_out_dir           = '{0}/Assets/Adjust/iOS'.format(root_dir)
    sdk_static_framework  = '{0}/Frameworks/Static/AdjustSdk.framework'.format(srcdir)
    
    # ------------------------------------------------------------------
    # Building AdjustStatic framework target
    debug_green('Building AdjustStatic framework target ...')
    os.chdir(srcdir)
    subprocess.call(['xcodebuild', '-target', 'AdjustStatic', '-configuration', 'Release', 'clean', 'build'])
    copy_file(sdk_static_framework + '/Versions/A/AdjustSdk', lib_out_dir + '/AdjustSdk.a')
    copy_files('*', sdk_static_framework + '/Versions/A/Headers/', lib_out_dir)

    if with_test_lib:
        # ------------------------------------------------------------------
        # Test Library paths
        set_log_tag('IOS-TEST-LIB-BUILD')
        debug_green('Building Test Library started ...')
        waiting_animation(duration=4.0, step=0.025)
        test_static_framework = '{0}/Frameworks/Static/AdjustTestLibrary.framework'.format(srcdir)

        os.chdir('{0}/AdjustTests/AdjustTestLibrary'.format(srcdir))
        subprocess.call(['xcodebuild', '-target', 'AdjustTestLibraryStatic', '-configuration', 'Release', 'clean', 'build'])
        copy_file(test_static_framework + '/Versions/A/AdjustTestLibrary', lib_out_dir + '/AdjustTestLibrary.a')
        copy_files('*', test_static_framework + '/Versions/A/Headers/', lib_out_dir)
        