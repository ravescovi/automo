#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #########################################################################
# Copyright (c) 2016, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2016. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

"""
Module to create basic tomography data analyis automation.

"""

import os, glob
import string
import unicodedata
from distutils.dir_util import mkpath
import re

import dxchange
import h5py
try:
    import netCDF4 as cdf
except:
    pass
import numpy as np
import tomopy.misc.corr


__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2016, UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'
__all__ = ['append',
           'clean_entry',
           'clean_folder_name', 
           'dataset_info',
           'try_folder',
           'h5group_dims',
           'touch']


def h5group_dims(fname, dataset='exchange/data'):
    """
    Read data from hdf5 file array dims for a specific group.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    dataset : str
        Path to the dataset inside hdf5 file where data is located.

    Returns
    -------
    dims : list
        
    """
    try:
        with h5py.File(fname, "r") as f:
            try:
                data = f[dataset]
            except KeyError:
                return None
            shape = data.shape
    except KeyError:
        shape = None
    return shape


def dataset_info(fname):
    """
    Determine the tomographic data set array dimentions    

    Parameters
    ----------
    fname : str
        h5 full path file name.


    Returns
    -------
    dims : list
        List containing the data set array dimentions.
    """
    
    exchange_base = "exchange"
    tomo_grp = '/'.join([exchange_base, 'data'])
    flat_grp = '/'.join([exchange_base, 'data_white'])
    dark_grp = '/'.join([exchange_base, 'data_dark'])
    theta_grp = '/'.join([exchange_base, 'theta'])
    theta_flat_grp = '/'.join([exchange_base, 'theta_white'])
    tomo_list = []
    try: 
        tomo = h5group_dims(fname, tomo_grp)
        flat = h5group_dims(fname, flat_grp)
        dark = h5group_dims(fname, dark_grp)
        theta = h5group_dims(fname, theta_grp)
        theta_flat = h5group_dims(fname, theta_flat_grp)
        tomo_list.append('tomo')
        tomo_list.append(tomo)
        tomo_list.append('flat')
        tomo_list.append(flat)
        tomo_list.append('dark')
        tomo_list.append(dark)
        tomo_list.append('theta')
        tomo_list.append(theta)
        tomo_list.append('theta_flat')
        tomo_list.append(theta_flat)
        return tomo_list
    except OSError:
        pass


def clean_entry(entry):
    """
    Remove from user last name characters that are not compatible folder names.
     
    Parameters
    ----------
    entry : str
        user last name    
    Returns
    -------
    entry : str
        user last name compatible with directory name   
    """

    
    valid_folder_entry_chars = "-_%s%s" % (string.ascii_letters, string.digits)

    cleaned_folder_name = unicodedata.normalize('NFKD', entry.decode('utf-8', 'ignore')).encode('ASCII', 'ignore')
    return ''.join(c for c in cleaned_folder_name if c in valid_folder_entry_chars)

def clean_folder_name(directory):
    """
    Clean the folder name from unsupported characters before
    creating it.
    

    Parameters
    ----------
    folder : str
        Folder that will be containing multiple h5 files.

    """

    valid_folder_name_chars = "-_"+ os.sep + "%s%s" % (string.ascii_letters, string.digits)
    cleaned_folder_name = unicodedata.normalize('NFKD', directory.decode('utf-8', 'ignore')).encode('ASCII', 'ignore')
    
    return ''.join(c for c in cleaned_folder_name if c in valid_folder_name_chars)

def try_folder(directory):
    """
    Function description.

    Parameters
    ----------
    parameter_01 : type
        Description.

    parameter_02 : type
        Description.

    parameter_03 : type
        Description.

    Returns
    -------
    return_01
        Description.
    """

    print ("2")
    try:
        if os.path.isdir(directory):
            return True
        else:
            print directory + " does not exist"
            a = raw_input('Would you like to create ' + directory + ' ? ').lower()
            if a.startswith('y'): 
                mkpath(directory)
                print("Great!")
                return True
            else:
                print ("Sorry for asking...")
                return False
    except: 
        pass # or raise
    else: 
        return False


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def append(fname, process):
    with open(fname, "a") as pfile:
        pfile.write(process)


def entropy(img, range=(0, 0.002), mask_ratio=0.9, window=None, ring_removal=True, center_x=None, center_y=None):

    temp = np.copy(img)
    if window is not None:
        window = np.array(window, dtype='int')
        temp = temp[window[0][0]:window[1][0], window[0][1]:window[1][1]]
        dxchange.write_tiff(temp, 'tmp/data', dtype='float32', overwrite=False)
    if ring_removal:
        temp = np.squeeze(tomopy.remove_ring(temp[np.newaxis, :, :], center_x=center_x, center_y=center_y))
    if mask_ratio is not None:
        mask = tomopy.misc.corr._get_mask(temp.shape[0], temp.shape[1], mask_ratio)
        temp = temp[mask]
    temp = temp.flatten()
    # temp[np.isnan(temp)] = 0
    temp[np.invert(np.isfinite(temp))] = 0
    hist, e = np.histogram(temp, bins=1024, range=range)
    hist = hist.astype('float32') / temp.size + 1e-12
    val = -np.dot(hist, np.log2(hist))
    return val


def minimum_entropy(folder, pattern='*.tiff', range=(0, 0.002), mask_ratio=0.9, window=None, ring_removal=True,
                    center_x=None, center_y=None):

    flist = glob.glob(os.path.join(folder, pattern))
    a = []
    s = []
    for fname in flist:
        img = dxchange.read_tiff(fname)
        # if max(img.shape) > 1000:
        #     img = scipy.misc.imresize(img, 1000. / max(img.shape), mode='F')
        # if ring_removal:
        #     img = np.squeeze(tomopy.remove_ring(img[np.newaxis, :, :]))
        s.append(entropy(img, range=range, mask_ratio=mask_ratio, window=window, ring_removal=ring_removal,
                         center_x=center_x, center_y=center_y))
        a.append(fname)
    return a[np.argmin(s)]


def read_data_adaptive(fname, proj=None, sino=None, data_format='aps_32id', shape_only=False, return_theta=True, **kwargs):
    """
    Adaptive data reading function that works with dxchange both below and beyond version 0.0.11.
    """
    theta = None
    dxver = dxchange.__version__
    m = re.search(r'(\d+)\.(\d+)\.(\d+)', dxver)
    ver = m.group(1, 2, 3)
    ver = map(int, ver)
    if proj is not None:
        proj_step = 1 if len(proj) == 2 else proj[2]
    if sino is not None:
        sino_step = 1 if len(sino) == 2 else sino[2]
    if data_format == 'aps_32id':
        if shape_only:
            f = h5py.File(fname)
            d = f['exchange/data']
            return d.shape
        try:
            if ver[0] > 0 or ver[1] > 1 or ver[2] > 1:
                dat, flt, drk, theta = dxchange.read_aps_32id(fname, proj=proj, sino=sino)
            else:
                dat, flt, drk = dxchange.read_aps_32id(fname, proj=proj, sino=sino)
                f = h5py.File(fname)
                theta = f['exchange/theta'].value
        except:
            f = h5py.File(fname)
            d = f['exchange/data']
            theta = f['exchange/theta'].value
            if proj is None:
                dat = d[:, sino[0]:sino[1]:sino_step, :]
                flt = f['exchange/data_white'][:, sino[0]:sino[1]:sino_step, :]
                try:
                    drk = f['exchange/data_dark'][:, sino[0]:sino[1]:sino_step, :]
                except:
                    print('WARNING: Failed to read dark field. Using zero array instead.')
                    drk = np.zeros([flt.shape[0], 1, flt.shape[2]])
            elif sino is None:
                dat = d[proj[0]:proj[1]:proj_step, :, :]
                flt = f['exchange/data_white'].value
                try:
                    drk = f['exchange/data_dark'].value
                except:
                    print('WARNING: Failed to read dark field. Using zero array instead.')
                    drk = np.zeros([1, flt.shape[1], flt.shape[2]])
            else:
                dat = None
                flt = None
                drk = None
                print('ERROR: Sino and Proj cannot be specifed simultaneously. ')
    elif data_format == 'aps_13bm':
        f = cdf.Dataset(fname)
        if shape_only:
            return f['array_data'].shape
        if sino is None:
            dat = f['array_data'][proj[0]:proj[1]:proj_step, :, :].astype('uint16')
            basename = os.path.splitext(fname)[0]
            flt1 = cdf.Dataset(basename + '_flat1.nc')['array_data'][...]
            flt2 = cdf.Dataset(basename + '_flat2.nc')['array_data'][...]
            flt = np.vstack([flt1, flt2]).astype('uint16')
            drk = np.zeros([1, flt.shape[1], flt.shape[2]]).astype('uint16')
            drk[...] = 64
        elif proj is None:
            dat = f['array_data'][:, sino[0]:sino[1]:sino_step, :].astype('uint16')
            basename = os.path.splitext(fname)[0]
            flt1 = cdf.Dataset(basename + '_flat1.nc')['array_data'][:, sino[0]:sino[1]:sino_step, :]
            flt2 = cdf.Dataset(basename + '_flat2.nc')['array_data'][:, sino[0]:sino[1]:sino_step, :]
            flt = np.vstack([flt1, flt2]).astype('uint16')
            drk = np.zeros([1, flt.shape[1], flt.shape[2]]).astype('uint16')
            drk[...] = 64

    if return_theta:
        return dat, flt, drk, theta
    else:
        return dat, flt, drk


def most_neighbor_clustering(data, radius):

    data = np.array(data)
    counter = np.zeros(len(data))
    for ind, i in enumerate(data):
        for j in data:
            if j != i and abs(j - i) < radius:
                counter[ind] += 1
    return data[np.where(counter == counter.max())]