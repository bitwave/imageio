# -*- coding: utf-8 -*-
# Copyright (c) 2015, imageio contributors
# imageio is distributed under the terms of the (new) BSD License.

"""
This module is a simple wrapper for the FLIF C-API
"""

from ctypes import *

class FlifImage(object):
    def __init__(self,width,height,hdr=False):
        self.fl = cdll.LoadLibrary('libflif.so')
        if hdr:
            self.image = char_p(self.fl.flif_create_image(width,height))
        else:
            self.image = char_p(self.fl.flif_create_image_HDR(width,height))
    
    def __init__(self,imgptr):
        self.fl = cdll.LoadLibrary('libflif.so')
        self.image = imgptr
    
    @property
    def width(self):
        if hasattr(self,'image'):
            return self.fl.flif_image_get_width(self.image)
        else:
            return -1
    
    @property
    def height(self):
        if hasattr(self,'image'):
            return self.fl.flif_image_get_height(self.image)
        else:
            return -1
    
    @property
    def nb_channels(self):
        if hasattr(self,'image'):
            return self.fl.flif_image_get_nb_channels(self.image)
        else:
            return -1
    
    def read_row_RGBA8(self,row):
        buffer_size_bytes = self.width*4
        buffer = create_string_buffer(buffer_size_bytes)
        if hasattr(self,'image'):
            self.fl.flif_image_read_row_RGBA8(self.image,row,buffer,buffer_size_bytes)
        return buffer

class FlifDecoder(object):
    def __init__(self):
        self.fl = cdll.LoadLibrary('libflif.so')
        self.decoder = self.fl.flif_create_decoder()
    
    def __del__(self):
        if self.decoder:
            self.fl.flif_destroy_decoder(self.decoder)
    
    def get_image(self,index):
        return self.fl.flif_decoder_get_image(self.decoder,index)
    
    def decode_file(self,filename):
        return self.fl.flif_decoder_decode_file(self.decoder,c_char_p(bytes(filename,'utf-8')))
