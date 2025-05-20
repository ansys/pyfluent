# Fix for Issue #3911: Ablation Example Missing Plots/Pictures

## Problem

The ablation example in PyFluent is missing the plot images in the documentation. The example references several images in the documentation, but these images are not present in the `doc/source/_static` folder:

- ablation-residual.png
- ablation-drag_force_x.png
- ablation-avg_pressure.png
- ablation-recede_point.png
- ablation-pressure.png
- ablation-mach-number.png
- ablation-mach-number-thumbnail.png

The issue affects the documentation page at: https://fluent.docs.pyansys.com/version/stable/examples/00-fluent/modeling_ablation.html

## Solution

The solution has two parts:

1. Modify the `modeling_ablation.py` example to explicitly save the plot images
2. Run the example to generate the images and copy them to the documentation's static folder

## Implementation Steps

### Step 1: Modify the Ablation Example

The `modeling_ablation.py` example needs to be modified to save the images. The example already creates the plots but doesn't save them to disk with the correct filenames.

The following changes were made to `examples/00-fluent/modeling_ablation.py`:

- Added code to configure picture export settings
- Added code to save each plot with the appropriate filename
- Added code to save the contour images and thumbnails

### Step 2: Run the Example and Copy Images

Created a utility script `copy_ablation_images.py` that:

1. Runs the modified ablation example to generate all the necessary plot images
2. Copies the generated images to the documentation's static directory

## Testing

After running the utility script and rebuilding the documentation, all the images should appear correctly in the ablation example page.

## Files Modified

1. `examples/00-fluent/modeling_ablation.py`
   - Added code to save the plot images with the correct filenames

2. New files created:
   - `copy_ablation_images.py`: Utility script to run the example and copy images to the documentation static folder

## Steps to Verify Fix

1. Run the `copy_ablation_images.py` script:
   ```
   python copy_ablation_images.py
   ```

2. Verify that the following images have been copied to `doc/source/_static`:
   - ablation-residual.png
   - ablation-drag_force_x.png
   - ablation-avg_pressure.png
   - ablation-recede_point.png
   - ablation-pressure.png
   - ablation-mach-number.png
   - ablation-mach-number-thumbnail.png

3. Rebuild the documentation and verify that the images appear correctly in the ablation example page.

## Notes

The issue appears to be that the ablation example references images using Sphinx directives, but the actual images were never created or added to the documentation static folder. The modified example now explicitly saves these images, ensuring they're available for the documentation build process. 