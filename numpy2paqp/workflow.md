# numpy2paqp

This document describes the workflow for conversion contours from numpy text files to QuimP datafiles. Numpy file is expected to contain coordinates of contours in the format for each row:

```
frame1   x1  y1  x2  y2  ...
frame2   x1  y1  x2  y2  ...
...
```

## The workflow

In principle the numpy file is converted to old *paQP* files, which are then processed in QuimP. Final solution (maps) is converted back to *csv* for sake of readability.

1. Run `numpy2paqp` tool to convert numpy dataset to *paQP*. Three files will be generated:
   1. `image.tif` - fake black image of size of processed data needed for BOA
   2. `output_0.paQP` - master file
   3. `output_0.snQP` - file with contours

    ```bash
    python numpy2paqp.py numpy2paqp/test_data/cell_contour009.txt numpy2paqp/test_data/output
    ```

2. Follow the macro to process resulting *paQP* files in QuimP. All files are saved in the folder with master *paQP* file generated in previous step

    ```java
    // First convert to new QCONF format
    run("Format converter", "opts={status:[],areMultipleFiles:true,paramFile:(C:/Users/baniu/Documents/Repos/moving_shapes/numpy2paqp/test_data/output_0.paQP)}");
    // Generate binary mask from contours
    run("Generate mask", "opts={binary:true,paramFile:(C:/Users/baniu/Documents/Repos/moving_shapes/numpy2paqp/test_data/output.QCONF)}");
    // close mask
    close();
    // run ECMM
    run("ECMM Mapping", "opts={paramFile:(C:/Users/baniu/Documents/Repos/moving_shapes/numpy2paqp/test_data/output.QCONF)}");
    saveAs("Tiff", "C:/Users/baniu/Documents/Repos/moving_shapes/numpy2paqp/test_data/ECMM_mappings.tif");
    close();
    // run QAnalysis
    run("QuimP Analysis", "opts={trackColor:Summer,outlinePlot:Speed,sumCov:1.0,avgCov:0.0,mapRes:400,paramFile:(C:/Users/baniu/Documents/Repos/moving_shapes/numpy2paqp/test_data/output.QCONF)}");
    // close two maps
    close();
    close();
    // convert results of QA to csv format
    run("Format converter", "opts={status:[map:coord,map:origin,map:ycoords,map:xcoords,map:motility,map:convexity,map:fluores],areMultipleFiles:true,paramFile:(C:/Users/baniu/Documents/Repos/moving_shapes/numpy2paqp/test_data/output.QCONF)}");
    ```
