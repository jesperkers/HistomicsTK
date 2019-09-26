#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 02:25:34 2019.

@author: mtageld
"""
import unittest
import girder_client
import numpy as np
from histomicstk.annotations_and_masks.annotation_and_mask_utils import (
    delete_annotations_in_slide)
from histomicstk.saliency.cellularity_detection import (
    Cellularity_detector_superpixels)

# %%===========================================================================
# Constants & prep work

APIURL = 'http://candygram.neurology.emory.edu:8080/api/v1/'
SAMPLE_SLIDE_ID = "5d586d76bd4404c6b1f286ae"

gc = girder_client.GirderClient(apiUrl=APIURL)
gc.authenticate(apiKey='kri19nTIGOkWH01TbzRqfohaaDWb6kPecRqGmemb')

# color normalization values from TCGA-A2-A3XS-DX1
cnorm_thumbnail = {
    'mu': np.array([9.24496373, -0.00966569,  0.01757247]),
    'sigma': np.array([0.35686209, 0.02566772, 0.02500282]),
}
# from the ROI in Amgad et al, 2019
cnorm_main = {
    'mu': np.array([8.74108109, -0.12440419,  0.0444982]),
    'sigma': np.array([0.6135447, 0.10989545, 0.0286032]),
}

# %%===========================================================================


class CellularityDetectionTest(unittest.TestCase):
    """Test methods for getting ROI mask from annotations."""

    def test_Cellularity_detector_superpixels(self):
        """Test Cellularity_detector_superpixels()."""
        # deleting existing annotations in target slide (if any)
        delete_annotations_in_slide(gc, SAMPLE_SLIDE_ID)

        # run cellularity detector
        cds = Cellularity_detector_superpixels(
            gc, slide_id=SAMPLE_SLIDE_ID, MAG=3.0, max_cellularity=40,
            visualize_spixels=True, visualize_contiguous=True,
            get_tissue_mask_kwargs={
                'deconvolve_first': True, 'n_thresholding_steps': 1,
                'sigma': 2.0, 'min_size': 500, },
            suppress_warnings=True, verbose=2, monitorPrefix='test')
        cds.set_color_normalization_values(
            mu=cnorm_thumbnail['mu'],
            sigma=cnorm_thumbnail['sigma'], what='thumbnail')
        cds.set_color_normalization_values(
            mu=cnorm_main['mu'], sigma=cnorm_main['sigma'], what='main')
        cds.run()

        # just make sure it runs without errors & check visual
        self.assertTrue(True)

# %%===========================================================================


if __name__ == '__main__':
    unittest.main()
