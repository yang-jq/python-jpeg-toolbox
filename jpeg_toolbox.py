#!/usr/bin/python3


import copy
from ctypes import *
import numpy as np



def load(path, use_blocks=False):
   jpeg = CDLL('./jpeg.so')
   jpeg.write_file.argtypes = c_char_p,
   jpeg.read_file.restype = py_object
   r = jpeg.read_file(path.encode())

   r["quant_tables"] = np.array(r["quant_tables"])
   r["coef_arrays"] = np.array(r["coef_arrays"])

   for i in range(len(r["ac_huff_tables"])):
      r["ac_huff_tables"][i]["counts"] = np.array(r["ac_huff_tables"][i]["counts"])
      r["ac_huff_tables"][i]["symbols"] = np.array(r["ac_huff_tables"][i]["symbols"])

   for i in range(len(r["dc_huff_tables"])):
      r["dc_huff_tables"][i]["counts"] = np.array(r["dc_huff_tables"][i]["counts"])
      r["dc_huff_tables"][i]["symbols"] = np.array(r["dc_huff_tables"][i]["symbols"])

   if not use_blocks:
      chn = len(r["coef_arrays"])
      w = r["image_width"]
      h = r["image_height"]
      r["coef_arrays"] = np.moveaxis(r["coef_arrays"], [0,1,2,3,4], [0,1,3,2,4])
      r["coef_arrays"] = r["coef_arrays"].reshape((chn, w, h))

   return r


def save(data, path, use_blocks=False):
   jpeg = CDLL('./jpeg.so')
   jpeg.write_file.argtypes = py_object,c_char_p

   r = copy.deepcopy(data)
   r["quant_tables"] = r["quant_tables"].tolist()

   for i in range(len(r["ac_huff_tables"])):
      r["ac_huff_tables"][i]["counts"] = r["ac_huff_tables"][i]["counts"].tolist()
      r["ac_huff_tables"][i]["symbols"] = r["ac_huff_tables"][i]["symbols"].tolist()

   for i in range(len(r["dc_huff_tables"])):
      r["dc_huff_tables"][i]["counts"] = r["dc_huff_tables"][i]["counts"].tolist()
      r["dc_huff_tables"][i]["symbols"] = r["dc_huff_tables"][i]["symbols"].tolist()

   if not use_blocks:
      chn = len(r["coef_arrays"])
      w = r["image_width"]
      h = r["image_height"]
      r["coef_arrays"] = r["coef_arrays"].reshape((chn, w//8, 8, h//8, 8))
      r["coef_arrays"] = np.moveaxis(r["coef_arrays"], [0,1,2,3,4], [0,1,3,2,4])

   r["coef_arrays"] = r["coef_arrays"].tolist()


   jpeg.write_file(r, path.encode())



