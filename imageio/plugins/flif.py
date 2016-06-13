# -*- coding: utf-8 -*-
# Copyright (c) 2015, imageio contributors
# imageio is distributed under the terms of the (new) BSD License.

""" Simple FLIF image reader
"""

from __future__ import absolute_import, print_function, division

import numpy as np

from .. import formats
from ..core import Format
from ._flif import *

class FlifFormat(Format):
    def _can_read(self, request):
        if request.mode[1] in (self.modes + '?'):
            if request.filename.lower().endswith(self.extensions):
                return True

    # needs to be implemented
    def _can_write(self, request):
        return False

    # -- reader

    class Reader(Format.Reader):

        def _open(self):
            filename = self.request.get_local_filename()
            decoder = FlifDecoder()
            decoder.decode_file(filename)
            image = FlifImage(decoder.get_image(0))
            self.metadata = {'width': image.width, 'height': image.height}
            self._data = bytes()
            for i in range(image.height):
                self._data += bytes(image.read_row_RGBA8(i))
            self._length = 1
            del image
            del decoder

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            pass

        def _get_length(self):
            # Return the number of images. Can be np.inf
            return self._length

        def _get_data(self, index):
            # Return the data and meta data for the given index
            if index >= self._length:
                raise IndexError('Image index %i > %i' % (index, self._length))
                
            # Put in a numpy array
            im = np.frombuffer(self._data, 'uint8')
            im.shape = self.metadata['height'],self.metadata['width'],4
            return im, self.metadata

        def _get_meta_data(self, index):
            return self.metadata

# Register. You register an *instance* of a Format class. Here specify:
format = FlifFormat('flif',  # short name
                     'FLIF is a novel lossless image format.',  # one line descr.
                     '.flif',  # list of extensions
                     'i'  # currently only single images
                     )
formats.add_format(format)